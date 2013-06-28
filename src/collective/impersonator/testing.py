# -*- coding: utf-8 -*-

from plone.app.testing import (
    FunctionalTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
    TEST_USER_ID,
    applyProfile,
    setRoles
)
from plone.testing import z2


class ImpersonatorLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.impersonator
        self.loadZCML(package=collective.impersonator)
        z2.installProduct(app, 'collective.impersonator')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.impersonator:default')

        from plone import api
        setRoles(portal, TEST_USER_ID, ['Manager'])
        api.user.create(email='manager@example.com', username='manager',
                        password='manager', roles=('Manager',))
        api.user.create(email='member@example.com', username='member',
                        password='member', roles=('Member',))

IMPERSONATOR_FIXTURE = ImpersonatorLayer()

IMPERSONATOR_ROBOT_TESTING = FunctionalTesting(
    bases=(IMPERSONATOR_FIXTURE, z2.ZSERVER_FIXTURE),
    name='Impersonator:Robot'
)
