# -*- coding: utf-8 -*-
import logging
from zope.component import getUtility
from plone.contentrules.engine.interfaces import IRuleStorage

logger = logging.getLogger('cpskin.policy')


def installPolicy(context):
    if context.readDataFile('cpskin.policy-default.txt') is None:
        return

    logger.info('Installing policy')
    portal = context.getSite()
    states = ['published_and_hidden', 'published_and_shown']
    setReviewStateCriterion(portal, 'news', states)
    setReviewStateCriterion(portal, 'events', states)
    setNotExpiredCriterion(portal, 'news')
    setNotExpiredCriterion(portal, 'events')


def uninstallPolicy(context):
    if context.readDataFile('cpskin.policy-uninstall.txt') is None:
        return

    logger.info('Uninstalling policy')
    portal = context.getSite()
    deleteContentRules(portal)
    setReviewStateCriterion(portal, 'news', ['published'])
    setReviewStateCriterion(portal, 'events', ['published'])


def setReviewStateCriterion(portal, folderName, values):
    """
    Change criterion on review_state by selection_list
    (published_and_hidden and published_and_shown if installed)
    """
    folder = getattr(portal, folderName, None)
    if folder and hasattr(folder, 'aggregator'):
        collection = folder.aggregator
        queries = collection.query

        # Remove existing review state query
        for query in queries[:]:
            if query['i'] == 'review_state':
                queries.remove(query)

        # Create new review state query
        review_state_query = {'i': 'review_state',
                              'o': 'plone.app.querystring.operation.selection.is',
                              'v': values}
        queries.append(review_state_query)

        collection.setQuery(queries)


def setNotExpiredCriterion(portal, folderName):
    """
    Change criterion so expired items are not shown
    """
    folder = getattr(portal, folderName, None)
    if folder and hasattr(folder, 'aggregator'):
        collection = folder.aggregator
        queries = collection.query

        # If reinstall, remove it first
        for query in queries[:]:
            if query['i'] == 'expires':
                queries.remove(query)

        queries.append({'i': 'expires',
                        'o': 'plone.app.querystring.operation.date.afterToday'})
        collection.setQuery(queries)


def deleteContentRules(portal):
    storage = getUtility(IRuleStorage)
    if 'citizen-move-event' in storage:
        del storage['citizen-move-event']
    if 'citizen-reject-event' in storage:
        del storage['citizen-reject-event']
