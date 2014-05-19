import unittest2 as unittest

from cpskin.policy.testing import CPSKIN_POLICY_INTEGRATION_TESTING


class TestProfiles(unittest.TestCase):

    layer = CPSKIN_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_empty(self):
        pass
