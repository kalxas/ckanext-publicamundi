import logging
import zope.interface
import zope.schema

import ckan.plugins.toolkit as toolkit
from ckan.lib.navl.dictization_functions import missing, StopOnError, Invalid

from ckanext.publicamundi.lib.metadata import dataset_types

_t = toolkit._

log1 = logging.getLogger(__name__)

def to_float_number(value, context):
    raise Exception('to_float_number')
    try:
        value = float(value)
    except: 
        raise Invalid(_t('Not a number'))
    return value

