# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from plone import api
from plone.app.contenttypes.migration import dxmigration
from plone.app.folder.utils import timer
from time import strftime
import logging

logger = logging.getLogger("cpskin.policy")


class FolderishTypesMigrationView(BrowserView):
    """ Installs collective.folderishtypes and migrate existing contents """

    def mklog(self):
        """ Helper to prepend a time stamp to the output """
        write = self.request.RESPONSE.write

        def log(msg, level="info"):
            if level == "warn":
                logger.warn(msg)
            else:
                logger.info(msg)
            msg = "{0} {1}\n".format(strftime("%d/%m/%Y - %H:%M:%S"), msg)
            write(msg)

        return log

    def install_folderish_types(self):
        portal_setup = api.portal.get_tool("portal_setup")
        portal_setup.runAllImportStepsFromProfile(
            "profile-collective.folderishtypes.dx:default"
        )

    def __call__(self):
        log = self.mklog()
        real = timer()

        self.install_folderish_types()
        log("collective.folderishtypes installed.")

        changed_base_classes = [
            "plone.app.contenttypes.content.Document",
            "plone.app.contenttypes.content.NewsItem",
            "plone.app.contenttypes.content.Event",
        ]

        catalog = api.portal.get_tool("portal_catalog")
        migrated = []
        not_migrated = []
        for brain in catalog():
            obj = brain.getObject()
            old_class_name = dxmigration.get_old_class_name_string(obj)
            if old_class_name in changed_base_classes:
                if dxmigration.migrate_base_class_to_new_class(
                    obj, migrate_to_folderish=True
                ):
                    migrated.append(obj)
                else:
                    not_migrated.append(obj)

        if migrated:
            log("{0} objects have been migrated.".format(len(migrated)))
        if not_migrated:
            log(
                "{0} objects have NOT been migrated.".format(len(not_migrated)),
                level="warn",
            )

        catalog.clearFindAndRebuild()
        log("Portal catalog has been rebuilt.")

        msg = "Processed folderish types migration in {0}.".format(real.next())
        log(msg)
