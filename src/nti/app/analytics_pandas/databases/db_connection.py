#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from pandas import DataFrame

from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine as sqlalchemy_create_engine

from nti.analytics_database import Base

from ..utils.string_folder import StringFolder

def create_engine(dburi, pool_size=30, max_overflow=10, pool_recycle=300):
	try:
		if dburi == 'sqlite://':
			result = sqlalchemy_create_engine(dburi,
											  connect_args={'check_same_thread':False},
											  poolclass=StaticPool)

		else:
			result = sqlalchemy_create_engine(dburi,
											  pool_size=pool_size,
											  max_overflow=max_overflow,
											  pool_recycle=pool_recycle)
	except TypeError:
		# SQLite does not use pooling anymore.
		result = sqlalchemy_create_engine(dburi)
	return result

def create_sessionmaker(engine, autoflush=True, twophase=True):
	result = sessionmaker(bind=engine,
						  autoflush=autoflush,
						  twophase=twophase)
	return result

def create_session(sessionmaker):
	return scoped_session(sessionmaker)

class DBConnection(object):

	def __init__(self):
		# TODO: Fix URI
		dburi = "mysql+pymysql://root@localhost:3306/Analytics"
		self.engine = create_engine(dburi)
		self.metadata = getattr(Base, 'metadata').create_all(self.engine)
		self.sessionmaker = create_sessionmaker(self.engine)
		self.session = create_session(self.sessionmaker)

	def close_session(self):
		self.session.close()

def create_engine_mysql(db_user='root', pwd=None, host='localhost', port='3306',
						db_name='Analytics'):
	"""
	create engine to access mysql db
	"""
	if pwd is None:
		engine_string = u'mysql+pymysql://%s@%s:%s/%s' % (db_user, host, port, db_name)
	else:
		engine_string = u'mysql+pymysql://%s:%s@%s:%s/%s' % (db_user, pwd, host, port, db_name)
	result = sqlalchemy_create_engine(engine_string)
	return result

def build_data_frame(engine, query):
	with engine.connect() as connection:
		# Execute the query against the database
		results = (connection.execution_options(stream_results=True).execute(query))
		# dataframe = DataFrame(iter(results))
		dataframe = DataFrame(string_folding_wrapper(results))
		dataframe.columns = results.keys()
	connection.close()
	return dataframe

def string_folding_wrapper(query_results):
	"""
	source : http://www.mobify.com/blog/sqlalchemy-memory-magic/
	This generator yields rows from the results as tuples,
	with all string values folded.
	"""
	# Get the list of keys so that we build tuples with all
	# the values in key order.
	keys = query_results.keys()
	folder = StringFolder()
	for row in query_results:
		yield tuple(folder.fold_string(row[key])for key in keys)
