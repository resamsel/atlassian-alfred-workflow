#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from atlassian import jira, create_workflow

__version__ = '0.0.1'


def main():
    create_workflow().run(jira.main)

if __name__ == '__main__':
    sys.exit(main())
