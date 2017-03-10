#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


INSTALL_REQUIRES = [
    'Click>=6.0',
    'Requests>=2.13.0',
    'beautifulsoup4>=4.5.3',
    'progressbar2',
    'selenium',
]

EXTRAS_REQUIRE = {
    # ...
}

if int(setuptools.__version__.split(".", 1)[0]) < 18:
    if sys.version_info[0:2] >= (3, 5):
        INSTALL_REQUIRES.append("aiohttp")
        INSTALL_REQUIRES.append("aiofiles")
else:
    EXTRAS_REQUIRE[":python_version>='3.5'"] = ["aiohttp", "aiofiles"]

setup(
    # ...
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
)


test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='ctdata_edsight_scraping_tool',
    version='0.1.0',
    description="Click based CLI for scraping CTSDE EdSight",
    long_description=readme + '\n\n' + history,
    author="Sasha Cuerda",
    author_email='scuerda@ctdata.org',
    url='https://github.com/scuerda/ctdata_edsight_scraping_tool',
    packages=[
        'ctdata_edsight_scraping_tool',
    ],
    package_dir={'ctdata_edsight_scraping_tool':
                 'ctdata_edsight_scraping_tool'},
    package_data={
      '': ['*.json']
    },
    entry_points={
        'console_scripts': [
            'edsight=ctdata_edsight_scraping_tool.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    license="MIT license",
    zip_safe=False,
    keywords='ctdata_edsight_scraping_tool',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
