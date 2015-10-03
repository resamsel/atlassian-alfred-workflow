#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

from atlassian import bamboo
from main import create_workflow

__version__ = '0.0.1'


def main(wf):
    wf.logger.setLevel(logging.ERROR)
    wf.logger.debug('Args: %s', wf.args)

    for plan in bamboo.get_plans(wf):
        print plan['title']

if __name__ == '__main__':
    wf = create_workflow()
    sys.exit(wf.run(main))
