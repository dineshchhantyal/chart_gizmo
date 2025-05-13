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
        if self.stacked:
            options["scales"]["x"]["stacked"] = True
            options["scales"]["y"]["stacked"] = True
        if configuration is None:
            configuration = dict(
                type=self.type,
                data=self.data.as_dict(),
                options=self.options or default_options,
            )
        return configuration
 
class CSVBarChart(BarChart):
    """
    Create a bar chart from a CSV file.
    """
    def __init__(self, filename, width=400, height=400, stacked=False, options=None):
        super().__init__(width=width, height=height, stacked=stacked, options=options)
        self.filename = filename
        self.configuration = None
        self.data = None
        self.stacked = stacked
        self.options = options
        self.load_csv(filename)
    def load_csv(self, filename):
        """
        Load a CSV file and create a bar chart.
        """
        import csv
        with open(filename, "r") as f:
            reader = csv.reader(f)
            # read the header
            header = next(reader)
            # read the data
            data = []
            for row in reader:
                data.append(row)
            # create a bar chart
            self.data = data_config.ChartData()
            # Assume the first column is the dataset name.
            # Assume the rest of the columns are the data values.
            # Only use the columns that are strictly numeric.
            # The first row is the header.
            dataset_name_header = header[0]
            value_names = header[1:]
            is_numeric_column = {name: True for name in value_names}
            name_to_values = {name: [] for name in value_names}
            for row in data:
                for i, value in enumerate(row[1:]):
                    name = value_names[i]
                    name_to_values[name].append(value)
                    try:
                        float(value)
                    except ValueError:
                        is_numeric_column[name] = False
            # create the labels for numeric columns
            not finished

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