import os
from setuptools import setup

from testbed import __version__, __author__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

fpath = os.path.join(os.path.dirname(__file__), 'doc/Requirements.rst')

with open(fpath) as hdl:
    REQUIREMENTS = hdl.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='testbed',
    version=__version__,
    packages=['testbed'],
    scripts=["bin/tbd"],
    include_package_data=True,
    license='GPLv3',
    description='Comprehensive web-based test tracking software.',
    long_description=README,
    url='https://github.com/markleehamilton/testbed',
    author=__author__,
    author_email='mark.lee.hamilton@gmail.com',
    install_requires=REQUIREMENTS.split("\n"),
    data_files=[("/etc/testbed", [])],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Testbed',
        'Intended Audience :: Developers',
        'Intended Audience :: Managers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Utilities',
    ],
)
