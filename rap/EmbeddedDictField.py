from djongo import models
from django import forms
import typing

class EmbeddedDictField(models.Field):
    def __init__(self,
                 model_container: typing.Type[dict],
                 model_form_class: typing.Type[forms.ModelForm] = None,
                 model_form_kwargs: dict = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_container = model_container
        self.model_form_class = model_form_class
        self.null = True
        self.instance = None

        if model_form_kwargs is None:
            model_form_kwargs = {}
        self.model_form_kwargs = model_form_kwargs

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['model_container'] = self.model_container
        if self.model_form_class is not None:
            kwargs['model_form_class'] = self.model_form_class
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        # print(value)
        ret_val = {}
        # for fld in value._meta.get_fields():
        #     if not useful_field(fld):
        #         continue
        #
        #     fld_value = getattr(value, fld.attname)
        # ret_val[ self.attname] = fld.get_db_prep_value(value, None, False)
        ret_val[self.attname] = self.get_db_prep_value(value, None, False)
        return ret_val

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if isinstance(value, dict):
            return value

        if not isinstance(value, Model):
            raise TypeError('Object must be of type Model')

        mdl_ob = {}
        for fld in value._meta.get_fields():
            if not useful_field(fld):
                continue
            fld_value = getattr(value, fld.attname)
            mdl_ob[fld.attname] = fld.get_db_prep_value(fld_value, connection, prepared)

        return mdl_ob

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)