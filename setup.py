from setuptools import setup

requires = [ 
    'getopt',
    'os',
    'requests',
    'urlparse',
    'yaml',
    'CheckableString'
]

setup(
    name = 'wsync',
    version = '0.0.7',
    description = 'A small Python utility for synchronizing a local folder '\
    'with a remote web repository',
    py_modules = [ 'wsync' ],
    author = 'Roberto Reale',
    author_email = 'roberto.reale82@gmail.com',
    url = 'https://github.com/roberto-reale/wsync',
    keywords = [ 'wsync', 'sync', 'http', 'https', 'web' ],
)
