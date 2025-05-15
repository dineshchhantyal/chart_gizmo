"""
Bar chart wrappers for Chart.js.
"""

from . import raw_chart
from . import data_config

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

class BarChart(raw_chart.RawChart):
    """
    A class to represent a bar chart.
    """
    def __init__(
            self, 
            configuration=None, 
            width=400, 
            height=400, 
            stacked=False, options=None):
        super().__init__(configuration, width, height)
        self.configuration = configuration
        self.type = "bar"
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
        configuration = self.configuration
        options = self.options or default_options
        if self.stacked is not None:
            # set the stacked option
            options["scales"]["x"]["stacked"] = self.stacked
            options["scales"]["y"]["stacked"] = self.stacked
        if configuration is None:
            configuration = dict(
                type=self.type,
                data=self.data.as_dict(),
                options=self.options or default_options,
            )
        return configuration
 

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
            width=400,
            height=400,
            stacked=False,
            configuration=None,
            options=None
        ):
        """
        Create a bar chart from a tabular data source represented as a list of dictionaries.
        """
        super().__init__(configuration, width, height, stacked, options)
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
            label_column,
            value_column,
            group_column=None,
            width=400,
            height=400,
            stacked=False,
            configuration=None,
            options=None
        ):
        import csv
        dictionaries = []
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            dictionaries = list(reader)
        super().__init__(dictionaries, label_column, value_column, group_column, width, height, stacked, configuration, options)

def CSVBarChartScript():
    "Command line script to create a CSV bar chart."
    import argparse
    import sys
    import os
    from H5Gizmos import serve
    import csv
    parser = argparse.ArgumentParser(description="Create a bar chart from a CSV file.")
    parser.add_argument("csv_file", help="CSV file to read.")
    # other arguments are optional with None as default and abbreviations
    parser.add_argument("-l", "--label_column", help="Label column name.")
    parser.add_argument("-v", "--value_column", help="Value column name.")
    parser.add_argument("-g", "--group_column", help="Group column name.")
    parser.add_argument("-w", "--width", type=int, default=400, help="Width of the chart.")
    #parser.add_argument("-h", "--height", type=int, default=400, help="Height of the chart.")
    # get the arguments
    args = parser.parse_args()
    # check if the file exists
    csv_file = args.csv_file
    if not os.path.exists(csv_file):
        print(f"File {csv_file} does not exist.")
        sys.exit(1)
    label_column = args.label_column
    value_column = args.value_column
    group_column = args.group_column
    width = args.width
    #height = args.height
    # use the first 3 columns if not specified
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        if label_column is None:
            label_column = headers[0]
        if value_column is None:
            value_column = headers[1]
        if group_column is None:
            group_column = headers[2]
    # create the chart
    chart = CSVBarChart(
        csv_file,
        label_column=label_column,
        value_column=value_column,
        group_column=group_column,
        width=width,
        #height=height,
    )
    # serve the chart
    serve(chart.show())

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