from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relation, relationship, backref
from geoalchemy import Geometry, GeometryColumn, GeometryDDL, Polygon, Point

from pycsw import util

from ckan.model import Package

from ckanext.publicamundi.model import Base

class CswRecord(Base):
    __tablename__ = 'csw_records'

    # core; nothing happens without these
    identifier = Column('identifier', Text, ForeignKey(Package.id, ondelete='cascade'), primary_key=True)
    typename = Column('typename', Text,
           default='csw:Record', nullable=False, index=True)
    schema = Column('schema', Text,
           default='http://www.opengis.net/cat/csw/2.0.2', nullable=False,
           index=True)
    mdsource = Column('mdsource', Text, default='local', nullable=False,
           index=True)
    insert_date = Column('insert_date', Text, nullable=False, index=True)
    xml = Column('xml', Text, nullable=False)
    anytext = Column('anytext', Text, nullable=False)
    language = Column('language', Text, index=True)

    # identification
    type = Column('type', Text, index=True)
    title = Column('title', Text, index=True)
    title_alternate = Column('title_alternate', Text, index=True)
    abstract = Column('abstract', Text, index=True)
    keywords = Column('keywords', Text, index=True)
    keywordstype = Column('keywordstype', Text, index=True)
    parentidentifier = Column('parentidentifier', Text, index=True)
    relation = Column('relation', Text, index=True)
    time_begin = Column('time_begin', Text, index=True)
    time_end = Column('time_end', Text, index=True)
    topicategory = Column('topicategory', Text, index=True)
    resourcelanguage = Column('resourcelanguage', Text, index=True)

    # attribution
    creator = Column('creator', Text, index=True)
    publisher = Column('publisher', Text, index=True)
    contributor = Column('contributor', Text, index=True)
    organization = Column('organization', Text, index=True)

    # security
    securityconstraints = Column('securityconstraints', Text, index=True)
    accessconstraints = Column('accessconstraints', Text, index=True)
    otherconstraints = Column('otherconstraints', Text, index=True)

    # date
    date = Column('date', Text, index=True)
    date_revision = Column('date_revision', Text, index=True)
    date_creation = Column('date_creation', Text, index=True)
    date_publication = Column('date_publication', Text, index=True)
    date_modified = Column('date_modified', Text, index=True)

    format = Column('format', Text, index=True)
    source = Column('source', Text, index=True)

    # geospatial
    crs = Column('crs', Text, index=True)
    geodescode = Column('geodescode', Text, index=True)
    denominator = Column('denominator', Text, index=True)
    distancevalue = Column('distancevalue', Text, index=True)
    distanceuom = Column('distanceuom', Text, index=True)
    wkt_geometry = Column('wkt_geometry', Text)

    # service
    servicetype = Column('servicetype', Text, index=True)
    servicetypeversion = Column('servicetypeversion', Text, index=True)
    operation = Column('operation', Text, index=True)
    couplingtype = Column('couplingtype', Text, index=True)
    operateson = Column('operateson', Text, index=True)
    operatesonidentifier = Column('operatesonidentifier', Text, index=True)
    operatesoname = Column('operatesoname', Text, index=True)

    # additional
    degree = Column('degree', Text, index=True)
    classification = Column('classification', Text, index=True)
    conditionapplyingtoaccessanduse = Column('conditionapplyingtoaccessanduse', Text, index=True)
    lineage = Column('lineage', Text, index=True)
    responsiblepartyrole = Column('responsiblepartyrole', Text, index=True)
    specificationtitle = Column('specificationtitle', Text, index=True)
    specificationdate = Column('specificationdate', Text, index=True)
    specificationdatetype = Column('specificationdatetype', Text, index=True)

    # distribution
    # links: format "name,description,protocol,url[^,,,[^,,,]]"
    links = Column('links', Text, index=True)

    geom = GeometryColumn('wkb_geometry', Geometry(2), nullable=True)

    #uniq_name = UniqueConstraint('name')

    def __init__(self, id, insert_date, xml):
        self.identifier = id
        self.insert_date = insert_date or datetime.now();
        self.xml = xml
        self.anytext = util.get_anytext(xml)

    def __unicode__(self):
        return "<CswRecord \"%s\">" % (self.schema)

# note: needed to generate proper AddGeometryColumn statements
GeometryDDL(CswRecord.__table__)

