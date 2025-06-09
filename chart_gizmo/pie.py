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
    def __init__(self, configuration=None, width=400, height=400, donut=False, donut_ratio=0.5, options=None, title=None, animate=AbstractChart.ANIMATION_DEFAULT, **kwargs):
        super().__init__(configuration, width, height, options, title, animate=animate, **kwargs)  # Pie charts don't use 'stacked' parameter
        self.type = "pie" if not donut else "doughnut"
        self.donut = donut
        self.donut_ratio = donut_ratio
        # Initialize options if None
        if self.options is None:
            self.options = {}

        # Ensure responsive is set to False to respect width and height,
        # this is !fix to avoid chart rendered as a massive element
        self.options["responsive"] = self.options.get("responsive", False)


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

        # Chart.js v3+ uses 'cutout' (as percent string or number)
        self.options["cutout"] = f"{int(ratio * 100)}%"
        # Remove legacy key if present
        self.options.pop("cutoutPercentage", None)

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
    a single slice. Optionally, group_column can be used to create multiple datasets.
    """
    def __init__(self, csv_file, label_column=None, value_column=None,
                 width=400, height=400, donut=False,
                 donut_ratio=0.5, group_column=None, configuration=None, stacked=False, options=None, title=None, animate=AbstractChart.ANIMATION_DEFAULT, **kwargs):
        super().__init__(
            configuration,
            width,
            height,
            donut,
            donut_ratio,
            options,
            title,
            animate=animate,
            **kwargs
        )
        self.csv_file = csv_file
        self.label_column = label_column
        self.value_column = value_column
        self.group_column = group_column

        # Load data from CSV
        self._load_csv_data()

    def _load_csv_data(self):
        """Load data from the CSV file and format for pie chart, supporting group_column."""
        import csv
        import random

        def generate_colors(count):
            colors = []
            for i in range(count):
                r = random.randint(100, 255)
                g = random.randint(100, 255)
                b = random.randint(100, 255)
                colors.append(f"rgba({r}, {g}, {b}, 0.7)")
            return colors

        with open(self.csv_file, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        if not rows:
            raise ValueError(f"CSV file is empty or invalid: {self.csv_file}")

        headers = list(rows[0].keys())
        self.label_column = self.label_column or headers[0]
        self.value_column = self.value_column or (headers[1] if len(headers) > 1 else None)
        if not self.value_column:
            raise ValueError("No value column specified or available")


        self.clear()

        if self.group_column and self.group_column in headers:
            # Grouped pie: multiple datasets, one per group
            group_data = {}
            label_set = set()
            for row in rows:
                group = row[self.group_column]
                label = row[self.label_column]
                try:
                    value = float(row[self.value_column])
                except (ValueError, KeyError):
                    continue
                label_set.add(label)
                if group not in group_data:
                    group_data[group] = {}
                if label not in group_data[group]:
                    group_data[group][label] = 0
                group_data[group][label] += value
            labels = sorted(label_set)
            for label in labels:
                super().add_label(label)
            for group, label_values in group_data.items():
                values = [label_values.get(label, 0) for label in labels]
                colors = generate_colors(len(values))
                self.add_data_values(
                    group,
                    values,
                    background_color=colors,
                    border_color="rgba(255,255,255,0.8)",
                    border_width=2
                )
        else:
            # Standard pie: single dataset
            data = {}
            for row in rows:
                label = row[self.label_column]
                try:
                    value = float(row[self.value_column])
                    if label not in data:
                        data[label] = 0
                    data[label] += value
                except (ValueError, KeyError):
                    continue
            labels = list(data.keys())
            values = list(data.values())
            for label in labels:
                super().add_label(label)
            colors = generate_colors(len(values))
            self.add_data_values(
                self.value_column,
                values,
                background_color=colors,
                border_color="rgba(255,255,255,0.8)",
                border_width=2
            )

        self.options = self.options or {}
        self.options["plugins"] = self.options.get("plugins", {})
        self.options["plugins"]["title"] = {
            "display": True,
            "text": f"Distribution of {self.value_column} by {self.label_column}" + (f" (grouped by {self.group_column})" if self.group_column else "")
        }
        if self.donut:
            self.options["cutout"] = f"{int(self.donut_ratio * 100)}%"
            self.options.pop("cutoutPercentage", None)

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
                      }
                    )
    cli.run()


if __name__ == "__main__":
    # serve_example_pie_chart()
    # Uncomment to see donut example
    serve_example_donut_chart()
