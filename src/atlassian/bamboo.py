# -*- coding: utf-8 -*-

import logging
import re

from workflow import web

from config import KEY_BAMBOO_SERVER, KEY_BAMBOO_PROJECT, KEY_USERNAME, \
    KEY_PASSWORD

__version__ = '0.0.1'

BRANCH_PATTERN = re.compile('\d')


def result_key(result):
    return result['key']


class Results(object):
    def __init__(self, wf, branch_key):
        self.wf = wf
        self.branch_key = branch_key

    def load(self):
        wf = self.wf

        response = web.get(
            '{0}/rest/api/latest/result/{1}.json'.format(
                wf.stored_data(KEY_BAMBOO_SERVER),
                self.branch_key
            ),
            auth=(wf.stored_data(KEY_USERNAME), wf.get_password(KEY_PASSWORD))
        ).json()

        return map(
            lambda result: {
                'title': result_key(result),
                'subtitle': result['buildState'],
                'arg': result_key(result),
                'copytext': result_key(result),
                'autocomplete': result_key(result),
                'valid': True
            },
            response['results']['result']
        )


def branch_key(plan_key, branch):
    return '{0}-{1}'.format(plan_key, branch['shortKey'])


class Branches(object):
    def __init__(self, wf, plan_key):
        self.wf = wf
        self.plan_key = plan_key

    def load(self):
        wf = self.wf
        project = wf.stored_data(KEY_BAMBOO_PROJECT)

        response = web.get(
            '{0}/rest/api/latest/plan/{1}/branch.json'.format(
                wf.stored_data(KEY_BAMBOO_SERVER),
                self.plan_key
            ),
            auth=(wf.stored_data(KEY_USERNAME), wf.get_password(KEY_PASSWORD))
        ).json()

        return map(
            lambda branch: {
                'title': branch_key(project, branch),
                'subtitle': branch['shortName'],
                'arg': branch_key(project, branch),
                'copytext': branch_key(project, branch),
                'autocomplete': branch_key(project, branch),
                'valid': True
            },
            response['branches']['branch']
        )


class Plans(object):
    def __init__(self, wf):
        self.wf = wf

    def load(self):
        wf = self.wf

        response = web.get(
            '{0}/rest/api/latest/project/{1}.json?expand=plans'.format(
                wf.stored_data(KEY_BAMBOO_SERVER),
                wf.stored_data(KEY_BAMBOO_PROJECT)
            ),
            auth=(wf.stored_data(KEY_USERNAME), wf.get_password(KEY_PASSWORD))
        ).json()

        return map(
            lambda plan: {
                'title': plan['key'],
                'subtitle': plan['name'],
                'arg': plan['key'],
                'copytext': '{0}: {1}'.format(plan['key'], plan['name']),
                'autocomplete': plan['key'],
                'valid': True
            },
            response['plans']['plan']
        )


def key(item):
    return u'{} {}'.format(item['title'], item['subtitle'])


def get_plans(wf):
    if len(wf.args) > 0 and BRANCH_PATTERN.search(wf.args[0]):
        # Load branches instead of plans
        query = wf.args[0]
        branch_key = '-'.join(query.split('-')[0:2])

        results = wf.cached_data(
            'results-{0}'.format(branch_key),
            Results(wf, branch_key).load,
            max_age=30
        )

        results = wf.filter(query, results, key)

        return sorted(
            results,
            key=lambda r: int(r['title'].split('-')[2]),
            reverse=True
        )

    plans = wf.cached_data('plans', Plans(wf).load, max_age=30)
    # plans = Plans(wf).load()

    query = None
    if len(wf.args) > 0:
        query = wf.args[0]

    if query:  # Only call `filter()` if there's a `query`
        plans = wf.filter(query, plans, key)

    if len(plans) == 1:
        # Load branches of plan
        return wf.cached_data(
            'branches', Branches(wf, plans[0]['title']).load, max_age=30)

    return plans


def main(wf):
    wf.logger.setLevel(logging.ERROR)
    wf.logger.debug('Args: %s', wf.args)

    for plan in get_plans(wf):
        print plan['title']
