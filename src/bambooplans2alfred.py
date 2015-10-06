#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from atlassian import bamboo, create_workflow

__version__ = '0.0.1'


def main(wf):
    wf.logger.debug('Args: %s', wf.args)

    for plan in bamboo.get_plans(wf):
        wf.add_item(**plan)

    # Send output to Alfred
    wf.send_feedback()

if __name__ == '__main__':
    wf = create_workflow()
    sys.exit(wf.run(main))
