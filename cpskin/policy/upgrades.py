from Products.CMFCore.utils import getToolByName
import logging


def delete_multilingualbehavior(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')

    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile(
        'profile-plone.multilingualbehavior:uninstall', purge_old=False)
    logger.info('plone.multilingualbehavior deleted')


def install_collective_atomrss(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')

    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile(
        'profile-collective.atomrss:default')
    logger.info('collective.atomrss installed')
