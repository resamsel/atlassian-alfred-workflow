# -*- coding: utf-8 -*-

import logging

from base64 import b64encode

from workflow import web

from config import KEY_JIRA_SERVER, KEY_USERNAME, KEY_PASSWORD, KEY_JIRA_FILTER
from config import get_password

__version__ = '0.0.1'

logger = logging.getLogger(__name__)


class Issues(object):
    def __init__(self, wf):
        self.wf = wf

    def load(self):
        wf = self.wf

        url = '{0}/rest/api/2/search'.format(wf.stored_data(KEY_JIRA_SERVER))
        params = {'jql': 'filter={0}'.format(wf.stored_data(KEY_JIRA_FILTER))}

        logger.debug('URL: %s, params: %s', url, params)

        wf.logger.debug('URL: %s, params: %s', url, params)

        response = web.get(
            url,
            params=params,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Basic {0}'.format(
                    b64encode('{0}:{1}'.format(
                        wf.stored_data(KEY_USERNAME),
                        get_password(wf, KEY_PASSWORD))))
            }
        ).json()

        # wf.logger.debug('Response: %s', response)

        return map(
            lambda issue: {
                'title': issue['fields']['summary'],
                'subtitle': issue['key'],
                'arg': u'{0}: {1}'.format(
                    issue['key'], issue['fields']['summary']),
                'copytext': u'{0}: {1}'.format(
                    issue['key'], issue['fields']['summary']),
                'valid': True
            },
            response['issues']
        )


def key_for_issue(issue):
    return u'{} {}'.format(issue['title'], issue['subtitle'])


def get_issues(wf):
    issues = wf.cached_data('issues', Issues(wf).load, max_age=30)

    query = None
    if len(wf.args) > 0:
        query = wf.args[0]

    if query:  # Only call `filter()` if there's a `query`
        issues = wf.filter(query, issues, key_for_issue)

    return issues


def main(wf):
    wf.logger.debug('Args: %s', wf.args)

    for issue in get_issues(wf):
        print u'{subtitle}: {title}'.format(**issue)
