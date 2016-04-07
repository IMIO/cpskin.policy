# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging
import transaction
from cpskin.policy.setuphandlers import add_cookiescuttr
from plone import api


def delete_multilingualbehavior(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')

    portal = api.portal.get()
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


def install_collective_cookiecuttr(context, logger=None):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-collective.cookiecuttr:default')
    portal = api.portal.get()
    add_cookiescuttr(portal)


def clean_registries(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy.upgrades')
    portal = api.portal.get()
    logger.info('Cleaning registries...')

    jstool = portal.portal_javascripts
    jstool.cookResources()
    logger.info('portal_javascripts has been cleaned!')

    csstool = portal.portal_css
    csstool.cookResources()
    logger.info('portal_css has been cleaned!')
    ps = portal.portal_setup
    # clean portal_setup
    for stepId in ps.getSortedImportSteps():
        stepMetadata = ps.getImportStepMetadata(stepId)
        # remove invalid steps
        if stepMetadata['invalid']:
            logger.info('Removing %s step from portal_setup' % stepId)
            ps._import_registry.unregisterStep(stepId)
    logger.info('portal_setup has been cleaned!')

    logger.info('Registries have been cleaned!')


def install_image_cropping(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')

    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile(
        'profile-plone.app.imagecropping:default')
    logger.info('plone.app.imagecropping installed')


def set_allowed_sizes(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('cpskin.policy')

    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(
        'profile-cpskin.policy:default', 'propertiestool')
    logger.info('cpskin.policy updated')
    clean_registries(context)
