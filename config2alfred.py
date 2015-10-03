#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from atlassian import config
from main import create_workflow

__version__ = '0.0.1'


def main(wf):
    wf.logger.debug('Args: %s', wf.args)

    for item in config.Config(wf).process():
        wf.add_item(**item)

    # Send output to Alfred
    wf.send_feedback()

if __name__ == '__main__':
    sys.exit(create_workflow().run(main))
