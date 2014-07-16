from setuptools import setup

setup(
    name = 'wsync',
    version = '0.0.8',
    description = 'A small Python utility for synchronizing a local folder '\
    'with a remote web repository',
    py_modules = [ 'wsync' ],
    author = 'Roberto Reale',
    author_email = 'roberto.reale82@gmail.com',
    url = 'https://github.com/roberto-reale/wsync',
    keywords = [ 'wsync', 'sync', 'http', 'https', 'web' ],
    install_requires = [ 
    'requests',
    'PyYAML',
    'CheckableString'
    ]
)
