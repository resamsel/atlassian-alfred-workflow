#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name="atlassian-alfred-workflow",
    version='0.0.1',
    author="René Samselnig",
    author_email="me@resamsel.com",
    description="Tools for Atlassian's suite (Jira, Bamboo)",
    keywords="atlassian jira bamboo plans issues branches results",

    packages=find_packages(
        'src', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    package_dir={'': 'src'},

    test_suite='tests',

    tests_require=[
        'flake8>=2.2.5',
        'pep8-naming>=0.2.2',
        'flake8-todo>=0.3',
        'nose>=1.3.4',
        'coverage>=3.7.1',
        'pylint>=1.4.3'
    ],

    entry_points={
        'console_scripts': [
            'awf-config = config:main',
            'awf-issues = jiraissues:main',
            'awf-plans = bambooplans:main'
        ]
    }
)
