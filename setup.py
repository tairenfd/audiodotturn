import os
from setuptools import setup, find_packages
import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

APP_NAME = 'audiodotturn'

setup(
    name=APP_NAME,
    version=get_version("src/__init__.py"),
    description='A tool for formatting and organizing music files.',
    author='tairenfd',
    author_email='tairenfd@mailbox.org',
    url='https://github.com/tairenfd/AudioDotTurn',
    packages=find_packages(),
    package_dir={},
    install_requires=[
        'rich>=13.3.1',
        'markdown-it-py>=2.2.0',
        'mdurl>=0.1.2',
        'Pygments>=2.14.0'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'audiodotturn=src.cli_runner:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities'
    ],
)