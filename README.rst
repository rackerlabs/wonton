wonton
======

Gevent-based, multithreaded tool for bulk transferring objects from Amazon S3 to Rackspace Cloud Files or vice versa

Installation
------------

Requirements
~~~~~~~~~~~~

#. `gevent <https://pypi.python.org/pypi/gevent>`_
#. `apache-libcloud <https://pypi.python.org/pypi/apache-libcloud>`_
#. Python 2.6 or 2.7

**Note:** gevent currently does not support Python 3

Red Hat / CentOS / Fedora
~~~~~~~~~~~~~~~~~~~~~~~~~

**Note:** This will require at least Red Hat / CentOS 6 or newer, due to the dependency on python 2.6. You can get python 2.6 or newer on older OSes using 3rd party repositories or utilizing `pythonz <http://saghul.github.io/pythonz/>`_.

.. code-block:: bash

    sudo yum -y install gcc python-devel python-pip python-virtualenv python-argparse
    virtualenv ~/wonton
    cd ~/wonton
    . bin/activate
    pip install apache-libcloud git+https://github.com/rackerlabs/wonton.git

Ubuntu / Debian
~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo apt-get -y install gcc python-dev python-pip python-virtualenv
    virtualenv ~/wonton
    cd ~/wonton
    . bin/activate
    pip install apache-libcloud git+https://github.com/rackerlabs/wonton.git

Usage
-----

.. code-block::

    $ wonton --help
    usage: wonton [-h] [--version] [--threads THREADS] (--from-s3 | --from-cf)
                  --cf-container CF_CONTAINER --cf-region CF_REGION
                  --cf-username CF_USERNAME --cf-password CF_PASSWORD
                  --s3-container S3_CONTAINER --s3-access-id S3_ACCESS_ID
                  --s3-access-key S3_ACCESS_KEY

    Wonton: Gevent-based, multithreaded tool for bulk transferring S3 to Cloud
    Files or vice versa

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --threads THREADS     Number of concurrent threads. Default 10
      --from-s3             Copy files from S3 to Cloud Files
      --from-cf             Copy files from Cloud Files to S3

    Cloud Files:
      --cf-container CF_CONTAINER
                            Name of the Cloud Files container
      --cf-region CF_REGION
                            Cloud Files region where the specified container
                            exists. Defaults to DFW.
      --cf-username CF_USERNAME
                            Cloud Files username
      --cf-password CF_PASSWORD
                            Cloud Files API Key

    S3:
      --s3-container S3_CONTAINER
                            Name of the S3 container
      --s3-access-id S3_ACCESS_ID
                            AWS Access Key ID
      --s3-access-key S3_ACCESS_KEY
                            AWS Access Key
