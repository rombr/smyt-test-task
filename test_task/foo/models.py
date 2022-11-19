"""Created dynamically"""

from django.db.models import Model, CharField, DateField, IntegerField
from django.contrib import admin

from .utils import get_models_config
from . import models as app_models
from .const import CHAR_FIELD_MAX_LENGTH


def create_models(module_name, module):
    """Create your models here, if not created yet"""
    models_spec = get_models_config()

    for m_name, m_spec in models_spec.items():
        m_name = str(m_name.capitalize())
        fields = m_spec.get("fields", [])

        class Meta:
            # At config only one form
            verbose_name = m_spec.get("title", "")
            verbose_name_plural = m_spec.get("title", "")

        model_attr_dict = dict(
            # http://stackoverflow.com/questions/7320705/python-missing-class-attribute-module-when-using-type/
            __module__=module_name,
            Meta=Meta,
        )

        for field in fields:
            field_type = field.get("type", "")
            if field_type == "char":
                model_attr_dict[field.get("id", "")] = CharField(
                    verbose_name=field.get("title", ""),
                    max_length=CHAR_FIELD_MAX_LENGTH,
                )
            elif field_type == "int":
                model_attr_dict[field.get("id", "")] = IntegerField(
                    verbose_name=field.get("title", "")
                )
            if field_type == "date":
                model_attr_dict[field.get("id", "")] = DateField(
                    verbose_name=field.get("title", "")
                )

        AppModel = type(m_name, (Model,), model_attr_dict)
        setattr(module, m_name, AppModel)

        class Admin(admin.ModelAdmin):
            list_display = [i.get("id", "") for i in fields][:5]

        admin.site.register(AppModel, Admin)


create_models(__name__, app_models)
