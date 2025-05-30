"""
PieChart class for creating pie and donut charts.
"""

from chart_gizmo.abstract_chart import AbstractChart
from chart_gizmo.cli import CSVChartCLI
from chart_gizmo.data_config import DataSet, Datum


class PieDataSet(DataSet):
    """
A specialized DataSet class for pie charts that handles
    multiple background colors for a single dataset.
    """

    def __init__(self, label, values=(), background_colors=None, border_color=None, border_width=1, **kwargs):
        """
        Initialize a PieDataSet with support for multiple background colors.

        Parameters
        ----------
        label : str
            The label for the dataset
        values : list
            The values for each segment
        background_colors : list
            A list of colors for each segment (must match length of values)
        border_color : str or list
            Border color(s) for segments
        border_width : int
            Border width
        """
        super().__init__(label, values, None, border_color, border_width, **kwargs)

        # Handle background colors - each segment needs its own color
        if background_colors is None:
            import random
            # Generate random colors if none provided
            background_colors = []
            for _ in range(len(values)):
                r = random.randint(100, 255)
                g = random.randint(100, 255)
                b = random.randint(100, 255)
                background_colors.append(f"rgba({r}, {g}, {b}, 0.7)")

        # Store individual colors for each segment
        self.segment_colors = background_colors

        # Apply colors to each datum
        for i, datum in enumerate(self.data):
            if i < len(background_colors):
                datum.backgroundColor = background_colors[i]

    def as_dict(self, index=0):
        """
        Convert the dataset to a JSON compatible dictionary for pie charts.
        Each segment gets its own background color.
        """
        result = dict(
            label=self.label,
            data=[datum.value for datum in self.data],
            backgroundColor=[datum.backgroundColor for datum in self.data],
            borderColor=self.borderColor,
            borderWidth=self.borderWidth,
        )
        # Add other options
        result.update(self.options)
        return result


class PieChart(AbstractChart):
    """
    PieChart class for creating pie and donut charts.

    Pie charts display data as slices of a circle with sizes proportional to their values.
    Donut charts are pie charts with a hole in the center.
    """
    def __init__(self, configuration=None, width=400, height=400, donut=False, donut_ratio=0.5, options=None):
        super().__init__(configuration, width, height, False, options)  # Pie charts don't use 'stacked' parameter
        self.type = "pie" if not donut else "doughnut"
        self.donut = donut
        self.donut_ratio = donut_ratio

    def as_donut(self, ratio=0.5):
        """
        Convert this pie chart to a donut chart.

        Parameters
        ----------
        ratio : float
            The size of the hole (0-1, where 1 would be all hole)
        """
        self.type = "doughnut"
        self.donut = True
        self.donut_ratio = ratio

        # If options is None, initialize it
        if self.options is None:
            self.options = {}

        # Set the cutout percentage for the donut chart
        self.options["cutoutPercentage"] = int(ratio * 100)

        return self

    def get_default_data_configuration(self):
        """
        Get the default data configuration for pie charts.
        Pie charts handle datasets differently than other chart types.
        """
        from chart_gizmo.data_config import DataConfig
        config = DataConfig()
        # For pie charts, labels are segment names
        config.labels = []
        return config

    def add_data_values(self, label, values=None, background_color=None, border_color=None, border_width=1):
        """
        Add a dataset to the pie chart.

        For pie charts, colors should be an array matching the number of data points.

        Parameters
        ----------
        label : str
            Dataset label
        values : list or dict
            Values for the dataset
        background_color : str or list
            Background color(s) for the segments. Can be a single color or a list of colors.
        border_color : str or list
            Border color(s) for the segments. Can be a single color or a list of colors.
        border_width : int
            Border width
        """
        if self.data is None:
            self.data = self.get_default_data_configuration()

        # For pie charts, we need to handle colors differently - each segment needs its own color
        if background_color and not isinstance(background_color, list):
            background_color = [background_color] * len(values)
        if border_color and not isinstance(border_color, list):
            border_color = [border_color] * len(values)

        # Use our specialized PieDataSet class instead of the regular DataSet
        dataset = PieDataSet(label, values, background_color, border_color, border_width)

        self.data.datasets.append(dataset)
        return self

    def add_label(self, label, values=()):
        """
        Add a label to the pie chart.

        For pie charts, labels are added differently than other charts.
        We just add the label without requiring values for datasets.

        Parameters
        ----------
        label : str
            The label to add
        values : tuple, optional
            Ignored for pie charts
        """
        if self.data is None:
            self.data = self.get_default_data_configuration()

        # Simply add the label without validation against datasets
        self.data.labels.append(label)
        return self


class CSVPieChart(PieChart):
    """
    Loads a CSV and creates a pie or donut chart.

    A pie chart shows distribution as slices of a circle, with each slice proportional
    to the value. Each row in the CSV with the same label will be aggregated into
    a single slice.
    """
    def __init__(self, csv_file, label_column=None, value_column=None,
                 width=400, height=400, donut=False,
                 donut_ratio=0.5, configuration=None, stacked=False, options=None):
        # Initialize with parent's constructor
        super().__init__(
            configuration,
            width,
            height,
            donut,
            donut_ratio,
            options
        )

        self.csv_file = csv_file
        self.label_column = label_column
        self.value_column = value_column
        # Remove group_column - not applicable for pie charts

        # Load data from CSV
        self._load_csv_data()

    def _load_csv_data(self):
        """Load data from the CSV file and format for pie chart"""
        import csv
        import random

        # Generate some default colors
        def generate_colors(count):
            colors = []
            for i in range(count):
                r = random.randint(100, 255)
                g = random.randint(100, 255)
                b = random.randint(100, 255)
                colors.append(f"rgba({r}, {g}, {b}, 0.7)")
            return colors

        # Read CSV file
        with open(self.csv_file, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            raise ValueError(f"CSV file is empty or invalid: {self.csv_file}")

        # If columns not specified, use the first columns
        headers = list(rows[0].keys())

        self.label_column = self.label_column or headers[0]
        self.value_column = self.value_column or (headers[1] if len(headers) > 1 else None)

        if not self.value_column:
            raise ValueError("No value column specified or available")

        # Clear any existing data
        self.clear()

        # Aggregate data by label
        data = {}
        for row in rows:
            label = row[self.label_column]
            try:
                value = float(row[self.value_column])
                if label not in data:
                    data[label] = 0
                data[label] += value
            except (ValueError, KeyError):
                # Skip invalid rows
                continue

        # Add labels and values
        labels = list(data.keys())
        values = list(data.values())

        # First add all labels to the chart
        for label in labels:
            super().add_label(label)

        # Generate colors for each pie segment
        colors = generate_colors(len(values))

        # Create the dataset
        self.add_data_values(
            self.value_column,  # Use the value column name as the dataset label
            values,
            background_color=colors,
            border_color="rgba(255,255,255,0.8)",
            border_width=2
        )

        # Configure chart title
        self.options = self.options or {}
        self.options["plugins"] = self.options.get("plugins", {})
        self.options["plugins"]["title"] = {
            "display": True,
            "text": f"Distribution of {self.value_column} by {self.label_column}"
        }

        # Add tooltip configuration for better display
        self.options["plugins"]["tooltip"] = {
            "callbacks": {
                "label": "function(context) { return context.label + ': ' + context.raw.toLocaleString(); }"
            }
        }

        if self.donut:
            self.options["cutoutPercentage"] = int(self.donut_ratio * 100)

        print(f"Pie chart created with {len(values)} segments from CSV file: {self.csv_file}")


def serve_example_pie_chart():
    """
    Serve an example pie chart.
    """
    from H5Gizmos import serve

    chart = PieChart(width=600, height=400)

    # Add labels
    for fruit in ["Apples", "Oranges", "Bananas", "Grapes", "Kiwi"]:
        chart.add_label(fruit)

    # Add data with colors - each color corresponds to a slice
    chart.add_data_values(
        "Fruits",
        [45, 25, 15, 10, 5],
        background_color=[
            "rgba(255, 99, 132, 0.7)",
            "rgba(54, 162, 235, 0.7)",
            "rgba(255, 206, 86, 0.7)",
            "rgba(75, 192, 192, 0.7)",
            "rgba(153, 102, 255, 0.7)"
        ],
        border_color="rgba(255, 255, 255, 0.8)",  # White borders for contrast
        border_width=2
    )

    # Set up click handler
    def click_callback(event):
        print("Click event:", event)
    chart.on_click_call(click_callback)

    # Serve the chart
    serve(chart.show())


def serve_example_donut_chart():
    """
    Serve an example donut chart.
    """
    from H5Gizmos import serve

    chart = PieChart(width=600, height=400)
    chart.as_donut(0.6)  # Convert to donut with 60% hole

    # Add labels
    for category in ["Housing", "Food", "Transport", "Entertainment", "Savings"]:
        chart.add_label(category)

    # Add data
    chart.add_data_values(
        "Budget",
        [35, 25, 15, 10, 15],
        background_color=[
            "rgba(255, 99, 132, 0.7)",
            "rgba(54, 162, 235, 0.7)",
            "rgba(255, 206, 86, 0.7)",
            "rgba(75, 192, 192, 0.7)",
            "rgba(153, 102, 255, 0.7)"
        ]
    )

    # Serve the chart
    serve(chart.show())


def CSVPieChartScript():
    """Command-line entrypoint for CSVPieChart"""
    cli = CSVChartCLI(CSVPieChart,
                      {
                          "custom_commands_args": [
                              {
                                  "name": "donut",
                                  "flags": ["-d", "--donut"],
                                  "help": "Create a donut chart instead of a pie chart",
                                  "action": "store_true"  # No type or required for boolean flags
                              },
                              {
                                  "name": "donut_ratio",
                                  "flags": ["--donut-ratio"],
                                  "help": "Ratio for the donut hole size (0-1)",
                                  "required": False,
                                  "default": 0.5,
                                  "type": float
                              }
                          ]
                      })
    cli.run()


if __name__ == "__main__":
    # serve_example_pie_chart()
    # Uncomment to see donut example
    serve_example_donut_chart()
