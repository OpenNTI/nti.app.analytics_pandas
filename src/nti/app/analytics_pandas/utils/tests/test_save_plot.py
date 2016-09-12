#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, absolute_import, division
__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from ggplot import aes
from ggplot import xlab
from ggplot import ylab
from ggplot import ggplot
from ggplot import geom_density

import numpy as np

import pandas as pd

from PIL import Image as PLTImage

from nti.analytics_pandas.utils.save_plot import save_plot_

from nti.analytics_pandas.analysis.resource_views import ResourceViewsTimeseries
from nti.analytics_pandas.analysis.plots.resource_views import ResourceViewsTimeseriesPlot

from nti.analytics_pandas.tests import AnalyticsPandasTestBase

def _build_testing_plot():
	df = pd.DataFrame({
		"x": np.arange(0, 100),
		"y": np.arange(0, 100),
		"z": np.arange(0, 100)
	})

	df['y'] = np.sin(df.y)
	df['z'] = df['y'] + 100
	df['c'] = np.where(df.x % 2 == 0, "red", "blue")

	plot = ggplot(aes(x="x", color="c"), data=df)
	plot = plot + geom_density() + xlab("x label") + ylab("y label")
	return plot

class TestSavePlot(AnalyticsPandasTestBase):

	def test_save_plot(self):
		plot = _build_testing_plot()
		image_filename = 'image_test.png'
		image = save_plot_(plot, image_filename)
		image.data.seek(0)
		im = PLTImage.open(image.data)
		im.show()
		image.data.close()

	def test_save_resource_views_plots(self):
		start_date = '2015-01-01'
		end_date = '2015-05-31'
		course_id = ['388']
		rvt = ResourceViewsTimeseries(self.session, start_date, end_date, course_id)
		rvtp = ResourceViewsTimeseriesPlot(rvt)
		plots = rvtp.explore_events()
		for plot in plots:
			image_filename = u'%s' % (plot.plot_name)
			image = save_plot_(plot.plot, image_filename, image_type='png')
			image.data.seek(0)
			im = PLTImage.open(image.data)
			im.show()
			image.data.close()
