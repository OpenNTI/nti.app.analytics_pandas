#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from zope import interface

from ...analysis import TopicsCreationTimeseries
from ...analysis import TopicsCreationTimeseriesPlot

from ...analysis import TopicViewsTimeseries
from ...analysis import TopicViewsTimeseriesPlot

from ...analysis import TopicLikesTimeseries
from ...analysis import TopicLikesTimeseriesPlot

from ...analysis import TopicFavoritesTimeseries
from ...analysis import TopicFavoritesTimeseriesPlot

from .commons import get_course_names
from .commons import build_plot_images_dictionary
from .commons import build_images_dict_from_plot_dict

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class TopicsTimeseriesContext(object):

	def __init__(self, session=None, start_date=None, end_date=None, courses=None,
				 period_breaks=None, minor_period_breaks=None, theme_bw_=True,
				 number_of_most_active_user=10, period='daily'):
		self.session = session
		self.courses = courses
		self.end_date = end_date
		self.start_date = start_date
		self.period_breaks = period_breaks
		self.theme_bw_ = theme_bw_
		self.minor_period_breaks = minor_period_breaks
		self.number_of_most_active_user = number_of_most_active_user
		self.period = period

Context = TopicsTimeseriesContext

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
		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ", ".join(map(str, course_names))
		data = {}

		self.tct = TopicsCreationTimeseries(self.context.session,
									   		self.context.start_date,
									   		self.context.end_date,
											self.context.courses,
											period=self.context.period)
		if self.tct.dataframe.empty:
			self.options['has_topics_created_data'] = False
		else:
			self.options['has_topics_created_data'] = True
			data = self.generate_topics_created_plots(data)


		self.tvt = TopicViewsTimeseries(self.context.session,
								   		self.context.start_date,
								   		self.context.end_date,
										self.context.courses,
										period=self.context.period)
		if self.tvt.dataframe.empty:
			self.options['has_topic_views_data'] = False
		else:
			self.options['has_topic_views_data'] = True
			data = self.generate_topic_view_plots(data)

		self.tlt = TopicLikesTimeseries(self.context.session,
								   		self.context.start_date,
								   		self.context.end_date,
										self.context.courses,
										period=self.context.period)

		if self.tlt.dataframe.empty:
			self.options['has_topic_likes_data'] = False
		else:
			self.options['has_topic_likes_data'] = True
			data = self.generate_topic_like_plots(data)

		self.tft = TopicFavoritesTimeseries(self.context.session,
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

View = TopicsTimeseriesReport = TopicsTimeseriesReportView
