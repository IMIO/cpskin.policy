import unittest2 as unittest

from cpskin.policy.interfaces import ICPSkinPolicyLayer
from cpskin.policy.testing import CPSKIN_POLICY_INTEGRATION_TESTING
from plone.app.testing import applyProfile
from plone.browserlayer.utils import registered_layers


class TestProfiles(unittest.TestCase):

    layer = CPSKIN_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_package_installed(self):
        self.assertIn(ICPSkinPolicyLayer, registered_layers(),
                      'Browserlayers appears not loaded')

    def test_uninstall(self):
        applyProfile(self.portal, 'cpskin.policy:uninstall')

    def test_reinstall(self):
        applyProfile(self.portal, 'cpskin.policy:uninstall')
        applyProfile(self.portal, 'cpskin.policy:default')

    def test_uninstall_with_members(self):
        applyProfile(self.portal, 'cpskin.policy:members-configuration')
        applyProfile(self.portal, 'cpskin.policy:uninstall')
