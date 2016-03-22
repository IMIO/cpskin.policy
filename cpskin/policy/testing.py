# -*- coding: utf-8 -*-
from plone.testing import z2
from plone.app.testing import applyProfile
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
import cpskin.policy


class CpskinPolicyPloneWithPackageLayer(PloneWithPackageLayer):
    """
    """

    def setUpPloneSite(self, portal):
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        applyProfile(portal, 'cpskin.policy:testing')


CPSKIN_POLICY_FIXTURE = CpskinPolicyPloneWithPackageLayer(
    name='CPSKIN_POLICY_FIXTURE',
    zcml_filename='testing.zcml',
    zcml_package=cpskin.policy,
    additional_z2_products=('Products.PasswordStrength',),
    gs_profile_id='cpskin.policy:testing')

CPSKIN_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CPSKIN_POLICY_FIXTURE,),
    name="CPSkinPolicy:Integration")

CPSKIN_POLICY_ROBOT_TESTING = FunctionalTesting(
    bases=(CPSKIN_POLICY_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="cpskin.policy:Robot")
