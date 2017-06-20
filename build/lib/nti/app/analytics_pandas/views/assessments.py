#!/usr/bin/env python
# -*- coding: utf-8 -*
"""
.. $Id: assessments.py 115516 2017-06-19 16:50:24Z austin.graham $
"""

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

from . import MessageFactory as _

from zope import interface

from nti.analytics_pandas.analysis import AssessmentEventsTimeseries
from nti.analytics_pandas.analysis import AssessmentEventsTimeseriesPlot

from nti.analytics_pandas.analysis import AssignmentViewsTimeseries
from nti.analytics_pandas.analysis import AssignmentsTakenTimeseries
from nti.analytics_pandas.analysis import AssignmentViewsTimeseriesPlot
from nti.analytics_pandas.analysis import AssignmentsTakenTimeseriesPlot

from nti.analytics_pandas.analysis import SelfAssessmentViewsTimeseries
from nti.analytics_pandas.analysis import SelfAssessmentsTakenTimeseries
from nti.analytics_pandas.analysis import SelfAssessmentViewsTimeseriesPlot
from nti.analytics_pandas.analysis import SelfAssessmentsTakenTimeseriesPlot

from nti.contenttypes.reports.interfaces import IReportContext

from .commons import get_course_names
from .commons import build_plot_images_dictionary
from .commons import build_images_dict_from_plot_dict

from .mixins import AbstractReportView

@interface.implementer(IReportContext)
class AssessmentsEventsTimeseriesContext(object):

	def __init__(self, session=None, start_date=None, end_date=None, courses=None,
				 period_breaks='1 week', minor_period_breaks='1 day',
				 theme_bw_=True, number_of_most_active_user=10, period='daily'):
		self.session = session
		self.courses = courses
		self.end_date = end_date
		self.start_date = start_date
		self.period_breaks = period_breaks
		self.theme_bw_ = theme_bw_
		self.minor_period_breaks = minor_period_breaks
		self.number_of_most_active_user = number_of_most_active_user
		self.period = period

Context = AssessmentsEventsTimeseriesContext

class AssessmentsEventsTimeseriesReportView(AbstractReportView):

	@property
	def report_title(self):
		return _('Assessments Related Events')

	def _build_data(self, data=_('sample assessments related events report')):
		keys = self.options.keys()

		if 'has_assignment_taken_data' not in keys:
			self.options['has_assignment_taken_data'] = False

		if 'has_assignment_views_data' not in keys:
			self.options['has_assignment_views_data'] = False

		if 'has_self_assessment_views_data' not in keys:
			self.options['has_self_assessment_views_data'] = False

		if 'has_self_assessments_taken_data' not in keys:
			self.options['has_self_assessments_taken_data'] = False

		if 'has_assessment_events' not in keys:
			self.options['has_assessment_events'] = False

		self.options['data'] = data
		return self.options

	def __call__(self):
		course_names = get_course_names(self.context.session, self.context.courses)
		self.options['course_names'] = ", ".join(map(str, course_names))
		data = {}

		self.att = AssignmentsTakenTimeseries(self.context.session,
											  self.context.start_date,
											  self.context.end_date,
											  self.context.courses,
											  period=self.context.period)

		if self.att.dataframe.empty:
			self.options['has_assignment_taken_data'] = False
		else:
			self.options['has_assignment_taken_data'] = True
			data = self.generate_assignments_taken_plots(data)


		self.avt = AssignmentViewsTimeseries(self.context.session,
											 self.context.start_date,
											 self.context.end_date,
											 self.context.courses,
											 period=self.context.period)

		if self.avt.dataframe.empty:
			self.options['has_assignment_views_data'] = False
		else:
			self.options['has_assignment_views_data'] = True
			data = self.generate_assignment_view_plots(data)

		self.savt = SelfAssessmentViewsTimeseries(self.context.session,
												  self.context.start_date,
												  self.context.end_date,
												  self.context.courses,
												  period=self.context.period)

		if self.savt.dataframe.empty:
			self.options['has_self_assessment_views_data'] = False
		else:
			self.options['has_self_assessment_views_data'] = True
			data = self.generate_self_assessment_view_plots(data)


		self.satt = SelfAssessmentsTakenTimeseries(self.context.session,
												   self.context.start_date,
												   self.context.end_date,
												   self.context.courses,
												   period=self.context.period)

		if self.satt.dataframe.empty:
			self.options['has_self_assessments_taken_data'] = False
		else:
			self.options['has_self_assessments_taken_data'] = True
			data = self.generate_self_assessment_taken_plots(data)

		self.aet = AssessmentEventsTimeseries(avt=self.avt, 
											  att=self.att, 
											  savt=self.savt, 
											  satt=self.satt)
		data = self.generate_combined_assessment_event_plots(data)

		self._build_data(data)
		return self.options

	def generate_assignments_taken_plots(self, data):
		self.attp = AssignmentsTakenTimeseriesPlot(self.att)
		data = self.get_assignments_taken_plots(data)
		data = self.get_assignments_taken_plots_per_device_types(data)
		data = self.get_assignments_taken_plots_per_enrollment_types(data)
		if len(self.context.courses) > 1:
			data = self.get_assignments_taken_plots_per_course_sections(data)
		else:
			self.options['has_assignment_taken_per_course_sections'] = False
		data = self.get_assignment_taken_over_total_enrollments_ts(data)
		return data

	def get_assignments_taken_plots(self, data):
		plots = self.attp.analyze_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['assignment_taken'] = build_plot_images_dictionary(plots)
		return data

	def get_assignments_taken_plots_per_device_types(self, data):
		plots = self.attp.analyze_events_group_by_device_type(self.context.period_breaks,
															  self.context.minor_period_breaks,
															  self.context.theme_bw_)
		self.options['has_assignment_taken_per_device_types'] = False
		if plots:
			data['assignment_taken_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_assignment_taken_per_device_types'] = True
		return data

	def get_assignments_taken_plots_per_enrollment_types(self, data):
		plots = self.attp.analyze_events_group_by_enrollment_type(self.context.period_breaks,
																  self.context.minor_period_breaks,
																  self.context.theme_bw_)
		self.options['has_assignment_taken_per_enrollment_types'] = False
		if plots:
			data['assignment_taken_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_assignment_taken_per_enrollment_types'] = True
		return data

	def get_assignments_taken_plots_per_course_sections(self, data):
		plots = self.attp.analyze_events_per_course_sections(self.context.period_breaks,
															 self.context.minor_period_breaks,
															 self.context.theme_bw_)
		self.options['has_assignment_taken_per_course_sections'] = False
		if plots:
			data['assignment_taken_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_assignment_taken_per_course_sections'] = True
		return data

	def get_assignment_taken_over_total_enrollments_ts(self, data):
		plots = self.attp.analyze_assignment_taken_over_total_enrollments_ts(
																self.context.period_breaks,
																self.context.minor_period_breaks,
																self.context.theme_bw_)
		self.options['has_assignment_taken_over_total_enrollments_ts'] = False
		if plots:
			data['assignment_taken_over_total_enrollments_ts'] = build_plot_images_dictionary(plots)
			self.options['has_assignment_taken_over_total_enrollments_ts'] = True
		return data

	def generate_assignment_view_plots(self, data):
		self.avtp = AssignmentViewsTimeseriesPlot(self.avt)
		data = self.get_assignment_view_plots(data)
		data = self.get_assignment_view_plots_per_device_types(data)
		data = self.get_assignment_view_plots_per_enrollment_types(data)
		if len(self.context.courses) > 1:
			data = self.get_assignment_view_plots_per_course_sections(data)
		else:
			self.options['has_assignment_views_per_course_sections'] = False
		return data

	def get_assignment_view_plots(self, data):
		plots = self.avtp.analyze_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['assignment_views'] = build_plot_images_dictionary(plots)
		return data

	def get_assignment_view_plots_per_device_types(self, data):
		plots = self.avtp.analyze_events_group_by_device_type(self.context.period_breaks,
															  self.context.minor_period_breaks,
															  self.context.theme_bw_)
		self.options['has_assignment_views_per_device_types'] = False
		if plots:
			data['assignment_views_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_assignment_views_per_device_types'] = True
		return data

	def get_assignment_view_plots_per_enrollment_types(self, data):
		plots = self.avtp.analyze_events_group_by_enrollment_type(self.context.period_breaks,
																  self.context.minor_period_breaks,
																  self.context.theme_bw_)
		self.options['has_assignment_views_per_enrollment_types'] = False
		if plots:
			data['assignment_views_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_assignment_views_per_enrollment_types'] = True
		return data

	def get_assignment_view_plots_per_course_sections(self, data):
		plots = self.avtp.analyze_events_per_course_sections(self.context.period_breaks,
															 self.context.minor_period_breaks,
															 self.context.theme_bw_)
		self.options['has_assignment_views_per_course_sections'] = False
		if plots:
			data['assignment_views_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_assignment_views_per_course_sections'] = True
		return data

	def generate_self_assessment_view_plots(self, data):
		self.savtp = SelfAssessmentViewsTimeseriesPlot(self.savt)
		data = self.get_self_assessment_view_plots(data)
		data = self.get_self_assessment_view_plots_per_device_types(data)
		data = self.get_self_assessment_view_plots_per_enrollment_types(data)
		if len(self.context.courses) > 1:
			data = self.get_self_assessment_view_plots_per_course_sections(data)
		else:
			self.options['has_self_assessment_views_per_course_sections'] = False
		return data

	def get_self_assessment_view_plots(self, data):
		plots = self.savtp.analyze_events(self.context.period_breaks,
										  self.context.minor_period_breaks,
										  self.context.theme_bw_)
		if plots:
			data['self_assessment_views'] = build_plot_images_dictionary(plots)
		return data

	def get_self_assessment_view_plots_per_device_types(self, data):
		plots = self.savtp.analyze_events_group_by_device_type(self.context.period_breaks,
															   self.context.minor_period_breaks,
															   self.context.theme_bw_)
		self.options['has_self_assessment_views_per_device_types'] = False
		if plots:
			data['self_assessment_views_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_self_assessment_views_per_device_types'] = True
		return data

	def get_self_assessment_view_plots_per_enrollment_types(self, data):
		plots = self.savtp.analyze_events_group_by_enrollment_type(self.context.period_breaks,
																   self.context.minor_period_breaks,
																   self.context.theme_bw_)
		self.options['has_self_assessment_views_per_enrollment_types'] = False
		if plots:
			data['self_assessment_views_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_self_assessment_views_per_enrollment_types'] = True
		return data

	def get_self_assessment_view_plots_per_course_sections(self, data):
		plots = self.savtp.analyze_events_per_course_sections(self.context.period_breaks,
															  self.context.minor_period_breaks,
															  self.context.theme_bw_)
		self.options['has_self_assessment_views_per_course_sections'] = False
		if plots:
			data['self_assessment_views_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_self_assessment_views_per_course_sections'] = True
			if 'all_section_plots' in data['self_assessment_views_per_course_sections'].keys():
				self.options['has_self_assessment_views_all_section_plots'] = True
			else:
				self.options['has_self_assessment_views_all_section_plots'] = False
		return data

	def generate_self_assessment_taken_plots(self, data):
		self.sattp = SelfAssessmentsTakenTimeseriesPlot(self.satt)
		data = self.get_self_assessment_taken_plots(data)
		data = self.get_self_assessment_taken_plots_per_enrollment_types(data)
		data = self.get_self_assessment_taken_plots_per_device_types(data)
		if len(self.context.courses) > 1:
			data = self.get_self_assessment_taken_plots_per_course_sections(data)
		else:
			self.options['has_self_assessments_taken_per_course_sections'] = False
		data = self.get_self_assessments_taken_over_total_enrollments_ts(data)
		return data

	def get_self_assessment_taken_plots(self, data):
		plots = self.sattp.analyze_events(self.context.period_breaks,
										  self.context.minor_period_breaks,
										  self.context.theme_bw_)
		if plots:
			data['self_assessments_taken'] = build_plot_images_dictionary(plots)
		return data

	def get_self_assessment_taken_plots_per_enrollment_types(self, data):
		plots = self.sattp.analyze_events_group_by_enrollment_type(self.context.period_breaks,
																   self.context.minor_period_breaks,
																   self.context.theme_bw_)
		self.options['has_self_assessments_taken_per_enrollment_types'] = False
		if plots:
			data['self_assessments_taken_per_enrollment_types'] = build_plot_images_dictionary(plots)
			self.options['has_self_assessments_taken_per_enrollment_types'] = True
		return data

	def get_self_assessment_taken_plots_per_device_types(self, data):
		plots = self.sattp.analyze_events_group_by_device_type(self.context.period_breaks,
															   self.context.minor_period_breaks,
															   self.context.theme_bw_)
		self.options['has_self_assessments_taken_per_device_types'] = False
		if plots:
			data['self_assessments_taken_per_device_types'] = build_plot_images_dictionary(plots)
			self.options['has_self_assessments_taken_per_device_types'] = True
		return data

	def get_self_assessment_taken_plots_per_course_sections(self, data):
		plots = self.sattp.analyze_events_per_course_sections(self.context.period_breaks,
															 self.context.minor_period_breaks,
															 self.context.theme_bw_)
		self.options['has_self_assessments_taken_per_course_sections'] = False
		if plots:
			data['self_assessments_taken_per_course_sections'] = build_images_dict_from_plot_dict(plots)
			self.options['has_self_assessments_taken_per_course_sections'] = True
			if 'all_section_plots' in data['self_assessments_taken_per_course_sections'].keys():
				self.options['has_self_assessments_taken_all_section_plots'] = True
			else:
				self.options['has_self_assessments_taken_all_section_plots'] = False
		return data

	def get_self_assessments_taken_over_total_enrollments_ts(self, data):
		plots = self.sattp.analyze_self_assessments_taken_over_total_enrollments_ts(
																self.context.period_breaks,
																self.context.minor_period_breaks,
																self.context.theme_bw_)
		self.options['has_self_assessments_taken_over_total_enrollments_ts'] = False
		if plots:
			data['self_assessments_taken_over_total_enrollments_ts'] = build_plot_images_dictionary(plots)
			self.options['has_self_assessments_taken_over_total_enrollments_ts'] = True
		return data

	def generate_combined_assessment_event_plots(self, data):
		self.aetp = AssessmentEventsTimeseriesPlot(self.aet)
		plots = self.aetp.combine_events(self.context.period_breaks,
										 self.context.minor_period_breaks,
										 self.context.theme_bw_)
		if plots:
			data['assessment_events'] = build_plot_images_dictionary(plots)
			self.options['has_assessment_events'] = True
		return data

View = AssessmentsEventsTimeseriesReport = AssessmentsEventsTimeseriesReportView
