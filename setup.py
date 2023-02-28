from setuptools import setup, find_packages

setup(
    name='AudioDotTurn',
    version='0.1.0',
    description='A tool for formatting and organizing music files.',
    author='tairenfd',
    author_email='tairenfd@mailbox.org',
    url='https://github.com/tairenfd/AudioDotTurn',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},package_dir={'': 'src'},
    install_requires=[
        'rich>=13.3.1'
    ],
    entry_points={
        'console_scripts': [
            'audiodotturn=audiodotturn.main:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Topic :: Utilities'
    ]
)