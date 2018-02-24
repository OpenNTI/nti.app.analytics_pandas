from reportlab.lib.colors import purple, PCMYKColor, black, pink, green, blue
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.legends import LineLegend
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.axes import XValueAxis, YValueAxis, AdjYValueAxis, NormalDateXValueAxis

import tempfile

class TimeSeriesChart(_DrawingEditorMixin,Drawing):
    '''
    Chart Features
    ==============
    '''
    def __init__(self, data=(), legend_color_name_pairs=(), width=650, height=300,
                 chart_width=600, chart_height=250, chart_y=16, chart_x=32):
        Drawing.__init__(self,width,height)
        # font
        fontName = 'Helvetica'
        fontSize = 12
        # chart
        self._add(self,LinePlot(),name='chart',validate=None,desc=None)
        self.chart.y                = chart_y
        self.chart.x                = chart_x
        self.chart.width            = chart_width
        self.chart.height           = chart_height
        # line styles
        self.chart.lines.strokeWidth     = 0
        self.chart.lines.symbol= makeMarker('FilledSquare')
        # x axis
        self.chart.xValueAxis = NormalDateXValueAxis()
        self.chart.xValueAxis.labels.fontName          = fontName
        self.chart.xValueAxis.labels.fontSize          = fontSize-1
        self.chart.xValueAxis.forceEndDate             = 1
        self.chart.xValueAxis.forceFirstDate           = 1
        self.chart.xValueAxis.labels.boxAnchor      ='autox'
        self.chart.xValueAxis.xLabelFormat          = '{d}-{MMM}'
        self.chart.xValueAxis.maximumTicks          = 5
        self.chart.xValueAxis.minimumTickSpacing    = 0.5
        self.chart.xValueAxis.niceMonth             = 0
        self.chart.xValueAxis.strokeWidth           = 1
        self.chart.xValueAxis.loLLen                = 5
        self.chart.xValueAxis.hiLLen                = 5
        self.chart.xValueAxis.gridEnd               = self.width
        self.chart.xValueAxis.gridStart             = self.chart.x-10
        # y axis
        self.chart.yValueAxis.visibleGrid           = 1
        self.chart.yValueAxis.visibleAxis=0
        self.chart.yValueAxis.labels.fontName       = fontName
        self.chart.yValueAxis.labels.fontSize       = fontSize -1
        self.chart.yValueAxis.labelTextFormat       = '%0.2f%%'
        self.chart.yValueAxis.strokeWidth           = 0.25
        self.chart.yValueAxis.visible               = 1
        self.chart.yValueAxis.labels.rightPadding   = 5
        #self.chart.yValueAxis.maximumTicks          = 6
        self.chart.yValueAxis.rangeRound            ='both'
        self.chart.yValueAxis.tickLeft              = 7.5
        self.chart.yValueAxis.minimumTickSpacing    = 0.5
        self.chart.yValueAxis.maximumTicks          = 8
        self.chart.yValueAxis.forceZero             = 0
        self.chart.yValueAxis.avoidBoundFrac = 0.1
        # legend
        self._add(self,LineLegend(),name='legend',validate=None,desc=None)
        self.legend.fontName         = fontName
        self.legend.fontSize         = fontSize
        self.legend.alignment        ='right'
        self.legend.dx           = 5
        # sample data
        #self.chart.data = [[(19010706, 3.3900000000000001), (19010806, 3.29), (19010906, 3.2999999999999998), (19011006, 3.29), (19011106, 3.3399999999999999), (19011206, 3.4100000000000001), (19020107, 3.3700000000000001), (19020207, 3.3700000000000001), (19020307, 3.3700000000000001), (19020407, 3.5), (19020507, 3.6200000000000001), (19020607, 3.46), (19020707, 3.3900000000000001)], [(19010706, 3.2000000000000002), (19010806, 3.1200000000000001), (19010906, 3.1400000000000001), (19011006, 3.1400000000000001), (19011106, 3.1699999999999999), (19011206, 3.23), (19020107, 3.1899999999999999), (19020207, 3.2000000000000002), (19020307, 3.1899999999999999), (19020407, 3.3100000000000001), (19020507, 3.4300000000000002), (19020607, 3.29), (19020707, 3.2200000000000002)]]
        self.chart.data = data
        self.chart.lines[0].strokeColor = PCMYKColor(0,100,100,40,alpha=100)
        self.chart.lines[1].strokeColor = PCMYKColor(100,0,90,50,alpha=100)
        #self.chart.xValueAxis.strokeColor             = PCMYKColor(100,60,0,50,alpha=100)
        #self.legend.colorNamePairs = [(PCMYKColor(0,100,100,40,alpha=100), 'Bovis Homes'), (PCMYKColor(100,0,90,50,alpha=100), 'HSBC Holdings')]
        self.legend.colorNamePairs = legend_color_name_pairs
        self.chart.lines.symbol.x           = 0
        self.chart.lines.symbol.strokeWidth = 0
        self.chart.lines.symbol.arrowBarbDx = 5
        self.chart.lines.symbol.strokeColor = PCMYKColor(0,0,0,0,alpha=100)
        self.chart.lines.symbol.fillColor   = None
        self.chart.lines.symbol.arrowHeight = 5
        self.legend.dxTextSpace    = 7
        self.legend.boxAnchor      = 'nw'
        self.legend.subCols.dx        = 0
        self.legend.subCols.dy        = -2
        self.legend.subCols.rpad      = 0
        self.legend.columnMaximum  = 1
        self.legend.deltax         = 1
        self.legend.deltay         = 0
        self.legend.dy             = 5
        self.legend.y              = 135
        self.legend.x              = 120
        self.chart.lines.symbol.kind        = 'FilledCross'
        self.chart.lines.symbol.size        = 5
        self.chart.lines.symbol.angle       = 45
