from zope.interface import implements

import Products.CMFPlone.interfaces
import Products.CMFQuickInstallerTool.interfaces


class HiddenProfiles(object):
    implements(Products.CMFPlone.interfaces.INonInstallable)

    def getNonInstallableProfiles(self):
        """Hides profiles from 'Add Plone site' form"""
        return [u'cpskin.core:default',
                u'cpskin.core:members-configuration',
                u'cpskin.core:uninstall',
                u'cpskin.workflow:default',
                u'cpskin.workflow:members-configuration',
                u'cpskin.workflow:uninstall']


class HiddenProducts(object):
    implements(Products.CMFQuickInstallerTool.interfaces.INonInstallable)

    def getNonInstallableProducts(self):
        """Hides profiles from QuickInstaller"""
        return [u'cpskin.core',
                u'cpskin.locales',
                u'cpskin.menu',
                u'cpskin.theme',
                u'cpskin.workflow']
