# -*- coding: utf-8 -*-
from AccessControl.Permissions import add_user_folders
from Products.PluggableAuthService import PluggableAuthService
from collective.impersonator.plugins import impersonator

PluggableAuthService.registerMultiPlugin(
    impersonator.ImpersonatorPlugin.meta_type
)


def initialize(context):
    context.registerClass(
        impersonator.ImpersonatorPlugin,
        permission=add_user_folders,
        constructors=(
            impersonator.manage_addImpersonatorPluginForm,
            impersonator.manage_addImpersonatorPlugin
        ),
        visibility=None
    )
