#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from .. import MessageFactory as _

from nti.analytics_database.resources import Resources

from .mixins import TableQueryMixin

from . import orm_dataframe

class QueryResources(TableQueryMixin):

	table = Resources

	def get_all_resources(self):
		r = self.table
		query = self.session.query(r.resource_id,
									r.resource_ds_id,
									r.resource_display_name,
									r.max_time_length)
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def get_resources_ds_id_given_id(self, resource_id=()):
		r = self.table
		query = self.session.query(r.resource_id,
									r.resource_ds_id).filter(r.resource_id.in_(resource_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def get_resources_given_id(self, resources_id=None):
		r = self.table
		query = self.session.query(r.resource_id,
									r.resource_ds_id,
									r.resource_display_name,
									r.max_time_length).filter(r.resource_id.in_(resources_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	def get_resource_display_name_given_id(self, resources_id=None):
		r = self.table
		query = self.session.query(r.resource_id,
									r.resource_display_name).filter(r.resource_id.in_(resources_id))
		dataframe = orm_dataframe(query, self.columns)
		return dataframe

	@classmethod
	def _label_resource_type(cls, resource_ds_id):
		# video
		if u'.ntivideo.' in resource_ds_id:
			return _(u'video')
		elif u'NTISlideVideo' in resource_ds_id:
			return _(u'slide video')

		# relatedwork
		if u'.relatedworkref.' in resource_ds_id:
			if u'requiredreadings' in resource_ds_id :
				return _(u'required readings')
			elif u'textbook' in resource_ds_id:
				return _(u'textbook')
			elif u'reading_' in resource_ds_id:
				return _(u'reading')
			elif u'lecture' in resource_ds_id:
				return _(u'related work lecture')
			elif u'hw' in resource_ds_id:
				return _(u'homework')
			elif u'syllabus' in resource_ds_id:
				return _(u'syllabus')
			elif 'problem' in resource_ds_id:
				return _(u'problems')
			else:
				print(resource_ds_id)
				return _(u'relatedworkref')

		# assignment
		if u'naq.asg.assignment:' in resource_ds_id:
			return _(u'assignment')

		# question set
		if u'naq.set.qset' in resource_ds_id:
			return _(u'question set')

		# quiz
		if u'.naq.qid.' in resource_ds_id:
			if u'self_check' in resource_ds_id:
				return _(u'self check question')
			elif u'quiz' in resource_ds_id:
				return _(u'quiz question')
			else :
				return _(u'question')
		elif u'quiz' in resource_ds_id:
			return _(u'quiz')

		# self assessment
		if u'self_assessment' in resource_ds_id:
			return _(u'self assessment')

		# self check
		if u'self_check' in resource_ds_id or 'check_yourself' in resource_ds_id:
			return _(u'self check')

		# pre lab workbook
		if u'pre_lab_workbook:' in resource_ds_id:
			return _(u'pre lab workbook')

		# honor code
		if u'honor_code' in resource_ds_id:
			return _(u'honor code')

		# lecture
		if u'lec:' in resource_ds_id:
			return _(u'lecture')

		# reading
		if u'reading:' in resource_ds_id:
			return _(u'reading')

		# discussion
		if u'discussion:' in resource_ds_id or u'discussions:' in resource_ds_id:
			return _(u'discussion')
		elif u'In_Class_Discussions' in resource_ds_id:
			return _(u'in class discussion')
		elif u'section:' in resource_ds_id or u'sec:' in resource_ds_id:
			return _(u'section')

		# nti card
		if u'nticard' in resource_ds_id:
			return _(u'nticard')

		# timeline
		if u'JSON:Timeline' in resource_ds_id:
			return _(u'timeline')

		if 'practice_problems' in resource_ds_id:
			return _(u'practice problems')

		if 'problem' in resource_ds_id:
			return _(u'problems')

		print(resource_ds_id)
		return _(u'unknown')

	def add_resource_type(self, dataframe):
		index = dataframe['resource_ds_id']
		dataframe['resource_type'] = index.apply(lambda x: self._label_resource_type(x))
		return dataframe
