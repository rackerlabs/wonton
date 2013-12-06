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
