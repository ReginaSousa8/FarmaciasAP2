from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from coredrca.models import *

def validate_domainonly_nome(value):
    if 'None' in value:
        raise ValidationError(_('ERRO'))
    return value



