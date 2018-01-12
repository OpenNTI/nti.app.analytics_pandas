#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from pyramid.view import view_config

from zope import interface

from nti.app.analytics_pandas.reports.model import TopicsTimeseriesContext

from nti.analytics_pandas.analysis import TopicsCreationTimeseries
from nti.analytics_pandas.analysis import TopicsCreationTimeseriesPlot

from nti.analytics_pandas.analysis import TopicViewsTimeseries
from nti.analytics_pandas.analysis import TopicViewsTimeseriesPlot

from nti.analytics_pandas.analysis import TopicLikesTimeseries
from nti.analytics_pandas.analysis import TopicLikesTimeseriesPlot

from nti.analytics_pandas.analysis import TopicFavoritesTimeseries
from nti.analytics_pandas.analysis import TopicFavoritesTimeseriesPlot

from nti.mimetype.mimetype import nti_mimetype_with_class

from .commons import get_course_names
from .commons import build_plot_images_dictionary
from .commons import build_images_dict_from_plot_dict

from .mixins import AbstractReportView

@view_config(name="TopicsReport",
			 renderer="../templates/topics.rml")
class TopicsTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Topics Report')

	def _build_data(self, data=_('sample topics related events report')):
		keys = self.options.keys()

		if 'has_topics_created_data' not in keys:
			self.options['has_topics_created_data'] = False

		if 'has_topic_views_data' not in keys:
			self.options['has_topic_views_data'] = False

		if 'has_topic_likes_data' not in keys:
			self.options['has_topic_likes_data'] = False

		if 'has_topic_favorites_data' not in keys:
			self.options['has_topic_favorites_data'] = False

		self.options['data'] = data
		return self.options

	def __call__(self):
		values = self.readInput()
		if "MimeType" not in values.keys():
			values["MimeType"] = 'application/vnd.nextthought.reports.topicstimeseriescontext'
		self.context = self._build_context(TopicsTimeseriesContext, values)
		
		course_names = get_course_names(self.db.session, self.context.courses)
		self.options['course_names'] = ", ".join(map(str, course_names))
		data = {}

		self.tct = TopicsCreationTimeseries(self.db.session,
									   		self.context.start_date,
									   		self.context.end_date,
											self.context.courses,
											period=self.context.period)
		if self.tct.dataframe.empty:
			self.options['has_topics_created_data'] = False
		else:
			self.options['has_topics_created_data'] = True
			data = self.generate_topics_created_plots(data)


		self.tvt = TopicViewsTimeseries(self.db.session,
								   		self.context.start_date,
								   		self.context.end_date,
										self.context.courses,
										period=self.context.period)
		if self.tvt.dataframe.empty:
			self.options['has_topic_views_data'] = False
		else:
			self.options['has_topic_views_data'] = True
			data = self.generate_topic_view_plots(data)

		self.tlt = TopicLikesTimeseries(self.db.session,
								   		self.context.start_date,
								   		self.context.end_date,
										self.context.courses,
										period=self.context.period)

		if self.tlt.dataframe.empty:
			self.options['has_topic_likes_data'] = False
		else:
			self.options['has_topic_likes_data'] = True
			data = self.generate_topic_like_plots(data)

		self.tft = TopicFavoritesTimeseries(self.db.session,
									   		self.context.start_date,
									   		self.context.end_date,
											self.context.courses,
											period=self.context.period)
		if self.tft.dataframe.empty:
			self.options['has_topic_favorites_data'] = False
		else:
			self.options['has_topic_favorites_data'] = True
			data = self.generate_topic_favorite_plots(data)

		self._build_data(data)
		return self.options

	def generate_topics_created_plots(self, data):
		self.tctp = TopicsCreationTimeseriesPlot(self.tct)
		data = self.get_topics_created_plots(data)
		data = self.get_topics_created_plots_per_enrollment_types(data)
		data = self.get_topics_created_plots_per_device_types(data)
		if len(self.context.courses) > 1:
			data = self.get_topics_created_plots_per_course_sections(data)
		else:
			self.options['has_topics_created_per_course_sections'] = False
		return data

	def get_topics_created_plots(self, data):
		plots = self.tctp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots :
			data['topics_created'] = build_plot_images_dictionary(plots)
		return data

	def get_topics_created_plots_per_device_types(self, data):
		plots = self.tctp.analyze_events_per_device_types(self.context.period_breaks,
														  self.context.minor_period_breaks,
														  self.context.theme_bw_)
		self.options['has_topics_created_per_device_types'] = False
		if plots :
			data['topics_created_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_topics_created_per_device_types'] = True
		return data

	def get_topics_created_plots_per_course_sections(self, data):
		plots = self.tctp.analyze_events_per_course_sections(self.context.period_breaks,
															 self.context.minor_period_breaks,
															 self.context.theme_bw_)
		self.options['has_topics_created_per_course_sections'] = False
		if plots :
			data['topics_created_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_topics_created_per_course_sections'] = True
		return data

	def get_topics_created_plots_per_enrollment_types(self, data):
		plots = self.tctp.analyze_events_per_enrollment_types(self.context.period_breaks,
															  self.context.minor_period_breaks,
															  self.context.theme_bw_)
		self.options['has_topics_created_per_enrollment_types'] = False
		if plots :
			data['topics_created_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_topics_created_per_enrollment_types'] = True
		return data

	def generate_topic_view_plots(self, data):
		self.tvtp = TopicViewsTimeseriesPlot(self.tvt)
		data = self.get_topic_view_plots(data)
		data = self.get_topic_view_plots_per_device_types(data)
		if len(self.context.courses) > 1:
			data = self.get_topic_view_plots_per_course_sections(data)
		else:
			self.options['has_topic_views_per_course_sections'] = False
		data = self.get_topic_view_plots_per_enrollment_types(data)
		return data

	def get_topic_view_plots(self, data):
		plots = self.tvtp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['topic_views'] = build_plot_images_dictionary(plots)
		return data

	def get_topic_view_plots_per_device_types(self, data):
		plots = self.tvtp.analyze_device_types(self.context.period_breaks,
											   self.context.minor_period_breaks,
											   self.context.theme_bw_)
		self.options['has_topic_views_per_device_types'] = False
		if plots:
			data['topic_views_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_topic_views_per_device_types'] = True
		return data

	def get_topic_view_plots_per_course_sections(self, data):
		plots = self.tvtp.analyze_events_per_course_sections(self.context.period_breaks,
															 self.context.minor_period_breaks,
															 self.context.theme_bw_)
		self.options['has_topic_views_per_course_sections'] = False
		if plots:
			data['topic_views_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_topic_views_per_course_sections'] = True
		return data

	def get_topic_view_plots_per_enrollment_types(self, data):
		plots = self.tvtp.analyze_enrollment_types(self.context.period_breaks,
												   self.context.minor_period_breaks,
												   self.context.theme_bw_)
		self.options['has_topic_views_per_enrollment_types'] = False
		if plots:
			data['topic_views_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_topic_views_per_enrollment_types'] = True
		return data

	def generate_topic_like_plots(self, data):
		self.tltp = TopicLikesTimeseriesPlot(self.tlt)
		data = self.get_topic_like_plots(data)
		return data

	def get_topic_like_plots(self, data):
		plots = self.tltp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['topic_likes'] = build_plot_images_dictionary(plots)
		return data

	def generate_topic_favorite_plots(self, data):
		self.tftp = TopicFavoritesTimeseriesPlot(self.tft)
		data = self.get_topic_favorite_plots(data)
		return data

	def get_topic_favorite_plots(self, data):
		plots = self.tftp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['topic_favorites'] = build_plot_images_dictionary(plots)
		return data
