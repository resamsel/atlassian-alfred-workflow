#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from atlassian import bamboo, create_workflow

__version__ = '0.0.1'


def main():
    create_workflow().run(bamboo.main)

if __name__ == '__main__':
    sys.exit(main())
