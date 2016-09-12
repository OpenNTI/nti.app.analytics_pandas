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

from zope.i18n import translate

from ggplot import aes
from ggplot import xlab
from ggplot import ylab
from ggplot import ylim
from ggplot import theme
from ggplot import ggplot
from ggplot import ggtitle
from ggplot import geom_bar
from ggplot import geom_line
from ggplot import geom_point
from ggplot import facet_wrap
from ggplot import date_breaks
from ggplot import date_format
from ggplot import element_text
from ggplot import scale_x_date
from ggplot import theme_seaborn
from ggplot import geom_histogram
from ggplot import scale_x_discrete

from ...utils import Plot

DATE_FORMAT = "%Y-%m-%d"

def line_plot_x_axis_date(df,
						  x_axis_field,
						  y_axis_field,
						  x_axis_label,
						  y_axis_label,
						  title,
						  period_breaks,
						  minor_breaks=None,
						  theme_seaborn_=True,
						  plot_name=None,
						  period=None):

	if period is not None:
		title = generate_plot_title(title, period)

	y_max = pd.Series.max(df[y_axis_field]) + 1
	line_plot = \
		ggplot(df, aes(x=x_axis_field, y=y_axis_field)) + \
		geom_line() + \
		geom_point() + \
		ggtitle(_(title)) + \
		ylab(_(y_axis_label)) + \
		xlab(_(x_axis_label)) + \
		ylim(0, y_max)

	if period_breaks == '7 days':
		print(df)
	if period_breaks is not None:
		breaks = date_breaks(period_breaks)
	else:
		breaks = period_breaks

	if minor_breaks is not None:
		line_plot = line_plot + scale_x_date(breaks=breaks,
											 minor_breaks=minor_breaks,
											 labels=date_format(DATE_FORMAT))
	else:
		line_plot = line_plot + scale_x_date(breaks=breaks,
											 labels=date_format(DATE_FORMAT))
	if theme_seaborn_:
		line_plot = line_plot + theme_seaborn()

	if plot_name is not None:
		plot = Plot.process(plot_name, line_plot)
		return plot

	return line_plot

def scatter_plot_x_axis_date(df,
						 	 x_axis_field,
						  	 y_axis_field,
						  	 x_axis_label,
						  	 y_axis_label,
						  	 title,
						  	 period_breaks,
						  	 minor_breaks=None,
						  	 theme_seaborn_=True,
						  	 plot_name=None,
						  	 period=None):

	if period is not None:
		title = generate_plot_title(title, period)

	y_max = pd.Series.max(df[y_axis_field]) + 1
	scatter_plot = \
		ggplot(df, aes(x=x_axis_field, y=y_axis_field)) + \
		geom_point() + \
		ggtitle(_(title)) + \
		theme(title=element_text(size=10, face="bold")) + \
		ylab(_(y_axis_label)) + \
		xlab(_(x_axis_label)) + \
		ylim(0, y_max)

	scatter_plot = scatter_plot + scale_x_date(breaks=period_breaks,
											   minor_breaks=minor_breaks,
											   labels=date_format(DATE_FORMAT))

	if theme_seaborn_:
		scatter_plot = scatter_plot + theme_seaborn()

	if plot_name is not None:
		plot = Plot.process(plot_name, scatter_plot)
		return plot

	return scatter_plot

def group_line_plot_x_axis_date(df,
								x_axis_field,
								y_axis_field,
								x_axis_label,
								y_axis_label,
								title,
								period_breaks,
								group_by,
								minor_breaks=None,
								theme_seaborn_=True,
								plot_name=None,
								period=None):
	if period is not None:
		title = generate_plot_title(title, period)

	y_max = pd.Series.max(df[y_axis_field]) + 1
	line_plot = \
		ggplot(df, aes(x=x_axis_field, y=y_axis_field, color=group_by)) + \
		geom_line() + \
		geom_point() + \
		ggtitle(_(title)) + \
		theme(title=element_text(size=10, face="bold")) + \
		ylab(_(y_axis_label)) + \
		xlab(_(x_axis_label)) + \
		ylim(0, y_max)

	if minor_breaks is not None:
		line_plot = line_plot + scale_x_date(breaks=period_breaks,
											 minor_breaks=minor_breaks,
											 labels=date_format(DATE_FORMAT))
	else:
		line_plot = line_plot + scale_x_date(breaks=period_breaks,
											 labels=date_format(DATE_FORMAT))
	if theme_seaborn_ :
		line_plot = line_plot + theme_seaborn()

	if plot_name is not None:
		plot = Plot.process(plot_name, line_plot)
		return plot

	return line_plot

def group_scatter_plot_x_axis_date(df,
								   x_axis_field,
								   y_axis_field,
								   x_axis_label,
								   y_axis_label,
								   title,
								   period_breaks,
								   group_by,
								   minor_breaks=None,
								   theme_seaborn_=True,
								   plot_name=None,
								   period=None):
	if period is not None:
		title = generate_plot_title(title, period)

	y_max = pd.Series.max(df[y_axis_field]) + 1
	scatter_plot = \
		ggplot(df, aes(x=x_axis_field, y=y_axis_field, color=group_by)) + \
		geom_point() + \
		ggtitle(_(title)) + \
		theme(title=element_text(size=10, face="bold")) + \
		ylab(_(y_axis_label)) + \
		xlab(_(x_axis_label)) + \
		ylim(0, y_max)

	if minor_breaks is not None:
		scatter_plot = scatter_plot + scale_x_date(breaks=period_breaks,
											 	   minor_breaks=minor_breaks,
											 	   labels=date_format(DATE_FORMAT))
	else:
		scatter_plot = scatter_plot + scale_x_date(breaks=period_breaks,
											 	   labels=date_format(DATE_FORMAT))
	if theme_seaborn_:
		scatter_plot = scatter_plot + theme_seaborn()

	if plot_name is not None:
		plot = Plot.process(plot_name, scatter_plot)
		return plot

	return scatter_plot

def facet_line_plot_x_axis_date(df,
								x_axis_field,
								y_axis_field,
								x_axis_label,
								y_axis_label,
								title,
								period_breaks,
								group_by,
								facet,
								minor_breaks=None,
								scales='free',
								text_size=8):
	line_plot = \
		ggplot(df, aes(x=x_axis_field, y=y_axis_field, color=group_by)) + \
		geom_line() + \
		geom_point() + \
		ggtitle(_(title)) + \
		theme(title=element_text(size=text_size, face="bold")) + \
		ylab(_(y_axis_label)) + \
		xlab(_(x_axis_label)) + \
		facet_wrap(facet, scales=scales)

	if minor_breaks is not None:
		line_plot = line_plot + scale_x_date(breaks=period_breaks,
											 minor_breaks=minor_breaks,
											 labels=date_format(DATE_FORMAT))
	else:
		line_plot = line_plot + scale_x_date(breaks=period_breaks,
											 labels=date_format(DATE_FORMAT))
	return line_plot

def histogram_plot(df,
				   x_axis_field,
				   y_axis_field,
				   x_axis_label,
				   y_axis_label,
				   title,
				   stat,
				   plot_name=None):
	hist_plot = ggplot(df, aes(x=x_axis_field, y=y_axis_field)) + \
				geom_histogram(stat=stat) + \
				ggtitle(_(title)) + \
				theme(title=element_text(size=10, face="bold")) + \
				ylab(_(y_axis_label)) + \
				xlab(_(x_axis_label))

	if plot_name is not None:
		plot = Plot.process(plot_name, hist_plot)
		return plot

	return hist_plot

def histogram_plot_x_axis_discrete(df,
								   x_axis_field,
								   y_axis_field,
								   x_axis_label,
								   y_axis_label,
								   title,
								   stat,
								   theme_seaborn_=True,
								   plot_name=None):
	hist_plot = ggplot(df, aes(x=x_axis_field, y=y_axis_field)) + \
				geom_histogram(stat=stat) + \
				ggtitle(_(title)) + \
				theme(title=element_text(size=10, face="bold"),
					  axis_text_x=element_text(angle=15, hjust=1)) + \
				ylab(_(y_axis_label)) + \
				xlab(_(x_axis_label)) + \
				scale_x_discrete(x_axis_field)

	if plot_name is not None:
		plot = Plot.process(plot_name, hist_plot)
		return plot

	return hist_plot

def bar_plot_with_fill(df,
					   x_axis_field,
					   y_axis_field,
					   x_axis_label,
					   y_axis_label,
					   title,
					   stat,
					   fill,
					   theme_seaborn_=True,
					   plot_name=None):

	bar_plot = ggplot(df, aes(x=x_axis_field, y=y_axis_field, fill=fill)) + \
				geom_bar(stat=stat) + \
				ggtitle(_(title)) + \
				theme(title=element_text(size=10, face="bold"),
					  axis_text_x=element_text(angle=15, hjust=1)) + \
				ylab(_(y_axis_label)) + \
				xlab(_(x_axis_label))

	if plot_name is not None:
		plot = Plot.process(plot_name, bar_plot)
		return plot

	return bar_plot

def generate_plot_names(event_type):

	event_name = None
	user_event_name = None
	ratio_event_name = None

	if event_type is not None:
		event_name = 'event_%s' % event_type
		user_event_name = 'user_%s' % event_type
		ratio_event_name = 'ratio_%s' % event_type

	return (event_name, user_event_name, ratio_event_name)

def generate_plot_title(title, period):
	if period is not None:
		title = translate(_('${title} : ${period}',
							mapping={'title':title, 'period':period}))
	return title

def generate_three_plots(df, event_title, user_title, ratio_title,
						 event_y_axis_field, event_y_axis_label,
						 period_breaks, minor_period_breaks, theme_seaborn_,
						 event_type=None, period=None):

	event_name, user_event_name, ratio_event_name = generate_plot_names(event_type)
	event_title = generate_plot_title(event_title, period)
	user_title = generate_plot_title(user_title, period)
	ratio_title = generate_plot_title(ratio_title, period)

	plot_event = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field=event_y_axis_field,
									x_axis_label=_('Date'),
									y_axis_label=event_y_axis_label,
									title=event_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_,
									plot_name=event_name)

	plot_unique_users = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='number_of_unique_users',
									x_axis_label=_('Date'),
									y_axis_label=_('Number of unique users'),
									title=user_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_,
									plot_name=user_event_name)

	plot_ratio = line_plot_x_axis_date(
									df=df,
									x_axis_field='timestamp_period',
									y_axis_field='ratio',
									x_axis_label=_('Date'),
									y_axis_label=_('Ratio'),
									title=ratio_title,
									period_breaks=period_breaks,
									minor_breaks=minor_period_breaks,
									theme_seaborn_=theme_seaborn_,
									plot_name=ratio_event_name)

	return (plot_event, plot_unique_users, plot_ratio)

def generate_three_group_by_plots(df, group_by, event_title, user_title, ratio_title,
								  event_y_axis_field, event_y_axis_label,
								  period_breaks, minor_period_breaks, theme_seaborn_,
								  event_type=None, period=None):

	if 'device_type' in df.columns and 'device_type' in group_by:
		group_by = 'application_type'
		df.rename(columns={	'device_type'	:'application_type'},
				  inplace=True)
		event_title = event_title.replace('device', 'application')
		user_title = user_title.replace('device', 'application')
		ratio_title = ratio_title.replace('device', 'application')

	event_name, user_event_name, ratio_event_name = generate_plot_names(event_type)
	event_title = generate_plot_title(event_title, period)
	user_title = generate_plot_title(user_title, period)
	ratio_title = generate_plot_title(ratio_title, period)

	plot_events = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field=event_y_axis_field,
										x_axis_label=_('Date'),
										y_axis_label=event_y_axis_label,
										title=event_title,
										period_breaks=period_breaks,
										group_by=group_by,
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_,
										plot_name=event_name)

	plot_unique_users = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='number_of_unique_users',
										x_axis_label=_('Date'),
										y_axis_label=_('Number of unique users'),
										title=user_title,
										period_breaks=period_breaks,
										group_by=group_by,
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_,
										plot_name=user_event_name)

	plot_ratio = group_line_plot_x_axis_date(
										df=df,
										x_axis_field='timestamp_period',
										y_axis_field='ratio',
										x_axis_label=_('Date'),
										y_axis_label=_('Ratio'),
										title=ratio_title,
										period_breaks=period_breaks,
										group_by=group_by,
										minor_breaks=minor_period_breaks,
										theme_seaborn_=theme_seaborn_,
										plot_name=ratio_event_name)

	return (plot_events, plot_unique_users, plot_ratio)
