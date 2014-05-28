import unittest2 as unittest

from plone.app.testing import applyProfile

from cpskin.policy.testing import CPSKIN_POLICY_INTEGRATION_TESTING


class TestProfiles(unittest.TestCase):

    layer = CPSKIN_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_uninstall(self):
        applyProfile(self.portal, 'cpskin.policy:uninstall')

    def test_reinstall(self):
        applyProfile(self.portal, 'cpskin.policy:uninstall')
        applyProfile(self.portal, 'cpskin.policy:default')

    def test_uninstall_with_members(self):
        applyProfile(self.portal, 'cpskin.policy:members-configuration')
        applyProfile(self.portal, 'cpskin.policy:uninstall')
