#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import equal_to
from hamcrest import has_item
from hamcrest import assert_that

from nti.analytics_pandas.analysis.assessments import AssignmentViewsTimeseries
from nti.analytics_pandas.analysis.assessments import AssessmentEventsTimeseries
from nti.analytics_pandas.analysis.assessments import AssignmentsTakenTimeseries
from nti.analytics_pandas.analysis.assessments import SelfAssessmentViewsTimeseries
from nti.analytics_pandas.analysis.assessments import SelfAssessmentsTakenTimeseries

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

class TestAssignmentViewsTimeseries(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestAssignmentViewsTimeseries, self).setUp()

	def test_analyze_events(self):
		"""
		compare result with query :
		select count(assignment_view_id), date(timestamp)
		from AssignmentViews
		where timestamp between '2015-01-01' and '2015-05-31'
		and course_id in (1024, 1025, 1026, 1027, 1028)
		group by date(timestamp)
		"""
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session,
										start_date=start_date,
										end_date=end_date,
										course_id=courses_id)
		assert_that(avt.dataframe.columns, has_item('context_name'))
		assert_that(avt.dataframe.columns, has_item('enrollment_type'))
		df = avt.analyze_events()
		assert_that(len(df.index), equal_to(6))
		assert_that(df.columns, has_item('number_assignments_viewed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_analyze_events_empty(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['xxx']
		avt = AssignmentViewsTimeseries(self.session,
										start_date=start_date,
										end_date=end_date,
										course_id=courses_id)
		assert_that(avt.dataframe.empty, equal_to(True))

	def test_analyze_events_group_by_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session,
										start_date=start_date,
										end_date=end_date,
										course_id=courses_id)
		df = avt.analyze_events_group_by_device_type()
		assert_that(df.columns, has_item('number_assignments_viewed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

		df2 = avt.analyze_events()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

	def test_analyze_events_group_by_resource_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session,
										start_date=start_date,
										end_date=end_date,
										course_id=courses_id)
		df = avt.analyze_events_group_by_resource_type()
		assert_that(df.columns, has_item('number_assignments_viewed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

		df2 = avt.analyze_events()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

	def test_analyze_events_per_course_sections(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		avt = AssignmentViewsTimeseries(self.session,
										start_date=start_date,
										end_date=end_date,
										course_id=courses_id)
		df = avt.analyze_events_per_course_sections()
		assert_that(df.columns, has_item('number_assignments_viewed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

		df2 = avt.analyze_events()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

class TestAssignmentsTakenTimeseries(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestAssignmentsTakenTimeseries, self).setUp()

	def test_dataframe(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session,
										 start_date=start_date,
										 end_date=end_date,
										 course_id=courses_id)
		assert_that(att.dataframe.columns, has_item('assignment_title'))
		assert_that(att.dataframe.columns, has_item('context_name'))
		assert_that(att.dataframe.columns, has_item('enrollment_type'))

	def test_analyze_events(self):
		"""
		compare result with query (running manually):
		select count(assignment_taken_id), date(timestamp)
		from AssignmentsTaken
		where timestamp between '2015-01-01' and '2015-05-31'
		and course_id in (1024, 1025, 1026, 1027, 1028)
		group by date(timestamp)
		"""
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session,
										 start_date=start_date,
										 end_date=end_date,
										 course_id=courses_id)
		df = att.analyze_events()
		assert_that(len(df.index), equal_to(129))
		assert_that(df.columns, has_item('number_assignments_taken'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_analyze_events_group_by_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session,
										 start_date=start_date,
										 end_date=end_date,
										 course_id=courses_id)
		df = att.analyze_events_group_by_device_type()
		assert_that(df.columns, has_item('number_assignments_taken'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

		df2 = att.analyze_events()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

	def test_analyze_events_per_course_sections(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session,
										 start_date=start_date,
										 end_date=end_date,
										 course_id=courses_id)

		df = att.analyze_events_per_course_sections()
		assert_that(df.columns, has_item('number_assignments_taken'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

		df2 = att.analyze_events()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

	def test_analyze_assignment_taken_over_total_enrollments(self):
		"""
		we may compare result with the manual sql:
		select count(*), assignment_id from AssignmentsTaken where course_id in ('1024', '1025', '1026', '1027', '1028') group by assignment_id
		"""
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session,
										 start_date=start_date,
										 end_date=end_date,
										 course_id=courses_id)
		df = att.analyze_assignment_taken_over_total_enrollments()

		number_of_assignments = att.dataframe['assignment_title'].nunique()
		assert_that(len(df.index), equal_to(number_of_assignments))

	def test_analyze_assignment_taken_over_total_enrollments_ts(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session,
										 start_date=start_date,
										 end_date=end_date,
										 course_id=courses_id)
		df = att.analyze_assignment_taken_over_total_enrollments_ts()
		assert_that(df.columns, has_item('assignments_taken'))
		assert_that(df.columns, has_item('ratio'))

	def test_analyze_analyze_question_types(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session,
										 start_date=start_date,
										 end_date=end_date,
										 course_id=courses_id)
		df = att.analyze_question_types()
		assert_that(df.columns, has_item('submission'))
		assert_that(df.columns, has_item('question_type'))

class TestSelfAssessmentViewsTimeseries(AnalyticsPandasTestBase):

	def setUp(self):
		super(TestSelfAssessmentViewsTimeseries, self).setUp()

	def test_analyze_events(self):
		"""
		compare result with query (running manually):
		select count(self_assessment_view_id), date(timestamp)
		from SelfAssessmentViews where timestamp between '2015-01-01' and '2015-05-31'
		and course_id in (1024, 1025, 1026, 1027, 1028)
		group by date(timestamp);
		"""
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		savt = SelfAssessmentViewsTimeseries(self.session,
											 start_date=start_date,
											 end_date=end_date,
											 course_id=courses_id)
		assert_that(savt.dataframe.columns, has_item('context_name'))
		assert_that(savt.dataframe.columns, has_item('enrollment_type'))
		df = savt.analyze_events()
		assert_that(len(df.index), equal_to(3))
		assert_that(df.columns, has_item('number_self_assessments_viewed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_analyze_events_group_by_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		savt = SelfAssessmentViewsTimeseries(self.session,
											 start_date=start_date,
											 end_date=end_date,
											 course_id=courses_id)
		df = savt.analyze_events_group_by_device_type()
		assert_that(df.columns, has_item('number_self_assessments_viewed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

		df2 = savt.analyze_events()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

	def test_analyze_events_group_by_resource_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		savt = SelfAssessmentViewsTimeseries(self.session,
											 start_date=start_date,
											 end_date=end_date,
											 course_id=courses_id)
		df = savt.analyze_events_group_by_resource_type()
		assert_that(df.columns, has_item('number_self_assessments_viewed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

		df2 = savt.analyze_events()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

	def test_analyze_events_per_course_sections(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		savt = SelfAssessmentViewsTimeseries(self.session,
											 start_date=start_date,
											 end_date=end_date,
											 course_id=courses_id)
		df = savt.analyze_events_per_course_sections()
		assert_that(df.columns, has_item('number_self_assessments_viewed'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

		df2 = savt.analyze_events()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

class TestSelfAssessmentsTakenTimeseries(AnalyticsPandasTestBase):

	def test_analyze_events(self):
		"""
		compare result with query (running manually):
		select count(self_assessment_id), date(timestamp)
		from SelfAssessmentsTaken where timestamp between '2015-01-01' and '2015-05-31'
		and course_id in (1024, 1025, 1026, 1027, 1028)
		group by date(timestamp);
		"""
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		satt = SelfAssessmentsTakenTimeseries(self.session,
											  start_date=start_date,
											  end_date=end_date,
											  course_id=courses_id)
		assert_that(satt.dataframe.columns, has_item('context_name'))
		assert_that(satt.dataframe.columns, has_item('enrollment_type'))
		df = satt.analyze_events()
		assert_that(len(df.index), equal_to(85))
		assert_that(df.columns, has_item('number_self_assessments_taken'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

	def test_analyze_events_group_by_device_type(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		satt = SelfAssessmentsTakenTimeseries(self.session,
											  start_date=start_date,
											  end_date=end_date,
											  course_id=courses_id)
		df = satt.analyze_events_group_by_device_type()
		assert_that(df.columns, has_item('number_self_assessments_taken'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

		df2 = satt.analyze_events()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))

	def test_analyze_events_per_course_sections(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		satt = SelfAssessmentsTakenTimeseries(self.session,
											  start_date=start_date,
											  end_date=end_date,
											  course_id=courses_id)
		df = satt.analyze_events_per_course_sections()
		assert_that(df.columns, has_item('number_self_assessments_taken'))
		assert_that(df.columns, has_item('number_of_unique_users'))
		assert_that(df.columns, has_item('ratio'))

		df2 = satt.analyze_events()
		assert_that(len(df.sum(level='timestamp_period')), equal_to(len(df2.index)))


	def test_analyze_self_assessments_taken_over_total_enrollments_ts(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		satt = SelfAssessmentsTakenTimeseries(self.session,
											  start_date=start_date,
											  end_date=end_date,
											  course_id=courses_id)
		df = satt.analyze_self_assessments_taken_over_total_enrollments_ts()
		assert_that(df.columns, has_item('ratio'))

class TestAssessmentEventsTimeseries(AnalyticsPandasTestBase):

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
		df = aet.combine_events()
		assert_that(len(df.index), equal_to(223))

	def test_over_total_enrollments(self):
		start_date = u'2015-01-01'
		end_date = u'2015-05-31'
		courses_id = ['1024', '1025', '1026', '1027', '1028']
		att = AssignmentsTakenTimeseries(self.session,
										 start_date=start_date,
										 end_date=end_date,
										 course_id=courses_id)
		satt = SelfAssessmentsTakenTimeseries(self.session,
											  start_date=start_date,
											  end_date=end_date,
											  course_id=courses_id)
		aet = AssessmentEventsTimeseries(att=att, satt=satt)
		df = aet.analyze_assessments_taken_over_total_enrollments()
		assert_that(df.columns, has_item('ratio'))
		assert_that(df.columns, has_item('assessment_type'))
