"""
Bar chart wrappers for Chart.js.
"""

from .abstract_chart import AbstractChart
from . import data_config
from .cli import CSVChartCLI

default_options = dict(
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

class BarChart(AbstractChart):
    """
    A class to represent a bar chart.
    """
    def __init__(
            self,
            configuration=None,
            **kwargs
        ):
        super().__init__(configuration, **kwargs)
        self.configuration = configuration
        self.type = "bar"
        self.data = None

        # only allow data configuration if configuration is None
        if configuration is None:
            self.data = data_config.ChartData()



class TabularBarChart(BarChart):
    """
    Create a bar chart from a tabular data source.
    """
    def __init__(
            self,
            dictionaries,
            label_column,
            value_column,
            group_column=None,
            configuration=None,
            **kwargs
        ):
        """
        Create a bar chart from a tabular data source represented as a list of dictionaries.
        """
        super().__init__(configuration, **kwargs)
        self.dictionaries = dictionaries
        self.label_column = label_column
        self.value_columns = value_column
        self.group_column = group_column
        labels = []
        group_names = []
        name_to_values = {}
        for dictionary in dictionaries:
            # get the label
            label = dictionary[label_column]
            group = "value" # default group
            if group_column is not None:
                group = dictionary[group_column]
            value = dictionary[value_column]
            # add the label to the list of labels
            if label not in labels:
                labels.append(label)
            # add the group name to the list of group names
            if group not in group_names:
                group_names.append(group)
                name_to_values[group] = []
            # add the value to the list of values
            name_to_values[group].append(value)
        # add the labels
        for label in labels:
            self.add_label(label)
        # add the values
        for name in group_names:
            # add the values to the chart
            self.add_data_values(name, name_to_values[name])

class CSVBarChart(TabularBarChart):

    """
    Create a bar chart from a CSV file.
    """
    def __init__(
            self,
            csv_file,
            **kwargs
        ):
        import csv
        dictionaries = []
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            dictionaries = list(reader)
        super().__init__(dictionaries, **kwargs)

def CSVBarChartScript():
    "Command line script to create a CSV bar chart."
    cli = CSVChartCLI(CSVBarChart)
    cli.run()


# Example usages below are for testing purposes only.


def serve_example_tabular_barchart():
    """
    Serve an example tabular bar chart.
    """
    # create a TabularBarChart object
    from H5Gizmos import serve
    data = [
        {"label": "A", "group": "Red", "value": 12},
        {"label": "B", "group": "Red", "value": 1},
        {"label": "C", "group": "Red", "value": 23},
        {"label": "D", "group": "Red", "value": 5},
        {"label": "E", "group": "Red", "value": 2},
        {"label": "F", "group": "Red", "value": 3},
        {"label": "A", "group": "Blue", "value": 1},
        {"label": "B", "group": "Blue", "value": 19},
        {"label": "C", "group": "Blue", "value": 13},
        {"label": "D", "group": "Blue", "value": 15},
        {"label": "E", "group": "Blue", "value": 2},
        {"label": "F", "group": "Blue", "value": 13},
    ]
    # create a TabularBarChart object
    chart = TabularBarChart(
        dictionaries=data,
        label_column="label",
        group_column="group",
        value_column="value",
        stacked=True,
    )
    serve(chart.show())

def serve_example_bar_chart():
    """
    Serve an example bar chart.
    """
    # create a BarChart object
    from H5Gizmos import serve
    chart = BarChart()
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

if __name__ == "__main__":
    # example usage
    serve_example_bar_chart()