# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging
import transaction
from zope.component.hooks import getSite


def delete_multilingualbehavior(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')

    portal = getSite()
    sm = portal.getSiteManager()

    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-plone.multilingualbehavior:uninstall')

    # Check is PAM is installed, if not remore plone.multilingual
    portal_quickinstaller = getToolByName(context, 'portal_quickinstaller')
    portal_quickinstaller.uninstallProducts(['plone.multilingualbehavior'])
    logger.info('plone.multilingualbehavior uninstalled')

    portal_setup.runAllImportStepsFromProfile('profile-plone.multilingual:uninstall')
    portal_quickinstaller.uninstallProducts(['plone.multilingual'])
    logger.info('plone.multilingual uninstalled')

    subscribers = sm.adapters._subscribers
    for i, sub in enumerate(subscribers):
        for key in sub.keys():
            if 'multilingual' in str(key):
                del subscribers[i][key]
                logger.info("Deleted {0} subscriber".format(key))
    sm.adapters._subscribers = subscribers

    transaction.commit()
    app = portal.restrictedTraverse('/')
    app._p_jar.sync()


def install_collective_atomrss(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')

    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile(
        'profile-collective.atomrss:default')
    logger.info('collective.atomrss installed')
