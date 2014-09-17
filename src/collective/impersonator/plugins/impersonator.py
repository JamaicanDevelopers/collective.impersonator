# -*- coding: utf-8 -*-
from plone import api

from AccessControl.SecurityInfo import ClassSecurityInfo

from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.PluggableAuthService.interfaces.plugins import (
    IAuthenticationPlugin,
)
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements

from collective.impersonator.interfaces import IImpersonatorPlugin

manage_addImpersonatorPluginForm = PageTemplateFile('impersonator', globals())


def manage_addImpersonatorPlugin(dispatcher, id, title=None, path='/',
                                 REQUEST=None):
    sp = ImpersonatorPlugin(id, title=title)
    dispatcher._setObject(id, sp)

    if REQUEST is not None:
        REQUEST.response.redirect(
            '%s/manage_workspace?'
            'manage_tabs_message=Impersonator+authentication+plugin+created.' %
            dispatcher.absolute_url()
        )


class ImpersonatorPlugin(BasePlugin):
    meta_type = 'Impersonator Authentication Plugin'
    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    # IAuthenticationPlugin implementation
    def authenticateCredentials(self, credentials):
        # Fetch active request via Acquisition
        request = getattr(self, 'REQUEST', None)
        if not request:
            return None

        # Read X-impersonate-header
        x_impersonate = request.getHeader('X-impersonate', None)
        if not x_impersonate:
            return None

        x_impersonate_user = api.user.get(username=x_impersonate)
        if not x_impersonate_user:
            return None

        # Fetch plone.session plugin via Acquisition
        session = getattr(self, 'session', None)
        if not session:
            return None

        id_login_tuple = self.session.authenticateCredentials(credentials)
        if not id_login_tuple:
            return None

        permissions = api.user.get_permissions(username=id_login_tuple[0])
        try:
            if not permissions.get('Manage portal'):
                return None
        except AttributeError:
            return None

        return (x_impersonate_user.getId(),
                x_impersonate_user.getUser().getName())

classImplements(ImpersonatorPlugin, IImpersonatorPlugin,
                IAuthenticationPlugin)
