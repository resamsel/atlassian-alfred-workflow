#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from workflow import Workflow

__version__ = '0.0.1'

ITEM_FORMAT = u"""    <item>
        <title>{summary}</title>
        <subtitle>{key}</subtitle>
        <arg>{key}: {summary}</arg>
        <text type="copy">{key}: {summary}</text>
    </item>"""


def main(wf):
    from jira import JIRA

    wf.logger.debug('Args: %s', wf.args)

    jira = JIRA(
        server=wf.args[0],
        basic_auth=wf.args[1:3],
        get_server_info=False
    )

    for issue in jira.search_issues(
            'filter={0}'.format(wf.args[3]), fields=('key', 'summary')):
        wf.add_item(
            unicode(issue.fields.summary),
            unicode(issue.key),
            arg=unicode(u'{key}: {summary}'.format(
                key=issue.key, summary=issue.fields.summary))
        )

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
