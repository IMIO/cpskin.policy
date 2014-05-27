# -*- coding: utf-8 -*-
from Products.ATContentTypes.lib import constraintypes
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from plone import api
from plone.contentrules.engine.interfaces import IRuleStorage
from zope.component import getUtility
import logging



logger = logging.getLogger('cpskin.policy')


def publishContent(wftool, content):
    if wftool.getInfoFor(content, 'review_state') != 'published':
        actions = [a.get('id') for a in wftool.listActions(object=content)]
        # we need to handle both workflows
        if 'publish_and_hide' in actions:
            wftool.doActionFor(content, 'publish_and_hide')
        elif 'publish' in actions:
            wftool.doActionFor(content, 'publish')


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
                 folder_name='actualites',
                 index=review_index,
                 operator=review_operator,
                 value=review_states)
    setCriterion(portal=portal,
                 folder_name='evenements',
                 index=review_index,
                 operator=review_operator,
                 value=review_states)

    # expires
    not_expired_index = 'expires'
    not_expired_operator = 'plone.app.querystring.operation.date.afterToday'

    setCriterion(portal=portal,
                 folder_name='actualites',
                 index=not_expired_index,
                 operator=not_expired_operator)
    setCriterion(portal=portal,
                 folder_name='evenements',
                 index=not_expired_index,
                 operator=not_expired_operator)

    renameIndexhtml(portal)
    portal.setLayout('folderview')


def renameIndexhtml(portal):
    if portal.hasObject('index_html'):
        # Should be deteled
        api.content.rename(obj=portal['index_html'], new_id='index_html.old')



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
                 folder_name='actualites',
                 index=review_index,
                 operator=review_operator,
                 value=review_state)
    setCriterion(portal=portal,
                 folder_name='evenements',
                 index=review_index,
                 operator=review_operator,
                 value=review_state)


def createEventsAndNews(portal):
    """
    Inspired by Products.CMFPlone.setuphandlers
    """
    existing = portal.keys()
    language = portal.Language()
    wftool = getToolByName(portal, "portal_workflow")
    actu_folder = getattr(portal, 'actualites')
    events_folder = getattr(portal, 'evenements')
    # News topic
    if actu_folder:
        actu_folder.title = u'Actualités'
        actu_folder.description = 'Actualités du site'
        _createObjectByType('Collection', portal.actualites, id='index',
                   title=actu_folder.title, description=actu_folder.description)

        folder = portal.actualites
        folder.setConstrainTypesMode(constraintypes.ENABLED)
        folder.setLocallyAllowedTypes(['News Item'])
        folder.setImmediatelyAddableTypes(['News Item'])
        folder.setDefaultPage('index')
        folder.unmarkCreationFlag()
        folder.setLanguage(language)
        publishContent(wftool, folder)

        topic = portal.actualites.index
        topic.setLanguage(language)

        query = [{'i': 'portal_type',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': ['News Item']},
                 {'i': 'review_state',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': ['published']}]
        topic.setQuery(query)

        topic.setSort_on('effective')
        topic.setSort_reversed(True)
        topic.setLayout('folder_summary_view')
        topic.unmarkCreationFlag()
        publishContent(wftool, topic)

    # Events topic
    if events_folder:
        events_folder.title = 'Événements'
        events_folder.description = 'Événements du site'
        _createObjectByType('Collection', portal.evenements, id='index',
                            title=events_folder.title,
                            description=events_folder.description)

        folder = portal.evenements
        folder.setConstrainTypesMode(constraintypes.ENABLED)
        folder.setLocallyAllowedTypes(['Event'])
        folder.setImmediatelyAddableTypes(['Event'])
        folder.setDefaultPage('index')
        folder.unmarkCreationFlag()
        folder.setLanguage(language)
        publishContent(wftool, folder)

        topic = folder.index
        topic.unmarkCreationFlag()
        topic.setLanguage(language)

        query = [{'i': 'portal_type',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': ['Event']},
                 {'i': 'start',
                  'o': 'plone.app.querystring.operation.date.afterToday',
                  'v': ''},
                 {'i': 'review_state',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': ['published']}]
        topic.setQuery(query)
        topic.setSort_on('start')
        publishContent(wftool, topic)


def migrateTopicIds(portal):
    pc = getToolByName(portal, 'portal_catalog')
    for brainTopic in pc(portal_type='Topic'):
        topic = brainTopic.getObject()
        topic_parent = topic.aq_parent
        api.content.delete(obj=topic)
        if topic_parent.getId() == 'news':
            api.content.rename(obj=topic_parent, new_id='actualites')
        if topic_parent.getId() == 'events':
            api.content.rename(obj=topic_parent, new_id='evenements')


def setCriterion(portal, folder_name, index, operator, value=None):
    """
    Change existing criterion to collection, or add a new one
    """
    folder = getattr(portal, folder_name, None)
    if folder and hasattr(folder, 'index'):
        collection = folder.index
        if not hasattr(collection, 'query'):
            migrateTopicIds(portal)
            createEventsAndNews(portal)
            folder = getattr(portal, folder_name, None)
            collection = folder.index

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
