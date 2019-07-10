import os

from setuptools import find_packages
from setuptools import setup
from sixlowpan_parser import __version__

# Dependencies, versioned against what would be found on the ubuntu distro
install_requires = [
    'scapy',
    'click'
]

setup(
    name='sixlowpan_parser',
    version=__version__,
    packages=find_packages(exclude=['tests*', 'docs*']),
    package_data={
        'sixlowpan_parser': [
            'samples/*.pcap',
        ],
    },
    data_files=[],  # system files?
    install_requires=install_requires,
    author='YuSheng Tseng',
    author_email='chester@cwyark.me',
    maintainer='YuSheng Tseng',
    keywords=['6lowpan', 'pcap', 'parser'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License 2.0',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ],
    description="6lowpan parser to vcs files",
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'sixlowpan-parser=sixlowpan_parser.cli:main',
        ],
    },
)
