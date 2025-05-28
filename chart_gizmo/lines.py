"""
LineChart class for creating line charts.
"""

import csv
from . import data_config
from .bars import BarChart, CSVBarChart
from .cli import csv_chart_cli


class LineChart(BarChart):
    """
    LineChart class for creating line charts.
    """
    def __init__(self, configuration=None, width=400, height=400, options=None):
        super().__init__(configuration, width, height)
        self.configuration = configuration
        self.type = "line"
        self.data = None
        # only allow data configuration if configuration is None
        if configuration is None:
            self.data = data_config.ChartData()
        self.options = options
        self.stacked = False
        self.logarithmic_axes = {}


class CSVLineChart(CSVBarChart):
    """
    Loads a CSV and then calls super().__init__(...) exactly
    like CSVBarChart does.
    """
    def __init__(self, csv_file, label_column, value_column, group_column=None, width=400, height=400, stacked=False, configuration=None, options=None):
        super().__init__(
            csv_file,
            label_column,
            value_column,
            group_column,
            width,
            height,
            stacked,
            configuration,
            options
        )
        # After initialization, set the chart type to line
        self.type = "line"
        self.stacked = stacked


def serve_example_line_chart():
    """
    Serve an example line chart.
    """

    from H5Gizmos import serve
    chart = LineChart()
    chart.logarithmic()
    def click_callback(event):
        print("Click event:", event)
        chart.add("click: " + repr(event))
    chart.on_click_call(click_callback)
    # add dataset names
    for name in "ABCDEF":
        chart.add_label(name)
    # add labels and data values
    chart.add_data_values("Red", [12, 1, 23, 5, 2, 3])
    chart.add_data_values("Blue", [1, 19, 13, 15, 2, 13])
    chart.add_data_values("Yellow", [2, 19, 3, 5, 12, 3])
    # return the chart object
    serve(chart.show())


def CSVLineChartScript():
    """Command‐line entrypoint for CSVLineChart"""
    csv_chart_cli(CSVLineChart)