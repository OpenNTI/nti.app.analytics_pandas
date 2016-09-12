#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

import pandas as pd

import numpy as np

from zope.i18n import translate

from .commons import generate_three_plots
from .commons import line_plot_x_axis_date
from .commons import group_line_plot_x_axis_date
from .commons import generate_three_group_by_plots
from .commons import histogram_plot_x_axis_discrete

class AssessmentEventsTimeseriesPlot(object):

	def __init__(self, aet):
		"""
		aet = AssessmentEventsTimeseries
		"""
		self.aet = aet
		self.period = aet.period

	def combine_events(self, period_breaks='1 week',
					   minor_period_breaks='1 day', 
					   theme_seaborn_=True):
		aet = self.aet
		df = aet.combine_events()
		if len(df.index) <= 0:
			return ()

		group_by = 'event_type'
		event_title = _('Number of assessments events grouped by event type during period of time')
		user_title = _('Number of unique users creating assessments events during period of time')
		ratio_title = _('Ratio of assessments events over unique user on each available date')
		event_type = 'assessment_events'
		event_y_axis_field = 'total_events'
		event_y_axis_label = _('Number of assessments events')
		plots = generate_three_group_by_plots(df,
											  group_by,
											  event_title,
											  user_title,
											  ratio_title,
											  event_y_axis_field,
											  event_y_axis_label,
											  period_breaks,
											  minor_period_breaks,
											  theme_seaborn_,
											  event_type,
											  period=self.period)
		return plots

	def analyze_assessments_taken_over_total_enrollments(self,
														 period_breaks='1 week',
					   									 minor_period_breaks='1 day',
					   									 theme_seaborn_=True):
		aet = self.aet
		df = aet.analyze_assessments_taken_over_total_enrollments()
		if df is None:
			return ()

		if df.empty:
			return ()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		plot = group_line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label='Date',
								y_axis_label='Ratio',
								title='Ratio of assessments taken over total enrollments',
								period_breaks=period_breaks,
								group_by='assessment_type',
								minor_breaks=minor_period_breaks,
								theme_seaborn_=theme_seaborn_,
								plot_name='ratio_assessments_taken',
								period=self.period)
		return (plot,)

class AssignmentViewsTimeseriesPlot(object):

	def __init__(self, avt):
		"""
		avt = AssignmentViewsTimeseries
		"""
		self.avt = avt
		self.period = avt.period

	def analyze_events(self, 
					   period_breaks='1 week',
					   minor_period_breaks='1 day', 
					   theme_seaborn_=True):
		avt = self.avt
		df = avt.analyze_events()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_type = 'assignment_views'
		event_title = _('Number of assignments viewed during period of time')
		user_title = _('Number of unique users viewing assignments during period of time')
		ratio_title = _('Ratio of assignments viewed over unique user on each available date')
		event_y_axis_field = 'number_assignments_viewed'
		event_y_axis_label = _('Number of assignments viewed')
		plots = generate_three_plots(df,
									 event_title,
									 user_title,
									 ratio_title,
									 event_y_axis_field,
									 event_y_axis_label,
									 period_breaks,
									 minor_period_breaks,
									 theme_seaborn_,
									 event_type,
									 period=self.period)
		return plots

	def analyze_events_per_course_sections(self, 
										   period_breaks='1 week',
										   minor_period_breaks='1 day',
										   theme_seaborn_=True):
		avt = self.avt
		df = avt.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = {}
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of assignments viewed per course sections')
			user_title = _('Number of unique users viewing assignments per course sections')
			ratio_title = _('Ratio of assignments viewed over unique user per course sections')
			event_type = 'assignment_views_per_course_sections'
			event_y_axis_field = 'number_assignments_viewed'
			event_y_axis_label = _('Number of assignments viewed')
			all_section_plots = generate_three_group_by_plots(df,
															  group_by,
															  event_title,
															  user_title,
															  ratio_title,
															  event_y_axis_field,
															  event_y_axis_label,
															  period_breaks,
															  minor_period_breaks,
															  theme_seaborn_,
															  event_type,
															  period=self.period)
			plots['all_section_plots'] = all_section_plots

		section_plots_dict = {}
		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']

			event_title = translate(_("Number of assignments viewed in ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users viewing assignments in ${title}",
									  mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of assignments viewed over unique user in ${title}",
									  mapping={'title': context_name}))

			event_type = 'assignment_views_in_%s' % (context_name.replace(' ', '_'))
			event_y_axis_field = 'number_assignments_viewed'
			event_y_axis_label = _('Number of assignments viewed')
			section_plots = generate_three_plots(df,
												 event_title,
												 user_title,
												 ratio_title,
												 event_y_axis_field,
												 event_y_axis_label,
												 period_breaks,
												 minor_period_breaks,
												 theme_seaborn_,
												 event_type,
												 period=self.period)
			key = 'section_%s' % (course_id)
			section_plots_dict[key] = section_plots
		plots['section_plots'] = section_plots_dict
		return plots

	def analyze_events_group_by_device_type(self,
											period_breaks='1 week',
											minor_period_breaks='1 day',
											theme_seaborn_=True):
		avt = self.avt
		df = avt.analyze_events_group_by_device_type()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of assignments viewed grouped by device types')
		user_title = _('Number of unique users viewing assignments grouped by device types')
		ratio_title = _('Ratio of assignments viewed over unique user grouped by device types')
		event_type = 'assignment_views_per_device_types'
		event_y_axis_field = 'number_assignments_viewed'
		event_y_axis_label = _('Number of assignments viewed')
		plots = generate_three_group_by_plots(df,
											  group_by,
											  event_title,
											  user_title,
											  ratio_title,
											  event_y_axis_field,
											  event_y_axis_label,
											  period_breaks,
											  minor_period_breaks,
											  theme_seaborn_,
											  event_type,
											  period=self.period)
		return plots

	def analyze_events_group_by_enrollment_type(self, 
												period_breaks='1 week',
												minor_period_breaks='1 day',
												theme_seaborn_=True):
		avt = self.avt
		df = avt.analyze_events_group_by_enrollment_type()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'enrollment_type'
		event_title = _('Number of assignments viewed grouped by enrollment types')
		user_title = _('Number of unique users viewing assignments grouped by enrollment types')
		ratio_title = _('Ratio of assignments viewed over unique user grouped by enrollment types')
		event_type = 'assignment_views_per_enrollment_types'
		event_y_axis_field = 'number_assignments_viewed'
		event_y_axis_label = _('Number of assignments viewed')
		plots = generate_three_group_by_plots(df,
											  group_by,
											  event_title,
											  user_title,
											  ratio_title,
											  event_y_axis_field,
											  event_y_axis_label,
											  period_breaks,
											  minor_period_breaks,
											  theme_seaborn_,
											  event_type,
											  period=self.period)
		return plots

class AssignmentsTakenTimeseriesPlot(object):

	def __init__(self, att):
		"""
		att = AssignmentsTakenTimeseries
		"""
		self.att = att
		self.period = att.period

	def analyze_events(self, period_breaks='1 week', minor_period_breaks='1 day',
					   theme_seaborn_=True):

		att = self.att
		df = att.analyze_events()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of assignments taken during period of time')
		user_title = _('Number of unique users taking assignments during period of time')
		ratio_title = _('Ratio of assignments taken over unique user on each available date')
		event_type = 'assignments_taken'
		event_y_axis_field = 'number_assignments_taken'
		event_y_axis_label = _('Number of assignments taken')
		plots = generate_three_plots(df,
									 event_title,
									 user_title,
									 ratio_title,
									 event_y_axis_field,
									 event_y_axis_label,
									 period_breaks,
									 minor_period_breaks,
									 theme_seaborn_,
									 event_type,
									 period=self.period)
		return plots

	def analyze_events_per_course_sections(self, 
										   period_breaks='1 week',
										   minor_period_breaks='1 day',
										   theme_seaborn_=True):

		att = self.att
		df = att.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = {}
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of assignments taken per course sections')
			user_title = _('Number of unique users taking assignments per course sections')
			ratio_title = _('Ratio of assignments taken over unique user per course sections')
			event_type = 'assignments_taken_per_course_sections'
			event_y_axis_field = 'number_assignments_taken'
			event_y_axis_label = _('Number of assignments taken')
			all_section_plots = generate_three_group_by_plots(df,
															  group_by,
															  event_title,
															  user_title,
															  ratio_title,
															  event_y_axis_field,
															  event_y_axis_label,
															  period_breaks,
															  minor_period_breaks,
															  theme_seaborn_,
															  event_type,
															  period=self.period)
			plots['all_section_plots'] = all_section_plots

		section_plots_dict = {}
		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = translate(_("Number of assignments taken in ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users taking assignments in ${title}",
									  mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of assignments taken over unique user in ${title}",
									  mapping={'title': context_name}))

			event_type = 'assignments_taken_in_%s' % (context_name.replace(' ', '_'))
			event_y_axis_field = 'number_assignments_taken'
			event_y_axis_label = _('Number of assignments taken')
			section_plots = generate_three_plots(df,
												 event_title,
												 user_title,
												 ratio_title,
												 event_y_axis_field,
												 event_y_axis_label,
												 period_breaks,
												 minor_period_breaks,
												 theme_seaborn_,
												 event_type,
												 period=self.period)
			key = 'section_%s' % (course_id)
			section_plots_dict[key] = section_plots
		plots['section_plots'] = section_plots_dict
		return plots

	def analyze_events_group_by_device_type(self, 
											period_breaks='1 week',
											minor_period_breaks='1 day',
											theme_seaborn_=True):
		att = self.att
		df = att.analyze_events_group_by_device_type()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of assignments taken during period of time')
		user_title = _('Number of unique users taking assignments during period of time')
		ratio_title = _('Ratio of assignments taken over unique user on each available date')
		event_type = 'assignments_taken_per_device_types'
		event_y_axis_field = 'number_assignments_taken'
		event_y_axis_label = _('Number of assignments taken')
		plots = generate_three_group_by_plots(df,
											  group_by,
											  event_title,
											  user_title,
											  ratio_title,
											  event_y_axis_field,
											  event_y_axis_label,
											  period_breaks,
											  minor_period_breaks,
											  theme_seaborn_,
											  event_type,
											  period=self.period)
		return plots

	def analyze_events_group_by_enrollment_type(self, 
												period_breaks='1 week',
												minor_period_breaks='1 day',
												theme_seaborn_=True):
		att = self.att
		df = att.analyze_events_group_by_enrollment_type()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'enrollment_type'
		event_title = _('Number of assignments taken during period of time')
		user_title = _('Number of unique users taking assignments during period of time')
		ratio_title = _('Ratio of assignments taken over unique user on each available date')
		event_type = 'assignments_taken_per_enrollment_types'
		event_y_axis_field = 'number_assignments_taken'
		event_y_axis_label = _('Number of assignments taken')
		plots = generate_three_group_by_plots(df,
											  group_by,
											  event_title,
											  user_title,
											  ratio_title,
											  event_y_axis_field,
											  event_y_axis_label,
											  period_breaks,
											  minor_period_breaks,
											  theme_seaborn_,
											  event_type,
											  period=self.period)
		return plots

	def analyze_assignment_taken_over_total_enrollments(self):
		"""
		TODO : fix plot when there are more than 30 unique values mapped to x
		"""
		att = self.att
		df = att.analyze_assignment_taken_over_total_enrollments()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		plot = histogram_plot_x_axis_discrete(
								df=df,
								x_axis_field='assignment_title' ,
								y_axis_field='ratio',
								x_axis_label=_('Assignments'),
								y_axis_label=_('Ratio'),
								title=_('Ratio of assignments taken over total enrollments'),
								stat='bar',
								plot_name='assignments_taken_over_total_enrollments')
		return (plot,)

	def analyze_assignment_taken_over_total_enrollments_ts(self, 
														   period_breaks='1 week',
														   minor_period_breaks='1 day',
														   theme_seaborn_=True):
		att = self.att
		df = att.analyze_assignment_taken_over_total_enrollments_ts()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		plot = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label='Date',
								y_axis_label='Ratio',
								title='Ratio of Assignments Taken over Total Enrollments',
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks,
								theme_seaborn_=theme_seaborn_,
								plot_name='assignments_taken_over_total_enrollments',
								period=self.period)
		return (plot,)

class SelfAssessmentViewsTimeseriesPlot(object):

	def __init__(self, savt):
		"""
		savt =SelfAssessmentViewsTimeseries
		"""
		self.savt = savt
		self.period = savt.period

	def analyze_events(self, period_breaks='1 week',
					   minor_period_breaks='1 day',
					   theme_seaborn_=True):
		savt = self.savt
		df = savt.analyze_events()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of self assessments viewed during period of time')
		user_title = _('Number of unique users viewing self assessments during period of time')
		ratio_title = _('Ratio of self assessments viewed over unique user on each available date')
		event_type = 'self_assessment_views'
		event_y_axis_field = 'number_self_assessments_viewed'
		event_y_axis_label = _('Number of self assessment views')
		plots = generate_three_plots(df,
									 event_title,
									 user_title,
									 ratio_title,
									 event_y_axis_field,
									 event_y_axis_label,
									 period_breaks,
									 minor_period_breaks,
									 theme_seaborn_,
									 event_type,
									 period=self.period)
		return plots

	def analyze_events_per_course_sections(self, 
										   period_breaks='1 week',
										   minor_period_breaks='1 day',
										   theme_seaborn_=True):
		savt = self.savt
		df = savt.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = {}
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of self assessments viewed per course sections')
			user_title = _('Number of unique users viewing self assessments per course sections')
			ratio_title = _('Ratio of self assessments viewed over unique user per course sections')
			event_type = 'self_assessment_views_per_course_sections'
			event_y_axis_field = 'number_self_assessments_viewed'
			event_y_axis_label = _('Number of self assessment views')
			all_section_plots = generate_three_group_by_plots(df,
															  group_by,
															  event_title,
															  user_title,
															  ratio_title,
															  event_y_axis_field,
															  event_y_axis_label,
															  period_breaks,
															  minor_period_breaks,
															  theme_seaborn_,
															  event_type,
															  period=self.period)
			plots['all_section_plots'] = all_section_plots

		section_plots_dict = {}
		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = translate(_("Number of self assessments viewed in ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users viewing self assessments in ${title}",
									  mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of self assessments viewed over unique user in ${title}",
									  mapping={'title': context_name}))
			event_type = 'self_assessment_views_in_%s' % (context_name.replace(' ', '_'))
			event_y_axis_field = 'number_self_assessments_viewed'
			event_y_axis_label = _('Number of self assessment views')
			section_plots = generate_three_plots(df,
												 event_title,
												 user_title,
												 ratio_title,
												 event_y_axis_field,
												 event_y_axis_label,
												 period_breaks,
												 minor_period_breaks,
												 theme_seaborn_,
												 event_type,
												 period=self.period)
			key = 'section_%s' % (course_id)
			section_plots_dict[key] = section_plots
		plots['section_plots'] = section_plots_dict
		return plots

	def analyze_events_group_by_device_type(self, 
											period_breaks='1 week',
											minor_period_breaks='1 day',
											theme_seaborn_=True):
		savt = self.savt
		df = savt.analyze_events_group_by_device_type()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of self assessments viewed grouped by device types')
		user_title = _('Number of unique users viewing self assessments grouped by device types')
		ratio_title = _('Ratio of self assessments viewed over unique user grouped by device types')
		event_type = 'self_assessment_views_per_device_types'
		event_y_axis_field = 'number_self_assessments_viewed'
		event_y_axis_label = _('Number of self assessment views')
		plots = generate_three_group_by_plots(df,
											  group_by,
											  event_title,
											  user_title,
											  ratio_title,
											  event_y_axis_field,
											  event_y_axis_label,
											  period_breaks,
											  minor_period_breaks,
											  theme_seaborn_,
											  event_type,
											  period=self.period)
		return plots

	def analyze_events_group_by_enrollment_type(self, 
												period_breaks='1 week',
												minor_period_breaks='1 day',
												theme_seaborn_=True):
		savt = self.savt
		df = savt.analyze_events_group_by_enrollment_type()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'enrollment_type'
		event_title = _('Number of self assessments viewed grouped by enrollment types')
		user_title = _('Number of unique users viewing self assessments grouped by enrollment types')
		ratio_title = _('Ratio of self assessments viewed over unique user grouped by enrollment types')
		event_type = 'self_assessment_views_per_enrollment_types'
		event_y_axis_field = 'number_self_assessments_viewed'
		event_y_axis_label = _('Number of self assessment views')
		plots = generate_three_group_by_plots(df,
											  group_by,
											  event_title,
											  user_title,
											  ratio_title,
											  event_y_axis_field,
											  event_y_axis_label,
											  period_breaks,
											  minor_period_breaks,
											  theme_seaborn_,
											  event_type,
											  period=self.period)
		return plots

class SelfAssessmentsTakenTimeseriesPlot(object):

	def __init__(self, satt):
		"""
		satt =SelfAssessmentsTakenTimeseries
		"""
		self.satt = satt
		self.period = satt.period

	def analyze_events(self, 
					   period_breaks='1 week',
					   minor_period_breaks='1 day',
					   theme_seaborn_=True):
		satt = self.satt
		df = satt.analyze_events()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		event_title = _('Number of self assessments taken during period of time')
		user_title = _('Number of unique users taking self assessments during period of time')
		ratio_title = _('Ratio of self assessments taken over unique user on each available date')
		event_type = 'self_assessments_taken'
		event_y_axis_field = 'number_self_assessments_taken'
		event_y_axis_label = _('Number of self assessments taken')
		plots = generate_three_plots(df,
									 event_title,
									 user_title,
									 ratio_title,
									 event_y_axis_field,
									 event_y_axis_label,
									 period_breaks,
									 minor_period_breaks,
									 theme_seaborn_,
									 event_type,
									 period=self.period)
		return plots

	def analyze_events_per_course_sections(self, 
										   period_breaks='1 week',
										   minor_period_breaks='1 day',
										   theme_seaborn_=True):
		satt = self.satt
		df = satt.analyze_events_per_course_sections()
		if df is None:
			return()

		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		course_ids = np.unique(df['course_id'].values.ravel())

		plots = {}
		if len(course_ids) > 1:
			group_by = 'context_name'
			event_title = _('Number of self assessments taken per course sections')
			user_title = _('Number of unique users taking self assessments per course sections')
			ratio_title = _('Ratio of self assessments taken over unique user per course sections')
			event_type = 'self_assessments_taken_per_course_sections'
			event_y_axis_field = 'number_self_assessments_taken'
			event_y_axis_label = _('Number of self assessments taken')
			all_section_plots = generate_three_group_by_plots(df,
															  group_by,
															  event_title,
															  user_title,
															  ratio_title,
															  event_y_axis_field,
															  event_y_axis_label,
															  period_breaks,
															  minor_period_breaks,
															  theme_seaborn_,
															  event_type,
															  period=self.period)
			plots['all_section_plots'] = all_section_plots

		section_plots_dict = {}
		for course_id in course_ids:
			new_df = df[df['course_id'] == course_id]
			context_name = new_df.iloc[0]['context_name']
			event_title = translate(_("Number of self assessments taken in ${title}",
									  mapping={'title': context_name}))

			user_title = translate(_("Number of unique users taking self assessments in ${title}",
									  mapping={'title': context_name}))

			ratio_title = translate(_("Ratio of self assessments taken over unique user in ${title}",
									  mapping={'title': context_name}))
			event_type = 'self_assessments_taken_in_%s' % (context_name.replace(' ', '_'))
			event_y_axis_field = 'number_self_assessments_taken'
			event_y_axis_label = _('Number of self assessments taken')
			section_plots = generate_three_plots(
										df,
										event_title,
										user_title,
										ratio_title,
										event_y_axis_field,
										event_y_axis_label,
										period_breaks,
										minor_period_breaks,
										theme_seaborn_,
										event_type,
										period=self.period)
			key = 'section_%s' % (course_id)
			section_plots_dict[key] = section_plots
		plots['section_plots'] = section_plots_dict
		return plots

	def analyze_events_group_by_device_type(self, 
											period_breaks='1 week',
											minor_period_breaks='1 day',
											theme_seaborn_=True):
		satt = self.satt
		df = satt.analyze_events_group_by_device_type()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'device_type'
		event_title = _('Number of self assessments taken grouped by device types')
		user_title = _('Number of unique users taking self assessments grouped by device types')
		ratio_title = _('Ratio of self assessments taken over unique user grouped by device types')
		event_type = 'self_assessments_taken_per_device_types'
		event_y_axis_field = 'number_self_assessments_taken'
		event_y_axis_label = _('Number of self assessments taken')
		plots = generate_three_group_by_plots(
										df,
									  	group_by,
									  	event_title,
										user_title,
									 	ratio_title,
										event_y_axis_field,
										event_y_axis_label,
										period_breaks,
										minor_period_breaks,
										theme_seaborn_,
										event_type,
										period=self.period)
		return plots

	def analyze_events_group_by_enrollment_type(self, 
												period_breaks='1 week',
												minor_period_breaks='1 day',
												theme_seaborn_=True):
		satt = self.satt
		df = satt.analyze_events_group_by_enrollment_type()
		if df is None :
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])

		group_by = 'enrollment_type'
		event_title = _('Number of self assessments taken grouped by enrollment types')
		user_title = _('Number of unique users taking self assessments grouped by enrollment types')
		ratio_title = _('Ratio of self assessments taken over unique user grouped by enrollment types')
		event_type = 'self_assessments_taken_per_enrollment_types'
		event_y_axis_field = 'number_self_assessments_taken'
		event_y_axis_label = _('Number of self assessments taken')
		plots = generate_three_group_by_plots(df,
											  group_by,
											  event_title,
											  user_title,
											  ratio_title,
											  event_y_axis_field,
											  event_y_axis_label,
											  period_breaks,
											  minor_period_breaks,
											  theme_seaborn_,
											  event_type,
											  period=self.period)
		return plots

	def analyze_self_assessments_taken_over_total_enrollments_ts(self,
																 period_breaks='1 week',
														   		 minor_period_breaks='1 day',
														   		 theme_seaborn_=True):
		satt = self.satt
		df = satt.analyze_self_assessments_taken_over_total_enrollments_ts()
		if df is None:
			return ()
		df.reset_index(inplace=True)
		df['timestamp_period'] = pd.to_datetime(df['timestamp_period'])
		plot = line_plot_x_axis_date(
								df=df,
								x_axis_field='timestamp_period',
								y_axis_field='ratio',
								x_axis_label='Date',
								y_axis_label='Ratio',
								title='Ratio of Self Assessments Taken over Total Enrollments',
								period_breaks=period_breaks,
								minor_breaks=minor_period_breaks,
								theme_seaborn_=theme_seaborn_,
								plot_name='self_assessments_taken_over_total_enrollments',
								period=self.period)
		return (plot,)
