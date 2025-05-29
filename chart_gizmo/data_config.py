

"""
Helpers for creating chart configurations.
"""

from . import raw_chart
from . import color_list

class Datum:
    """
    A class to represent a data value in a dataset.
    """

    def __init__(self, value, background_color=None, border_color=None):
        self.value = value
        self.backgroundColor = background_color
        self.borderColor = border_color

    def configure_colors(self, background_color, border_color):
        """
        Configure the colors for the datum.
        """
        if background_color is not None:
            self.backgroundColor = background_color
        if border_color is not None:
            self.borderColor = border_color
        return self

class DataSet:

    """
    A class to represent a dataset for a chart.
    """

    def __init__(
            self,
            label, values=(),
            background_color=None,
            border_color=None,
            border_width=1,
            **kwargs,
            ):
        self.label = label
        self.data = []
        for value in values:
            self.data.append(Datum(value))
        self.backgroundColor = background_color
        self.borderColor = border_color
        self.borderWidth = border_width
        # other configuration options
        self.options = kwargs

    def append_value(self, value, background_color=None, border_color=None):
        """
        Append a value to the dataset.
        """
        datum = Datum(value, background_color, border_color)
        self.data.append(datum)
        return self

    def configure_color_index(self, index, background_alpha=0.2, border_alpha=1.0):
        """
        Configure the color index for the dataset.
        """
        if self.backgroundColor is None:
            self.backgroundColor = color_list.indexed_rgbahtml(index, background_alpha)
        if self.borderColor is None:
            self.borderColor = color_list.indexed_rgbahtml(index, border_alpha)
        return self

    def as_dict(self, index=0):
        """
        Convert the dataset to a JSON compatible dictionary.
        """
        # make sure colors are set
        self.configure_color_index(index)
        # colorize all datum entries
        for datum in self.data:
            datum.configure_colors(self.backgroundColor, self.borderColor)
        result = dict(
            label=self.label,
            data=[datum.value for datum in self.data],
            backgroundColor=[datum.backgroundColor for datum in self.data],
            borderColor=[datum.borderColor for datum in self.data],
            borderWidth=self.borderWidth,
        )
        # add other options
        result.update(self.options)
        return result

class ChartData:
    """
    A class to represent the data for a chart.js Chart.
    """
    def __init__(self, labels=(), datasets=()):
        self.labels = list(labels)
        self.datasets = list(datasets)

    def add_label(self, label, values=()):
        """
        Add a label to the chart data.
        """
        ndatasets = len(self.datasets)
        # values should match the number of datasets
        if len(values) != ndatasets:
            raise ValueError(f"Number of values {len(values)} does not match number of datasets {ndatasets}")
        # add the label
        self.labels.append(label)
        # add the values to each dataset
        for i, dataset in enumerate(self.datasets):
            dataset.append_value(values[i])

    def add_dataset(self, dataset):
        """
        Add a dataset to the chart data.
        """
        # the size of the dataset should match the number of labels
        if len(dataset.data) != len(self.labels):
            raise ValueError(f"Dataset size {len(dataset.data)} does not match number of labels {len(self.labels)}")
        # add the dataset
        self.datasets.append(dataset)

    def add_data_values(self, label, values, background_color=None, border_color=None, border_width=1):
        """
        Add data values to the chart data.
        """
        # the size of the values should match the number of labels
        if len(values) != len(self.labels):
            raise ValueError(f"Values size {len(values)} does not match number of labels {len(self.labels)}")
        # create a new dataset
        dataset = DataSet(label, values, background_color, border_color, border_width)
        # add the dataset
        self.add_dataset(dataset)

    def as_dict(self):
        """
        Convert the chart data to a JSON compatible dictionary.
        """
        result = dict(
            labels=self.labels,
            datasets=[dataset.as_dict(i) for i, dataset in enumerate(self.datasets)],
        )
        return result

