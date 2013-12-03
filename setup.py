import setuptools

setuptools.setup(
    name='wonton',
    version='0.1.0',
    description=('Gevent-based, multithreaded tool for bulk transferring S3 '
                 'to Cloud Files or vice versa'),
    long_description=open('README.rst').read(),
    keywords='rackspace cloud cloudfiles amazon aws s3',
    author='Matt Martz',
    author_email='matt@sivel.net',
    url='https://github.com/sivel/wonton',
    license='Apache License, Version 2.0',
    py_modules=['wonton'],
    install_requires=[
        'gevent>=1.0',
        'apache-libcloud>=0.13.2'
    ],
    entry_points={
        'console_scripts': [
            'wonton=wonton:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ]
)
