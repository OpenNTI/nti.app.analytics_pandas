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

from ...analysis import ForumsEventsTimeseries
from ...analysis import ForumsCreatedTimeseries
from ...analysis import ForumCommentLikesTimeseries
from ...analysis import ForumCommentFavoritesTimeseries
from ...analysis import ForumsCommentsCreatedTimeseries

from ...analysis import ForumsEventsTimeseriesPlot
from ...analysis import ForumsCreatedTimeseriesPlot
from ...analysis import ForumCommentLikesTimeseriesPlot
from ...analysis import ForumsCommentsCreatedTimeseriesPlot
from ...analysis import ForumCommentFavoritesTimeseriesPlot

from .commons import get_course_names
from .commons import build_plot_images_dictionary
from .commons import  build_images_dict_from_plot_dict

from .mixins import AbstractReportView

@interface.implementer(interface.Interface)
class ForumsTimeseriesContext(object):

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

Context = ForumsTimeseriesContext

class ForumsTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Forums Related Events')

	def _build_data(self, data=_('sample forums related events report')):
		keys = self.options.keys()
		if 'has_forums_created_data' not in keys:
			self.options['has_forums_created_data'] = False

		if 'has_forum_comments_created_data' not in keys:
			self.options['has_forum_comments_created_data'] = False

		if 'has_forum_comment_likes_data' not in keys:
			self.options['has_forum_comment_likes_data'] = False

		if 'has_forum_comment_favorites_data' not in keys:
			self.options['has_forum_comment_favorites_data'] = False

		if 'has_forum_events_data' not in keys:
			self.options['has_forum_events_data'] = False

		self.options['data'] = data
		return self.options

	def __call__(self):
		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ", ".join(map(str, course_names))

		self.fct = ForumsCreatedTimeseries(self.context.session,
										   self.context.start_date,
										   self.context.end_date,
										   self.context.courses,
										   period=self.context.period)
		data = {}

		if self.fct.dataframe.empty:
			self.options['has_forums_created_data'] = False
		else:
			self.options['has_forums_created_data'] = True
			data = self.generate_forums_created_plots(data)

		self.fcct = ForumsCommentsCreatedTimeseries(self.context.session,
													self.context.start_date,
													self.context.end_date,
													self.context.courses,
													period=self.context.period)
		if self.fcct.dataframe.empty:
			self.options['has_forum_comments_created_data'] = False
		else:
			self.options['has_forum_comments_created_data'] = True
			data = self.generate_forum_comments_created_plots(data)

		self.fclt = ForumCommentLikesTimeseries(self.context.session,
												self.context.start_date,
												self.context.end_date,
												self.context.courses,
												period=self.context.period)
		if self.fclt.dataframe.empty:
			self.options['has_forum_comment_likes_data'] = False
		else:
			self.options['has_forum_comment_likes_data'] = True
			data = self.generate_forum_comment_likes_plots(data)

		self.fcft = ForumCommentFavoritesTimeseries(self.context.session,
													self.context.start_date,
													self.context.end_date,
													self.context.courses,
													period=self.context.period)
		if self.fcft.dataframe.empty:
			self.options['has_forum_comment_favorites_data'] = False
		else:
			self.options['has_forum_comment_favorites_data'] = True
			data = self.generate_forum_comment_favorites_plots(data)

		self.fet = ForumsEventsTimeseries(self.fct, self.fcct, self.fclt, self.fcft)
		data = self.generate_forum_event_plots(data)

		self._build_data(data)
		return self.options

	def generate_forum_event_plots(self, data):
		self.fetp = ForumsEventsTimeseriesPlot(self.fet)
		data = self.get_forum_event_plots(data)
		return data

	def get_forum_event_plots(self, data):
		plots = self.fetp.explore_all_events(self.context.period_breaks,
											 self.context.minor_period_breaks,
											 self.context.theme_bw_)
		if plots:
			data['forum_events'] = build_plot_images_dictionary(plots)
			self.options['has_forum_events_data'] = True
		return data

	def generate_forums_created_plots(self, data):
		self.fctp = ForumsCreatedTimeseriesPlot(self.fct)
		data = self.get_forums_created_plots(data)
		data = self.get_forums_created_plots_per_device_types(data)
		return data

	def get_forums_created_plots(self, data):
		plots = self.fctp.explore_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['forums_created'] = build_plot_images_dictionary(plots)
		return data

	def get_forums_created_plots_per_device_types(self, data):
		plots = self.fctp.analyze_device_types(self.context.period_breaks,
											   self.context.minor_period_breaks,
										 	   self.context.theme_bw_)
		self.options['has_forums_created_data_per_device_types'] = False
		if plots:
			data['forums_created_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_forums_created_data_per_device_types'] = True
		return data

	def generate_forum_comments_created_plots(self, data):
		self.fcctp = ForumsCommentsCreatedTimeseriesPlot(self.fcct)
		data = self.get_forum_comments_created_plots(data)
		data = self.get_forum_comments_created_plots_per_enrollment_types(data)
		data = self.get_forum_comments_created_plots_per_device_types(data)
		if len(self.context.courses) > 1:
			data = self.get_forum_comments_created_plots_per_course_sections(data)
		data = self.get_the_most_active_forum_comment_users_plot(data)
		return data

	def get_forum_comments_created_plots(self, data):
		plots = self.fcctp.explore_events(self.context.period_breaks,
										  self.context.minor_period_breaks,
										  self.context.theme_bw_)
		if plots:
			data['forum_comments_created'] = build_plot_images_dictionary(plots)
		return data

	def get_forum_comments_created_plots_per_enrollment_types(self, data):
		plots = self.fcctp.analyze_enrollment_types(self.context.period_breaks,
										  		self.context.minor_period_breaks,
										  		self.context.theme_bw_)
		self.options['has_forum_comments_created_data_per_enrollment_types'] = False
		if plots:
			data['forum_comments_created_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_forum_comments_created_data_per_enrollment_types'] = True
		return data

	def get_forum_comments_created_plots_per_device_types(self, data):
		plots = self.fcctp.analyze_device_types(self.context.period_breaks,
										  		self.context.minor_period_breaks,
										  		self.context.theme_bw_)
		self.options['has_forum_comments_created_data_per_device_types'] = False
		if plots:
			data['forum_comments_created_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_forum_comments_created_data_per_device_types'] = True
		return data

	def get_forum_comments_created_plots_per_course_sections(self, data):
		plots = self.fcctp.analyze_comments_per_section(self.context.period_breaks,
										  				self.context.minor_period_breaks,
										 				self.context.theme_bw_)
		self.options['has_forum_comments_created_data_per_course_sections'] = False
		if plots:
			data['forum_comments_created_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_forum_comments_created_data_per_course_sections'] = True
		return data

	def get_the_most_active_forum_comment_users_plot(self, data):
		plots = self.fcctp.plot_the_most_active_users(self.context.number_of_most_active_user)
		self.options['has_forum_comments_users'] = False
		if plots:
			data['forum_comments_created_users'] = build_plot_images_dictionary(plots)
			self.options['has_forum_comments_users'] = True
		return data

	def generate_forum_comment_likes_plots(self, data):
		self.fcltp = ForumCommentLikesTimeseriesPlot(self.fclt)
		data = self.get_forum_comment_likes_plots(data)
		data = self.get_forum_comment_likes_plots_per_enrollment_types(data)
		data = self.get_forum_comment_likes_plots_per_device_types(data)
		if len(self.context.courses) > 1:
			data = self.get_forum_comment_likes_plots_per_course_sections(data)
		return data

	def get_forum_comment_likes_plots(self, data):
		plots = self.fcltp.analyze_events(self.context.period_breaks,
						  				  self.context.minor_period_breaks,
						 				  self.context.theme_bw_)
		if plots:
			data['forum_comment_likes'] = build_plot_images_dictionary(plots)
		return data

	def get_forum_comment_likes_plots_per_device_types(self, data):
		plots = self.fcltp.analyze_device_types(self.context.period_breaks,
							  					self.context.minor_period_breaks,
							 					self.context.theme_bw_)
		self.options['has_forum_comment_likes_per_device_types'] = False
		if plots:
			data['forum_comment_likes_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_forum_comment_likes_per_device_types'] = True
		return data

	def get_forum_comment_likes_plots_per_enrollment_types(self, data):
		plots = self.fcltp.analyze_enrollment_types(self.context.period_breaks,
							  					self.context.minor_period_breaks,
							 					self.context.theme_bw_)
		self.options['has_forum_comment_likes_per_enrollment_types'] = False
		if plots:
			data['forum_comment_likes_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_forum_comment_likes_per_enrollment_types'] = True
		return data

	def get_forum_comment_likes_plots_per_course_sections(self, data):
		plots = self.fcltp.analyze_events_per_course_sections(self.context.period_breaks,
											  				  self.context.minor_period_breaks,
											 				  self.context.theme_bw_)
		self.options['has_forum_comment_likes_per_course_sections'] = False
		if plots:
			data['forum_comment_likes_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_forum_comment_likes_per_course_sections'] = True
		return data

	def generate_forum_comment_favorites_plots(self, data):
		self.fcftp = ForumCommentFavoritesTimeseriesPlot(self.fcft)
		data = self.get_forum_comment_favorites_plots(data)
		data = self.get_forum_comment_favorites_plots_per_enrollment_types(data)
		data = self.get_forum_comment_favorites_plots_per_device_types(data)
		if len(self.context.courses) > 1:
			data = self.get_forum_comment_favorites_plots_per_course_sections(data)
		return data

	def get_forum_comment_favorites_plots(self, data):
		plots = self.fcftp.explore_events(self.context.period_breaks,
						  				  self.context.minor_period_breaks,
						 				  self.context.theme_bw_)
		if plots:
			data['forum_comment_favorites'] = build_plot_images_dictionary(plots)
		return data

	def get_forum_comment_favorites_plots_per_enrollment_types(self, data):
		plots = self.fcftp.analyze_enrollment_types(self.context.period_breaks,
							  					self.context.minor_period_breaks,
							 					self.context.theme_bw_)
		self.options['has_forum_comment_favorites_per_enrollment_types'] = False
		if plots:
			data['forum_comment_favorites_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_forum_comment_favorites_per_enrollment_types'] = True
		return data

	def get_forum_comment_favorites_plots_per_device_types(self, data):
		plots = self.fcftp.analyze_device_types(self.context.period_breaks,
							  					self.context.minor_period_breaks,
							 					self.context.theme_bw_)
		self.options['has_forum_comment_favorites_per_device_types'] = False
		if plots:
			data['forum_comment_favorites_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_forum_comment_favorites_per_device_types'] = True
		return data

	def get_forum_comment_favorites_plots_per_course_sections(self, data):
		plots = self.fcftp.analyze_events_per_course_sections(self.context.period_breaks,
										  					  self.context.minor_period_breaks,
										 					  self.context.theme_bw_)
		self.options['has_forum_comment_favorites_per_course_sections'] = False
		if plots:
			data['forum_comment_favorites_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_forum_comment_favorites_per_course_sections'] = True
		return data

View = ForumsTimeseriesReport = ForumsTimeseriesReportView
