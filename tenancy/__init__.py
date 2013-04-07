from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured


__version__ = (0, 0, 2, 'dev')


def get_tenant_model(origin=None):
    from django.db.models import get_model
    from .models import AbstractTenant
    from .settings import TENANT_MODEL

    app_label, object_name = TENANT_MODEL.split('.')
    model_name = object_name.lower()
    seed_cache = origin is None
    only_installed = (origin != app_label)
    tenant_model = get_model(
        app_label, model_name,
        seed_cache=seed_cache, only_installed=only_installed
    )
    if tenant_model is None:
        raise ImproperlyConfigured(
            "TENANCY_TENANT_MODEL refers to model '%s.%s' that has not "
            "been installed" % (app_label, object_name)
        )
    elif not issubclass(tenant_model, AbstractTenant):
        raise ImproperlyConfigured(
            "TENANCY_TENANT_MODEL refers to models '%s.%s' which is not a "
            "subclass of 'tenancy.AbstractTenant'" % (app_label, object_name))
    return tenant_model