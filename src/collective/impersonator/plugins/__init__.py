# -*- coding: utf-8 -*-
from Acquisition import aq_base

from zope.component import (
    getUtility,
    getSiteManager
)

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

from Products.PluggableAuthService.interfaces.plugins import (
    IAuthenticationPlugin
)

from Products.PlonePAS.Extensions.Install import activatePluginInterfaces

from collective.impersonator.interfaces import IImpersonatorPlugin


def configureImpersonatorPlugin(context):
    if context.readDataFile("collective.impersonator.txt") is None:
        return  # not our profile

    site = getUtility(ISiteRoot)
    pas = getToolByName(site, "acl_users")

    if "impersonator" not in pas.objectIds():
        factory = pas.manage_addProduct["collective.impersonator"]
        factory.manage_addImpersonatorPlugin(
            "impersonator",
            "Impersonator Authentication Plugin"
        )

    activatePluginInterfaces(site, "impersonator")

    # Make plugin the first in order:
    try:
        for i in range(len(pas.plugins.listPluginIds(IAuthenticationPlugin))):
            pas.plugins.movePluginsUp(IAuthenticationPlugin, ("impersonator",))
    except:
        pass

    sm = getSiteManager()
    obj = pas["impersonator"]
    sm.registerUtility(aq_base(obj), IImpersonatorPlugin)
