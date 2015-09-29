#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from workflow import Workflow

__version__ = '0.0.1'


def load_issues():
    args = wf.args

    from jira import JIRA

    jira = JIRA(
        server=args[0],
        basic_auth=args[1:3],
        get_server_info=False
    )

    return map(
        lambda issue: {
            'title': issue.fields.summary,
            'subtitle': issue.key,
            'arg': '{0}: {1}'.format(issue.key, issue.fields.summary),
            'copytext': '{0}: {1}'.format(issue.key, issue.fields.summary)
        },
        jira.search_issues(
            'filter={0}'.format(args[3]), fields=('key', 'summary'))
    )


def key_for_issue(issue):
    return '{} {}'.format(issue['title'], issue['subtitle'])


def main(wf):
    wf.logger.debug('Args: %s', wf.args)

    issues = wf.cached_data('issues', load_issues, max_age=30)
    
    wf.logger.debug(issues)

    query = None
    if len(wf.args) > 4:
        query = wf.args[4]

    if query:  # Only call `filter()` if there's a `query`
        plans = wf.filter(query, issues, key_for_issue)

    for issue in issues:
        wf.add_item(**issue)

    # Send output to Alfred
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(
        libraries=[
            'lib/jira-0.50-py2.7.egg',
            'lib/requests-2.7.0-py2.7.egg'
        ]
        # update_settings={
        #    'github_slug': 'resamsel/alfred-jira-workflow',
        #    'version': __version__
        #}
    )
    sys.exit(wf.run(main))
