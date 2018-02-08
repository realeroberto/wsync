from setuptools import setup

setup(
    name = 'wsync',
    version = '0.9',
    description = 'A small Python utility for synchronizing a local folder '\
    'with a remote web repository',
    packages = [ 'wsync' ],
    author = 'Roberto Reale',
    author_email = 'rober.reale@gmail.com',
    url = 'https://github.com/robertoreale/wsync',
    keywords = [ 'wsync', 'sync', 'http', 'https', 'web' ],
    install_requires = [ 
        'requests',
        'PyYAML',
        'pyCheckableString'
    ],
    test_suite = 'nose.collector',
    tests_require = ['nose'],
    entry_points={
        'console_scripts': [
            'wsync = wsync.__main__:main'
            ]
        },
)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
