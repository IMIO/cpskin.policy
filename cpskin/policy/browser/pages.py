from zope.publisher.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api


class CookiesPage(BrowserView):

    index = ViewPageTemplateFile('templates/cookies.pt')

    def __init__(self, context, request):
        super(CookiesPage, self).__init__(context, request)
        portal = api.portal.get()
        self.site_id = portal.getId()
        self.city_name = self.site_id.capitalize()
