import unittest2 as unittest

from plone.app.testing import applyProfile

from cpskin.policy.testing import CPSKIN_POLICY_INTEGRATION_TESTING


class TestProfiles(unittest.TestCase):

    layer = CPSKIN_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_profiles(self):
        applyProfile(self.portal, 'cpskin.policy:members-configuration')
        applyProfile(self.portal, 'cpskin.policy:uninstall')
        applyProfile(self.portal, 'cpskin.policy:default')
