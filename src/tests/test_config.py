# -*- coding: utf-8 -*-

import unittest
import logging

from atlassian import config


class MockWorkflow(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data = {}
        self.key_store = {}

    def save_password(self, key, value):
        self.key_store[key] = value

    def get_password(self, key):
        return self.key_store.get(key, None)

    def store_data(self, key, value):
        self.data[key] = value

    def stored_data(self, key):
        return self.data.get(key, None)


class ConfigTestCase(unittest.TestCase):
    def test_config(self):
        """Tests the config.Config class"""

        wf = MockWorkflow()

        self.assertIsNone(config.Config(None).wf)

        cfg = config.Config(wf)

        self.assertIsNotNone(cfg.wf)

        cfg.set_property(config.KEY_JIRA_SERVER, 'a')
        self.assertEqual('a', cfg.wf.stored_data(config.KEY_JIRA_SERVER))

        cfg.set_property(config.KEY_PASSWORD, 'b')
        self.assertIsNone(cfg.wf.stored_data(config.KEY_PASSWORD))
        self.assertEqual('b', cfg.wf.get_password(config.KEY_PASSWORD))
