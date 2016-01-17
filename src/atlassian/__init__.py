# -*- coding: utf-8 -*-

import logging

from workflow import Workflow

logger = logging.getLogger(__name__)


def init_logging():
    logging.basicConfig(
        filename='/usr/local/var/log/atlassian.log',
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")


def create_workflow():
    init_logging()
    logger.debug('Creating workflow')
    return Workflow(
        # update_settings={
        #    'github_slug': 'resamsel/alfred-jira-workflow',
        #    'version': __version__
        # }
    )
