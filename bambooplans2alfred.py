#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from workflow import Workflow
from workflow import web

__version__ = '0.0.1'


def load_plans():
    args = wf.args
    response = web.get(
        '{0}/rest/api/latest/result/{1}.json'.format(*args),
        auth=(args[2], args[3])
    ).json()

    return map(
        lambda plan: {
            'title': plan['key'],
            'subtitle': plan['plan']['name'],
            'arg': plan['key'],
            'copytext': '{0}: {1}'.format(plan['key'], plan['plan']['name'])
        },
        response['results']['result']
    )


def key_for_plan(plan):
    return '{} {}'.format(plan['title'], plan['subtitle'])


def main(wf):
    wf.logger.debug('Args: %s', wf.args)

    plans = wf.cached_data('plans', load_plans, max_age=30)
    
    wf.logger.debug(plans)

    query = None
    if len(wf.args) > 4:
        query = wf.args[4]

    if query:  # Only call `filter()` if there's a `query`
        plans = wf.filter(query, plans, key_for_plan)

    for plan in plans:
        wf.add_item(**plan)

    # Send output to Alfred
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(
        # update_settings={
        #    'github_slug': 'resamsel/atlassian-alfred-workflow',
        #    'version': __version__
        #}
    )
    sys.exit(wf.run(main))
