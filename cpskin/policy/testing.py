from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting

import cpskin.policy


CPSKIN_POLICY_FIXTURE = PloneWithPackageLayer(
    name="CPSKIN_POLICY_FIXTURE",
    zcml_filename="testing.zcml",
    zcml_package=cpskin.policy,
    gs_profile_id="cpskin.policy:testing")

CPSKIN_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_POLICY_FIXTURE,),
    name="CPSkinPolicy:Integration")
