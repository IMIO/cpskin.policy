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

    # review_state
    review_index = 'review_state'
    review_operator = 'plone.app.querystring.operation.selection.is'
    review_states = ['published_and_hidden', 'published_and_shown']

    setCriterion(portal=portal,
                 folder_name='news',
                 index=review_index,
                 operator=review_operator,
                 value=review_states)
    setCriterion(portal=portal,
                 folder_name='events',
                 index=review_index,
                 operator=review_operator,
                 value=review_states)

    # expires
    not_expired_index = 'expires'
    not_expired_operator = 'plone.app.querystring.operation.date.afterToday'

    setCriterion(portal=portal,
                 folder_name='news',
                 index=not_expired_index,
                 operator=not_expired_operator)
    setCriterion(portal=portal,
                 folder_name='events',
                 index=not_expired_index,
                 operator=not_expired_operator)


def uninstallPolicy(context):
    if context.readDataFile('cpskin.policy-uninstall.txt') is None:
        return

    logger.info('Uninstalling policy')
    portal = context.getSite()
    deleteContentRules(portal)

    review_index = 'review_state'
    review_operator = 'plone.app.querystring.operation.selection.is'
    review_state = ['published']

    setCriterion(portal=portal,
                 folder_name='news',
                 index=review_index,
                 operator=review_operator,
                 value=review_state)
    setCriterion(portal=portal,
                 folder_name='events',
                 index=review_index,
                 operator=review_operator,
                 value=review_state)


def setCriterion(portal, folder_name, index, operator, value=None):
    """
    Change existing criterion to collection, or add a new one
    """
    folder = getattr(portal, folder_name, None)
    if folder and hasattr(folder, 'aggregator'):
        collection = folder.aggregator
        queries = collection.query

        # Remove existing query, usefull for reinstalling too
        for query in queries[:]:
            if query['i'] == index:
                queries.remove(query)

        # Create new query
        new_query = {'i': index,
                     'o': operator}
        if value is not None:
            new_query['v'] = value

        queries.append(new_query)

        collection.setQuery(queries)


def deleteContentRules(portal):
    storage = getUtility(IRuleStorage)
    if 'citizen-move-event' in storage:
        del storage['citizen-move-event']
    if 'citizen-reject-event' in storage:
        del storage['citizen-reject-event']
