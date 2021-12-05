from . import models
from django.core import validators
from django.core.exceptions import ValidationError
import re
from django.utils.translation import ugettext_lazy as _


class DriverValidator:
    requires_context = False
    @staticmethod
    def validate(value):
        value = models.User.objects.get(id=value)
        try:
            driver = value.type
            if not driver:
                return False
        except:
            return False
        return True
    def __call__(self,value):
        if not DriverValidator.validate(value):
            raise ValidationError("User cannot Driver")

class PasportIdValidator:
    requires_context = False
    @staticmethod
    def validate(value):
        if len(value) == 9:
            seria = value[0:2]
            for v in seria:
                try:
                    int(v)
                    return False
                except:
                    pass
            try:
                nomer = int(value[2:9])
            except:
                return False
            return True
        else:
            return False


    def __call__(self,value):
        if not PasportIdValidator.validate(value):
            raise ValidationError("Passport id incorrect")

