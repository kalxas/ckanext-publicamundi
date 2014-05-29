import logging
import zope.interface
import zope.schema
import datetime

import ckan.plugins.toolkit as toolkit
from ckan.lib.navl.dictization_functions import missing, StopOnError, Invalid

from ckanext.publicamundi.lib.metadata import dataset_types

_t = toolkit._

log1 = logging.getLogger(__name__)

def to_float_number(value, context):
    try:
        value = float(value)
    except: 
        raise Invalid(_t('Not a number'))
    return value

def to_iso_date(value, context):
    try:
        fmt = '%Y-%m-%d'
        d = datetime.datetime.strptime(value, fmt)
    except ValueError as ex: 
        raise Invalid(_t('Not a ISO date: %s' %(str(ex))))
    return value

def to_iso_datetime(value, context):
    try:
        fmt = '%Y-%m-%d %H:%M:%S'
        d = datetime.datetime.strptime(value, fmt)
    except ValueError as ex: 
        raise Invalid(_t('Not a ISO datetime: %s' %(str(ex))))
    return value

