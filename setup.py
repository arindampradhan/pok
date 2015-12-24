#!/usr/bin/env python
import p
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



setup(
    name='Pok',
    description='Manage your pocket from terminal.',
    long_description=open('README.md').read(),
    classifiers=[],
    package_data={'license': ['LICENSE.txt']},
    include_package_data=True,
    version=p.__version__,
    author=p.__author__,
    author_email=p.__author_email__,
    maintainer=p.__maintainer__,
    maintainer_email=p.__maintainer_email__,
    url=p.__url__,
    download_url = 'https://github.com/arindampradhan/pok/archive/v0.1.0.tar.gz',
    license='MIT License',
    install_requires=[
        "requests",
        "docopt",
    ],
    keywords = ['pocket', 'cli', 'terminal'],
    packages=['p'],
    entry_points={
        'console_scripts': [
            'pok = p.poc:main',
        ]
    },
)
