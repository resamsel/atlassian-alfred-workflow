#!/usr/bin/env python
# -*- coding: utf-8 -*-

KEY_JIRA_SERVER = 'jira-server'
KEY_BAMBOO_SERVER = 'bamboo-server'
KEY_USERNAME = 'username'
KEY_PASSWORD = 'password'
KEY_JIRA_FILTER = 'jira-filter'
KEY_BAMBOO_PROJECT = 'bamboo-project'

KEYS = (
    KEY_JIRA_SERVER, KEY_BAMBOO_SERVER, KEY_USERNAME, KEY_PASSWORD,
    KEY_JIRA_FILTER, KEY_BAMBOO_PROJECT
)


def key(item):
    return '{title} {subtitle}'.format(**item)


class Config(object):
    def __init__(self, wf):
        self.wf = wf

    def set_property(self, property, value):
        wf = self.wf

        if property == KEY_PASSWORD:
            wf.logger.debug('Saving password')
            wf.save_password(KEY_PASSWORD, value)
        else:
            wf.logger.debug('Storing data: %s=%s', property, value)
            wf.store_data(property, value)

    def get_items(self, value):
        wf = self.wf
        items = []

        for key in KEYS:
            wf.logger.debug('Processing key %s', key)

            autocomplete = ''
            if value is None:
                autocomplete = '{0} '.format(key)

            if key == KEY_PASSWORD:
                items.append({
                    # Get the password, but don't display its value
                    'title': {None: ''}.get(
                        wf.get_password(KEY_PASSWORD),
                        '********'
                    ),
                    'subtitle': key,
                    'autocomplete': autocomplete
                })
            else:
                items.append({
                    'title': wf.stored_data(key),
                    'subtitle': key,
                    'autocomplete': autocomplete
                })

        return items

    def process(self):
        wf = self.wf

        property = None
        if len(wf.args) > 0:
            property = wf.args[0]
        value = None
        if len(wf.args) > 1:
            value = wf.args[1]

        if value is not None and value is not '':
            if property in KEYS:
                self.set_property(property, value)

        items = self.get_items(value)

        if property is not None:
            return wf.filter(property, items, key)

        return items
