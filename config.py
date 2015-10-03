#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

from atlassian import config
from main import create_workflow

__version__ = '0.0.1'


def main(wf):
    wf.logger.setLevel(logging.ERROR)
    wf.logger.debug('Args: %s', wf.args)

    for issue in config.Config(wf).process():
        print '{subtitle}: {title}'.format(**issue)

if __name__ == '__main__':
    sys.exit(create_workflow().run(main))
