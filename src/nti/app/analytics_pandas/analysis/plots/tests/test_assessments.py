#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import assert_that

from nti.analytics_pandas.analysis.assessments import AssignmentViewsTimeseries
from nti.analytics_pandas.analysis.assessments import AssignmentsTakenTimeseries
from nti.analytics_pandas.analysis.assessments import AssessmentEventsTimeseries
from nti.analytics_pandas.analysis.assessments import SelfAssessmentViewsTimeseries
from nti.analytics_pandas.analysis.assessments import SelfAssessmentsTakenTimeseries

from nti.analytics_pandas.analysis.plots.assessments import AssignmentViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.assessments import AssignmentsTakenTimeseriesPlot
from nti.analytics_pandas.analysis.plots.assessments import AssessmentEventsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.assessments import SelfAssessmentViewsTimeseriesPlot
from nti.analytics_pandas.analysis.plots.assessments import SelfAssessmentsTakenTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestAssignmentViewsPlot(AnalyticsPandasTestBase):

	def test_analyze_events(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date,
										end_date=end_date, course_id=courses_id)
		avtp = AssignmentViewsTimeseriesPlot(avt)
		_ = avtp.analyze_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_weekly(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date,
										end_date=end_date, course_id=courses_id,
										time_period='weekly')
		avtp = AssignmentViewsTimeseriesPlot(avt)
		_ = avtp.analyze_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_events_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date,
										end_date=end_date, course_id=courses_id)
		avtp = AssignmentViewsTimeseriesPlot(avt)
		_ = avtp.analyze_events(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))

	def test_analyze_events_group_by_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date,
										end_date=end_date, course_id=courses_id)
		avtp = AssignmentViewsTimeseriesPlot(avt)
		_ = avtp.analyze_events_group_by_device_type(period_breaks='1 day',
													 minor_period_breaks=None)

	def test_analyze_events_group_by_device_type_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date,
										end_date=end_date, course_id=courses_id)
		avtp = AssignmentViewsTimeseriesPlot(avt)
		_ = avtp.analyze_events_group_by_device_type(period_breaks='1 day',
													 minor_period_breaks=None)
		assert_that(len(_), equal_to(0))

	def test_analyze_events_group_by_enrollment_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date,
										end_date=end_date, course_id=courses_id)
		avtp = AssignmentViewsTimeseriesPlot(avt)
		_ = avtp.analyze_events_group_by_enrollment_type(period_breaks='1 day',
														 minor_period_breaks=None)

	def test_analyze_events_group_by_enrollment_type_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date,
										end_date=end_date, course_id=courses_id)
		avtp = AssignmentViewsTimeseriesPlot(avt)
		_ = avtp.analyze_events_group_by_enrollment_type(period_breaks='1 day',
														 minor_period_breaks=None)
		assert_that(len(_), equal_to(0))

	def test_analyze_events_per_course_sections(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date,
										end_date=end_date, course_id=courses_id)
		avtp = AssignmentViewsTimeseriesPlot(avt)
		_ = avtp.analyze_events_per_course_sections(period_breaks='1 day',
													 minor_period_breaks=None)

	def test_analyze_events_per_course_sections_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		avt = AssignmentViewsTimeseries(self.session, start_date=start_date,
										end_date=end_date, course_id=courses_id)
		avtp = AssignmentViewsTimeseriesPlot(avt)
		_ = avtp.analyze_events_per_course_sections(period_breaks='1 day',
													 minor_period_breaks=None)
		assert_that(len(_), equal_to(0))

class TestAssignmentsTakenPlot(AnalyticsPandasTestBase):

	def test_analyze_events(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date,
										 end_date=end_date, course_id=courses_id)
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_events(period_breaks='1 week', minor_period_breaks='1 day')

	def test_analyze_events_weekly(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date,
										 end_date=end_date, course_id=courses_id,
										 time_period='weekly')
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_events_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date,
										 end_date=end_date, course_id=courses_id)
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_events(period_breaks='1 week', minor_period_breaks='1 day')
		assert_that(len(_), equal_to(0))

	def test_analyze_events_per_course_sections(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date,
										 end_date=end_date, course_id=courses_id)
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_events_per_course_sections(period_breaks='1 week',
													 minor_period_breaks='1 day')

	def test_analyze_events_per_course_sections_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date,
										 end_date=end_date, course_id=courses_id)
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_events_per_course_sections(period_breaks='1 week',
													 minor_period_breaks='1 day')
		assert_that(len(_), equal_to(0))

	def test_analyze_events_per_device_types(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date,
										 end_date=end_date, course_id=courses_id)
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_events_group_by_device_type(period_breaks='1 week',
													 minor_period_breaks='1 day')

	def test_analyze_events_per_device_types_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date,
										 end_date=end_date, course_id=courses_id)
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_events_group_by_device_type(period_breaks='1 week',
													 minor_period_breaks='1 day')
		assert_that(len(_), equal_to(0))

	def test_analyze_events_per_enrollment_types(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date,
										 end_date=end_date, course_id=courses_id)
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_events_group_by_enrollment_type(period_breaks='1 week',
													 minor_period_breaks='1 day')

	def test_analyze_events_per_enrollment_types_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date,
										 end_date=end_date, course_id=courses_id)
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_events_group_by_enrollment_type(period_breaks='1 week',
													 minor_period_breaks='1 day')
		assert_that(len(_), equal_to(0))

	def test_analyze_assignment_taken_over_total_enrollments(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date,
										 end_date=end_date, course_id=courses_id)
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_assignment_taken_over_total_enrollments()

	def test_analyze_assignment_taken_over_total_enrollments_ts(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date,
										 end_date=end_date, course_id=courses_id)
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_assignment_taken_over_total_enrollments_ts()

	def test_analyze_assignment_taken_over_total_enrollments_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		att = AssignmentsTakenTimeseries(self.session, start_date=start_date,
										 end_date=end_date, course_id=courses_id)
		attp = AssignmentsTakenTimeseriesPlot(att)
		_ = attp.analyze_assignment_taken_over_total_enrollments()
		assert_that(len(_), equal_to(0))

class TestSelfAssessmentViewsPlot(AnalyticsPandasTestBase):

	def test_analyze_events(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		savt = SelfAssessmentViewsTimeseries(self.session, start_date=start_date,
											 end_date=end_date, course_id=courses_id)
		savtp = SelfAssessmentViewsTimeseriesPlot(savt)
		_ = savtp.analyze_events(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_weekly(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		savt = SelfAssessmentViewsTimeseries(self.session, start_date=start_date,
											 end_date=end_date, course_id=courses_id,
											 time_period='weekly')
		savtp = SelfAssessmentViewsTimeseriesPlot(savt)
		_ = savtp.analyze_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_events_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		savt = SelfAssessmentViewsTimeseries(self.session, start_date=start_date,
											 end_date=end_date, course_id=courses_id)
		savtp = SelfAssessmentViewsTimeseriesPlot(savt)
		_ = savtp.analyze_events(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))

	def test_analyze_events_per_course_sections(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		savt = SelfAssessmentViewsTimeseries(self.session, start_date=start_date,
											 end_date=end_date, course_id=courses_id)
		savtp = SelfAssessmentViewsTimeseriesPlot(savt)
		_ = savtp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks=None)

	def test_analyze_events_per_course_sections_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		savt = SelfAssessmentViewsTimeseries(self.session, start_date=start_date,
											 end_date=end_date, course_id=courses_id)
		savtp = SelfAssessmentViewsTimeseriesPlot(savt)
		_ = savtp.analyze_events_per_course_sections(period_breaks='1 day', minor_period_breaks=None)
		assert_that(len(_), equal_to(0))

	def test_analyze_events_group_by_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		savt = SelfAssessmentViewsTimeseries(self.session, start_date=start_date,
											 end_date=end_date, course_id=courses_id)
		savtp = SelfAssessmentViewsTimeseriesPlot(savt)
		_ = savtp.analyze_events_group_by_device_type(period_breaks='1 day',
													  minor_period_breaks=None)

	def test_analyze_events_group_by_device_type_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		savt = SelfAssessmentViewsTimeseries(self.session, start_date=start_date,
											 end_date=end_date, course_id=courses_id)
		savtp = SelfAssessmentViewsTimeseriesPlot(savt)
		_ = savtp.analyze_events_group_by_device_type(period_breaks='1 day',
													  minor_period_breaks=None)
		assert_that(len(_), equal_to(0))

	def test_analyze_events_group_by_enrollment_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		savt = SelfAssessmentViewsTimeseries(self.session, start_date=start_date,
											 end_date=end_date, course_id=courses_id)
		savtp = SelfAssessmentViewsTimeseriesPlot(savt)
		_ = savtp.analyze_events_group_by_enrollment_type(period_breaks='1 day',
													  minor_period_breaks=None)

	def test_analyze_events_group_by_enrollment_type_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		savt = SelfAssessmentViewsTimeseries(self.session, start_date=start_date,
											 end_date=end_date, course_id=courses_id)
		savtp = SelfAssessmentViewsTimeseriesPlot(savt)
		_ = savtp.analyze_events_group_by_enrollment_type(period_breaks='1 day',
													  minor_period_breaks=None)
		assert_that(len(_), equal_to(0))

class TestSelfAssessmentsTakenPlot(AnalyticsPandasTestBase):

	def test_analyze_events(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		satt = SelfAssessmentsTakenTimeseries(self.session, start_date=start_date,
											  end_date=end_date, course_id=courses_id)
		sattp = SelfAssessmentsTakenTimeseriesPlot(satt)
		_ = sattp.analyze_events(period_breaks='1 week', minor_period_breaks='1 day')

	def test_analyze_events_weekly(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		satt = SelfAssessmentsTakenTimeseries(self.session, start_date=start_date,
											  end_date=end_date, course_id=courses_id,
											  time_period='weekly')
		sattp = SelfAssessmentsTakenTimeseriesPlot(satt)
		_ = sattp.analyze_events(period_breaks='1 week', minor_period_breaks=None)

	def test_analyze_events_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		satt = SelfAssessmentsTakenTimeseries(self.session, start_date=start_date,
											  end_date=end_date, course_id=courses_id)
		sattp = SelfAssessmentsTakenTimeseriesPlot(satt)
		_ = sattp.analyze_events(period_breaks='1 week', minor_period_breaks='1 day')
		assert_that(len(_), equal_to(0))

	def test_analyze_events_per_course_sections(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		satt = SelfAssessmentsTakenTimeseries(self.session, start_date=start_date,
											  end_date=end_date, course_id=courses_id)
		sattp = SelfAssessmentsTakenTimeseriesPlot(satt)
		_ = sattp.analyze_events_per_course_sections(period_breaks='1 week', minor_period_breaks='1 day')

	def test_analyze_events_per_course_sections_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		satt = SelfAssessmentsTakenTimeseries(self.session, start_date=start_date,
											  end_date=end_date, course_id=courses_id)
		sattp = SelfAssessmentsTakenTimeseriesPlot(satt)
		_ = sattp.analyze_events_per_course_sections(period_breaks='1 week', minor_period_breaks='1 day')
		assert_that(len(_), equal_to(0))

	def test_analyze_events_group_by_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		satt = SelfAssessmentsTakenTimeseries(self.session, start_date=start_date,
											  end_date=end_date, course_id=courses_id)
		sattp = SelfAssessmentsTakenTimeseriesPlot(satt)
		_ = sattp.analyze_events_group_by_device_type(period_breaks='1 week',
													  minor_period_breaks='1 day')

	def test_analyze_events_group_by_device_type_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		satt = SelfAssessmentsTakenTimeseries(self.session, start_date=start_date,
											  end_date=end_date, course_id=courses_id)
		sattp = SelfAssessmentsTakenTimeseriesPlot(satt)
		_ = sattp.analyze_events_group_by_device_type(period_breaks='1 week',
													  minor_period_breaks='1 day')
		assert_that(len(_), equal_to(0))

	def test_analyze_events_group_by_enrollment_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		satt = SelfAssessmentsTakenTimeseries(self.session, start_date=start_date,
											  end_date=end_date, course_id=courses_id)
		sattp = SelfAssessmentsTakenTimeseriesPlot(satt)
		_ = sattp.analyze_events_group_by_enrollment_type(period_breaks='1 week',
													  minor_period_breaks='1 day')

	def test_analyze_self_assessments_taken_over_total_enrollments_ts(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		satt = SelfAssessmentsTakenTimeseries(self.session, start_date=start_date,
											  end_date=end_date, course_id=courses_id)
		sattp = SelfAssessmentsTakenTimeseriesPlot(satt)
		_ = sattp.analyze_self_assessments_taken_over_total_enrollments_ts(period_breaks='1 week',
													  					   minor_period_breaks='1 day')

	def test_analyze_events_group_by_enrollment_type_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		satt = SelfAssessmentsTakenTimeseries(self.session, start_date=start_date,
											  end_date=end_date, course_id=courses_id)
		sattp = SelfAssessmentsTakenTimeseriesPlot(satt)
		_ = sattp.analyze_events_group_by_enrollment_type(period_breaks='1 week',
													  minor_period_breaks='1 day')
		assert_that(len(_), equal_to(0))

class TestAssessmentEventsPlot(AnalyticsPandasTestBase):

	def test_combine_events(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session,
										start_date=start_date,
										end_date=end_date,
										course_id=courses_id)

		att = AssignmentsTakenTimeseries(self.session,
										 start_date=start_date,
										 end_date=end_date,
										 course_id=courses_id)
		savt = SelfAssessmentViewsTimeseries(self.session,
											 start_date=start_date,
											 end_date=end_date,
											 course_id=courses_id)
		satt = SelfAssessmentsTakenTimeseries(self.session,
											  start_date=start_date,
											  end_date=end_date,
											  course_id=courses_id)
		aet = AssessmentEventsTimeseries(avt=avt, att=att, savt=savt, satt=satt)
		aetp = AssessmentEventsTimeseriesPlot(aet)
		_ = aetp.combine_events()

	def test_combine_events_weekly(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session,
										start_date=start_date,
										end_date=end_date,
										course_id=courses_id,
										time_period='weekly')

		att = AssignmentsTakenTimeseries(self.session,
										 start_date=start_date,
										 end_date=end_date,
										 course_id=courses_id,
										 time_period='weekly')
		savt = SelfAssessmentViewsTimeseries(self.session,
											 start_date=start_date,
											 end_date=end_date,
											 course_id=courses_id,
											 time_period='weekly')
		satt = SelfAssessmentsTakenTimeseries(self.session,
											  start_date=start_date,
											  end_date=end_date,
											  course_id=courses_id,
											  time_period='weekly')
		aet = AssessmentEventsTimeseries(avt=avt, att=att, savt=savt, satt=satt)
		aetp = AssessmentEventsTimeseriesPlot(aet)
		_ = aetp.combine_events(period_breaks='1 week', minor_period_breaks=None, theme_seaborn_=True)

	def test_combine_events_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['123']
		avt = AssignmentViewsTimeseries(self.session,
										start_date=start_date,
										end_date=end_date,
										course_id=courses_id)

		att = AssignmentsTakenTimeseries(self.session,
										 start_date=start_date,
										 end_date=end_date,
										 course_id=courses_id)
		savt = SelfAssessmentViewsTimeseries(self.session,
											 start_date=start_date,
											 end_date=end_date,
											 course_id=courses_id)
		satt = SelfAssessmentsTakenTimeseries(self.session,
											  start_date=start_date,
											  end_date=end_date,
											  course_id=courses_id)
		aet = AssessmentEventsTimeseries(avt=avt, att=att, savt=savt, satt=satt)
		aetp = AssessmentEventsTimeseriesPlot(aet)
		_ = aetp.combine_events()
		assert_that(len(_), equal_to(0))

	def test_analyze_assessments_taken_over_total_enrollments(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session,
										start_date=start_date,
										end_date=end_date,
										course_id=courses_id)

		att = AssignmentsTakenTimeseries(self.session,
										 start_date=start_date,
										 end_date=end_date,
										 course_id=courses_id)
		savt = SelfAssessmentViewsTimeseries(self.session,
											 start_date=start_date,
											 end_date=end_date,
											 course_id=courses_id)
		satt = SelfAssessmentsTakenTimeseries(self.session,
											  start_date=start_date,
											  end_date=end_date,
											  course_id=courses_id)
		aet = AssessmentEventsTimeseries(avt=avt, att=att, savt=savt, satt=satt)
		aetp = AssessmentEventsTimeseriesPlot(aet)
		_ = aetp.analyze_assessments_taken_over_total_enrollments()
