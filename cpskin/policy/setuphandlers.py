import logging

logger = logging.getLogger('cpskin.workflow')


def installPolicy(context):
    if context.readDataFile('cpskin.policy-default.txt') is None:
        return

    logger.info('Installing policy')
    portal = context.getSite()
    states = ['published_and_hidden', 'published_and_shown']
    setReviewStateCriterion(portal, 'news', states)
    setReviewStateCriterion(portal, 'events', states)


def setReviewStateCriterion(portal, folderName, values):
    """
    Change criterion on review_state by selection_list
    (published_and_hidden and published_and_shown if installed)
    """
    folder = getattr(portal, folderName, None)
    if folder and hasattr(folder, 'aggregator'):
        collection = folder.aggregator
        queries = collection.query
        for query in queries:
            if query['i'] == 'review_state':
                query['v'] = values
        collection.setQuery(queries)
