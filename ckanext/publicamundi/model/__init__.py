import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .csw_record import CswRecord
from .csw_record import post_setup as csw_post_setup
from .csw_record import pre_cleanup as csw_pre_cleanup

from .resource_ingest import ResourceIngest

def post_setup(self):
	csw_post_setup()

def pre_cleanup(self):
	csw_pre_cleanup()
