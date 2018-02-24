#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from reportlab.graphics.charts.axes import NormalDateXValueAxis

from reportlab.graphics.charts.legends import LineLegend

from reportlab.graphics.charts.lineplots import LinePlot

from reportlab.lib.colors import PCMYKColor

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.shapes import _DrawingEditorMixin

from reportlab.graphics.widgets.markers import makeMarker

logger = __import__('logging').getLogger(__name__)


class TimeSeriesChart(_DrawingEditorMixin, Drawing):
    """
    Chart Features
    ==============
    """

    def __init__(self, data=(), legend_color_name_pairs=(), width=650, height=300,
                 chart_width=600, chart_height=250, chart_y=16, chart_x=32):
        Drawing.__init__(self, width, height)
        # font
        fontName = 'Helvetica'
        fontSize = 12
        # chart
        self._add(self, LinePlot(), name='chart', validate=None, desc=None)
        # pylint: disable=no-member
        self.chart.y = chart_y
        self.chart.x = chart_x
        self.chart.width = chart_width
        self.chart.height = chart_height
        # line styles
        self.chart.lines.strokeWidth = 0
        self.chart.lines.symbol = makeMarker('FilledSquare')
        # x axis
        self.chart.xValueAxis = NormalDateXValueAxis()
        self.chart.xValueAxis.labels.fontName = fontName
        self.chart.xValueAxis.labels.fontSize = fontSize - 1
        self.chart.xValueAxis.forceEndDate = 1
        self.chart.xValueAxis.forceFirstDate = 1
        self.chart.xValueAxis.labels.boxAnchor = 'autox'
        self.chart.xValueAxis.xLabelFormat = '{d}-{MMM}-{YYYY}'
        self.chart.xValueAxis.maximumTicks = 5
        self.chart.xValueAxis.minimumTickSpacing = 0.5
        self.chart.xValueAxis.niceMonth = 0
        self.chart.xValueAxis.strokeWidth = 1
        self.chart.xValueAxis.loLLen = 5
        self.chart.xValueAxis.hiLLen = 5
        self.chart.xValueAxis.gridEnd = self.width
        self.chart.xValueAxis.gridStart = self.chart.x - 10
        # y axis
        self.chart.yValueAxis.visibleGrid = 1
        self.chart.yValueAxis.visibleAxis = 0
        self.chart.yValueAxis.labels.fontName = fontName
        self.chart.yValueAxis.labels.fontSize = fontSize - 1
        #self.chart.yValueAxis.labelTextFormat       = '%0.2f%%'
        self.chart.yValueAxis.strokeWidth = 0.25
        self.chart.yValueAxis.visible = 1
        self.chart.yValueAxis.labels.rightPadding = 5
        #self.chart.yValueAxis.maximumTicks          = 6
        self.chart.yValueAxis.rangeRound = 'both'
        self.chart.yValueAxis.tickLeft = 7.5
        self.chart.yValueAxis.minimumTickSpacing = 0.5
        self.chart.yValueAxis.maximumTicks = 8
        self.chart.yValueAxis.forceZero = 0
        self.chart.yValueAxis.avoidBoundFrac = 0.1
        # legend
        self._add(self, LineLegend(), name='legend', validate=None, desc=None)
        self.legend.fontName = fontName
        self.legend.fontSize = fontSize
        self.legend.alignment = 'right'
        self.legend.dx = 5

        self.chart.data = data
        if legend_color_name_pairs:
            for i, color in enumerate(legend_color_name_pairs):
                self.chart.lines[i].strokeColor = color[0]
                self.legend.colorNamePairs = legend_color_name_pairs

        self.legend.colorNamePairs = legend_color_name_pairs
        self.chart.lines.symbol.x = 0
        self.chart.lines.symbol.strokeWidth = 0
        self.chart.lines.symbol.arrowBarbDx = 5
        self.chart.lines.symbol.strokeColor = PCMYKColor(0, 0, 0, 0, alpha=100)
        self.chart.lines.symbol.fillColor = None
        self.chart.lines.symbol.arrowHeight = 5
        self.legend.dxTextSpace = 7
        self.legend.boxAnchor = 'nw'
        self.legend.subCols.dx = 0
        self.legend.subCols.dy = -2
        self.legend.subCols.rpad = 0
        self.legend.columnMaximum = 1
        self.legend.deltax = 1
        self.legend.deltay = 0
        self.legend.dy = 5
        self.legend.y = 135
        self.legend.x = 120
        self.chart.lines.symbol.kind = 'FilledCross'
        self.chart.lines.symbol.size = 5
        self.chart.lines.symbol.angle = 45
