"""
Abstract base class for Chart.js charts.
"""

from . import raw_chart
from . import data_config

class AbstractChart(raw_chart.RawChart):
    """
    Base class for all chart types (bar, line, etc.).
    Provides common functionality while specific chart types set their own type.
    """
    def __init__(
            self,
            configuration=None,
            width=400,
            height=400,
            stacked=False,
            options=None):
        super().__init__(configuration, width, height)
        self.configuration = configuration
        # Chart type should be set by subclasses
        self.type = None
        self.data = None
        self.stacked = stacked
        # only allow data configuration if configuration is None
        if configuration is None:
            self.data = data_config.ChartData()
        self.options = options

    def clear(self):
        """
        Clear the chart data.
        """
        self.data = data_config.ChartData()
        return self

    def update(self):
        """
        Update the chart data.
        """
        # update the chart data
        self.update_data(self.data.as_dict())
        return self

    def add_label(self, label, values=()):
        """
        Add a label to the chart.
        """
        if self.data is None:
            raise ValueError("Data configuration is fixed.")
        # add a label to the chart
        self.data.add_label(label, values)
        return self

    def add_dataset(self, dataset):
        """
        Add a dataset to the chart.
        """
        if self.data is None:
            raise ValueError("Data configuration is fixed.")
        # add a dataset to the chart
        self.data.add_dataset(dataset)
        return self

    def add_data_values(self, label, values=(), background_color=None, border_color=None, border_width=1):
        """
        Add data values to the chart.
        """
        if self.data is None:
            raise ValueError("Data configuration is fixed.")
        # add data values to the chart
        self.data.add_data_values(label, values, background_color, border_color, border_width)
        return self

    def get_configuration(self):
        """
        Get the chart configuration.
        """
        configuration = self.configuration
        options = self.options or self.get_default_options()
        if self.stacked is not None:
            # set the stacked option
            if "scales" not in options:
                options["scales"] = {}
            if "x" not in options["scales"]:
                options["scales"]["x"] = {}
            if "y" not in options["scales"]:
                options["scales"]["y"] = {}
            options["scales"]["x"]["stacked"] = self.stacked
            options["scales"]["y"]["stacked"] = self.stacked
        if configuration is None:
            configuration = dict(
                type=self.type,
                data=self.data.as_dict(),
                options=options,
            )
        return configuration

    def get_default_options(self):
        """
        Get default options - can be overridden by subclasses.
        """
        return dict(
            responsive=True,
            maintainAspectRatio=False,
            scales=dict(
                x=dict(
                    stacked=True,
                ),
                y=dict(
                    stacked=True,
                ),
            ),
            plugins= dict(
                datalabels= dict(
                    display= False,
                ),
            ),
        )