# -*- coding:utf-8 -*-
"""
App settings
"""
from django.conf import settings


MODELS_CONFIG = getattr(settings, "FOO_MODELS_CONFIG", "models.yaml")
