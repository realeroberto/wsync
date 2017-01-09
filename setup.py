from setuptools import setup

setup(
    name = 'wsync',
    version = '0.0.8.1',
    description = 'A small Python utility for synchronizing a local folder '\
    'with a remote web repository',
    py_modules = [ 'wsync' ],
    author = 'Roberto Reale',
    author_email = 'roberto.reale@linux.com',
    url = 'https://github.com/robertoreale/wsync',
    keywords = [ 'wsync', 'sync', 'http', 'https', 'web' ],
    install_requires = [ 
    'requests',
    'PyYAML',
    'pyCheckableString'
    ]
)
