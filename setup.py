from setuptools import find_packages, setup

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE.txt') as f:
    license = f.read()

setup(
    name = 'wsync',
    version = '0.9.6',
    description = 'A small utility for synchronizing a local folder '\
    'with a remote web repository',
    long_description = readme,
    packages=find_packages(exclude=('tests', 'docs')),
    author = 'Roberto Reale',
    author_email = 'roberto@reale.me',
    url = 'https://github.com/reale/wsync',
    keywords = [ 'wsync', 'sync', 'http', 'https', 'web' ],
    install_requires = [ 
        'requests',
        'PyYAML',
        'alphabet'
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
