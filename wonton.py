import gevent
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from gevent.queue import Queue

import argparse
import libcloud.storage.types

from libcloud.storage.providers import get_driver
from libcloud.storage.types import Provider


__version__ = '0.1.0'

queue = Queue()


def handle_args():
    desc = ('Wonton: Gevent-based, multithreaded tool for bulk transferring '
            'S3 to Cloud Files or vice versa')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--version', action='version',
                        version=__version__)
    parser.add_argument('--threads', required=False, type=int,
                        default=10,
                        help='Number of concurrent threads. Default 10')

    from_args = parser.add_mutually_exclusive_group(required=True)
    from_args.add_argument('--from-s3', action='store_const', const='S3',
                           dest='from_service',
                           help='Copy files from S3 to Cloud Files')
    from_args.add_argument('--from-cf', action='store_const', const='CF',
                           dest='from_service',
                           help='Copy files from Cloud Files to S3')

    cf = parser.add_argument_group('Cloud Files')
    cf.add_argument('--cf-container', required=True,
                    help='Name of the Cloud Files container')
    cf.add_argument('--cf-region', required=True,
                    default='DFW',
                    help='Cloud Files region where the specified '
                         'container exists. Defaults to DFW.')
    cf.add_argument('--cf-username', required=True,
                    help='Cloud Files username')
    cf.add_argument('--cf-password', required=True,
                    help='Cloud Files API Key')

    s3 = parser.add_argument_group('S3')
    s3.add_argument('--s3-container', required=True,
                    help='Name of the S3 container')
    s3.add_argument('--s3-access-id', required=True,
                    help='AWS Access Key ID')
    s3.add_argument('--s3-access-key', required=True,
                    help='AWS Access Key')

    return parser.parse_args()


def create_destination(args):
    cf_driver = get_driver(Provider.CLOUDFILES_US)
    cf = cf_driver(args.cf_username, args.cf_password,
                   ex_force_service_region=args.cf_region)
    s3_driver = get_driver(Provider.S3)
    s3 = s3_driver(args.s3_access_id, args.s3_access_key)

    if args.from_service == 'S3':
        try:
            cf.create_container(args.cf_container)
        except libcloud.storage.types.ContainerAlreadyExistsError:
            pass
        except Exception as e:
            raise SystemExit(e)
        return s3.get_container(args.s3_container)
    elif args.from_service == 'CF':
        try:
            s3.create_container(args.s3_container)
        except (libcloud.storage.types.ContainerAlreadyExistsError):
            pass
        except Exception as e:
            raise SystemExit(e)
        return cf.get_container(args.cf_container)


def populate_queue(cont):
    for obj in cont.list_objects():
        queue.put_nowait(obj)


def put_s3(i, args):
    print 'Thread %4d: Start' % i
    cf_driver = get_driver(Provider.CLOUDFILES_US)
    cf = cf_driver(args.cf_username, args.cf_password,
                   ex_force_service_region=args.cf_region)
    cf_cont = cf.get_container(args.cf_container)

    s3_driver = get_driver(Provider.S3)
    s3 = s3_driver(args.s3_access_id, args.s3_access_key)
    s3_cont = s3.get_container(args.s3_container)

    while 1:
        try:
            obj = queue.get_nowait()
        except gevent.queue.Empty:
            print 'Thread %4d: Queue empty' % i
            raise gevent.GreenletExit
        else:
            obj.driver = cf
            obj.container = cf_cont

            print 'Thread %4d: Upload %s' % (i, obj.name)
            obj_stream = obj.as_stream()
            s3_cont.upload_object_via_stream(obj_stream, obj.name,
                                             extra=obj.extra)
            print 'Thread %4d: Upload complete %s' % (i, obj.name)
    print 'Thread %4d: Complete' % i


def put_cf(i, args):
    print 'Thread %4d: Start' % i
    cf_driver = get_driver(Provider.CLOUDFILES_US)
    cf = cf_driver(args.cf_username, args.cf_password,
                   ex_force_service_region=args.cf_region)
    cf_cont = cf.get_container(args.cf_container)

    s3_driver = get_driver(Provider.S3)
    s3 = s3_driver(args.s3_access_id, args.s3_access_key)
    s3_cont = s3.get_container(args.s3_container)

    while 1:
        try:
            obj = queue.get_nowait()
        except gevent.queue.Empty:
            print 'Thread %4d: Queue empty' % i
            raise gevent.GreenletExit
        else:
            obj.driver = s3
            obj.container = s3_cont

            print 'Thread %4d: Upload %s' % (i, obj.name)
            obj_stream = obj.as_stream()
            cf_cont.upload_object_via_stream(obj_stream, obj.name,
                                             extra=obj.extra)
            print 'Thread %4d: Upload complete %s' % (i, obj.name)
    print 'Thread %4d: Complete' % i


def spawn_copy(args):
    pool = Pool(size=args.threads)
    if args.from_service == 'S3':
        uploader = put_cf
    elif args.from_service == 'CF':
        uploader = put_s3
    for i in xrange(args.threads):
        pool.spawn(uploader, i, args)
    pool.join()


if __name__ == '__main__':
    args = handle_args()
    source = create_destination(args)
    populate_queue(source)
    spawn_copy(args)
