"""
LineChart class for creating line charts.
"""

from .bars import CSVBarChart
from .cli import CSVChartCLI
from .abstract_chart import AbstractChart


class LineChart(AbstractChart):
    """
    LineChart class for creating line charts.
    """
    def __init__(self, configuration=None, width=400, height=400, stacked=False, options=None, animate=None):
        super().__init__(configuration, width, height, stacked, options, animate=animate)
        self.type = "line"

    def get_default_options(self):
        """
        Get the default options for the line chart.
        """
        default_options = super().get_default_options()

        # any update to the default options goes here
        # default_options.update({})

        return default_options


class CSVLineChart(CSVBarChart):
    """
    Loads a CSV and then calls super().__init__(...) exactly
    like CSVBarChart does.
    """
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs
        )
        # After initialization, set the chart type to line
        self.type = "line"


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
    cli = CSVChartCLI(CSVLineChart)
    cli.run()