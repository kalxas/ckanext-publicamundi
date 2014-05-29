import logging
import zope.interface
import zope.schema
import json

import ckan.plugins.toolkit as toolkit
from ckan.lib.navl.dictization_functions import missing, StopOnError, Invalid

from ckanext.publicamundi.lib.metadata import dataset_types

_t = toolkit._

log1 = logging.getLogger(__name__)

def is_dataset_type(value, context):
    if not value in dataset_types:
        raise Invalid('Unknown dataset_type (%s)' %(value))

def dataset_postprocess_read(key, data, errors, context):
    assert key[0] == '__after', 'This validator can only be invoked in the __after stage'
    log1.debug('Post-processing dataset for reading')
    # Prepare computed fields, reorganize structure etc.
    data[('baz_view',)] = u'I am a read-only Baz'
    #raise Exception('Break (postprocess read)')
    pass

def dataset_postprocess_edit(key, data, errors, context):
    assert key[0] == '__after', 'This validator can only be invoked in the __after stage'
    log1.debug('Post-processing dataset for editing')
    _convert_bbox_to_spatial(data)
    #raise Exception('Break (postprocess edit)')
    pass

def dataset_validate(key, data, errors, context):
    assert key[0] == '__after', 'This validator can only be invoked in the __after stage'
    log1.debug('Validating dataset for editing')
    _validate_bbox(data)
    #raise Exception('Break (validate)')
    pass

def dataset_preprocess_edit(key, data, errors, context):
    assert key[0] == '__before', 'This validator can only be invoked in the __before stage'
    log1.debug('Pre-processing dataset for editing')
    #raise Exception('Break')
    pass

def get_field_validator(field):
    def validate(value, context):
        try: 
            # Invoke the zope.schema validator
            field.validate(value)
        except zope.schema.ValidationError as ex:
            # Map this exception to the one expected by CKAN's validator
            raise Invalid(u'Invalid data (%s)' %(type(ex).__name__))
        return value
    return validate


## Todo: Replace by zope.schema-based functionality

def _validate_bbox(data):
    wblng = data[('bounding_box.wblng',)]
    eblng = data[('bounding_box.eblng',)]
    if wblng > eblng:
        raise Invalid(_t('Invalid range for West-East longitude'))
    nblat = data[('bounding_box.nblat',)]
    sblat = data[('bounding_box.sblat',)]
    if sblat > nblat:
        raise Invalid(_t('Invalid range for South-North latitude'))
    

def _convert_bbox_to_spatial(data):
    x1 = x4 = data[('bounding_box.wblng',)]
    x2 = x3 = data[('bounding_box.eblng',)]
    y1 = y2 = data[('bounding_box.sblat',)]
    y3 = y4 = data[('bounding_box.nblat',)]
    data[('extras',)].append({
        'key': 'spatial',
        'value': json.dumps({ 
            'type': 'Polygon',
            'coordinates': [
                [
                    [x1, y1], [x2, y2], [x3, y3], [x4, y4],
                    [x1, y1],
                ]
            ]
        }),
    })

def is_latitude(value, context):
    if value < -90 or value > 90:
        raise Invalid(_t('This number cannot represent a latitude'))
    return value

def is_longitude(value, context):
    if value < -180 or value > 180:
        raise Invalid(_t('This number cannot represent a longitude'))
    return value



