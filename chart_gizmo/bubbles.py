"""
BubbleChart class for creating bubble charts.
"""

from .abstract_chart import AbstractChart
from .bars import CSVBarChart
from .cli import CSVChartCLI
from .data_config import DataSet


class BubbleChart(AbstractChart):
    """
    BubbleChart class for creating bubble charts.

    Bubble charts display three dimensions of data:
    - x position
    - y position
    - bubble size (radius)
    """
    def __init__(self, configuration=None, width=400, height=400, stacked=False, options=None,
                 title=None, r_column=None, x_column=None, y_column=None, group_column=None,
                 min_radius=None, max_radius=None):
        """
        Initialize the BubbleChart.

        Args:
            configuration: Chart data configuration
            width: Chart width in pixels
            height: Chart height in pixels
            stacked: Whether the chart is stacked (not used for bubble charts)
            options: Additional chart options
            title: Chart title
            r_column: Column for radius values
            x_column: Column for x-axis values
            y_column: Column for y-axis values
            group_column: Column for grouping data
            min_radius: Minimum radius for bubbles
            max_radius: Maximum radius for bubbles
            bubble_label_column: Column for bubble labels
            tooltip_column: Column for tooltip content
        """
        super().__init__(configuration, width, height, stacked, options, title)
        self.title = title
        self.type = "bubble"

        self.r_column = r_column
        self.x_column = x_column
        self.y_column = y_column
        self.group_column = group_column
        self.min_radius = int(min_radius) if min_radius is not None else 5
        self.max_radius = int(max_radius) if max_radius is not None else 20

        # Initialize options properly
        if self.options is None:
            self.options = {}

        # Ensure plugins section exists
        if "plugins" not in self.options:
            self.options["plugins"] = {}

        # Configure datalabels based on bubble_label_column
        self.options["plugins"]["datalabels"] = self.options.get("plugins", {}).get("datalabels", {})
        self.options["plugins"]["datalabels"]["display"] = False

        # Configure tooltip
        self.options["plugins"]["tooltip"] = self.options.get("plugins", {}).get("tooltip", {})
        self.options["plugins"]["tooltip"]["enabled"] = True

    def add_data_values(self, label, values=..., background_color=None, border_color=None, border_width=1):
        """
        Bubble charts has one label per dataset, so we can use the label as the group name.
        """
        if self.data is None:
            raise ValueError("Data configuration is fixed.")

        # create a new dataset

        database = DataSet(label, values, background_color, border_color, border_width)
        # Add a dataset for the bubble chart, directly using the label as the group name
        self.data.datasets.append(database)


class CSVBubbleChart(BubbleChart):
    """
    Loads a CSV and creates a bubble chart.
    """
    def __init__(self, csv_file, x_column, y_column, r_column,
                 group_column=None, width=400, height=400, stacked=False,
                 configuration=None, options=None, min_radius=5, max_radius=20,
                 title=None, bubble_label_column=None, tooltip_column=None):

        # Initialize with parent's constructor using proper keyword arguments
        super().__init__(
            configuration=configuration,
            width=width,
            height=height,
            stacked=stacked,
            options=options,
            title=title,
            r_column=r_column,
            x_column=x_column,
            y_column=y_column,
            group_column=group_column,
            min_radius=min_radius,
            max_radius=max_radius
        )

        self.csv_file = csv_file
        self.bubble_label_column = bubble_label_column
        self.tooltip_column = tooltip_column

        # Transform the data to bubble format
        self._transform_to_bubble_data(x_column, y_column, r_column)


    def _transform_to_bubble_data(self, x_column, y_column, r_column):
        """Transform bar chart data to bubble chart format"""
        import csv

        # Read CSV file to process it as bubble data
        with open(self.csv_file, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Clear existing datasets AND labels from parent initialization
        self.clear()
        self.data.labels = []  # Clear labels - bubble charts don't need one label per point

        # Find min and max values for radius scaling
        r_values = []
        for row in rows:
            try:
                r_values.append(float(row[r_column]))
            except (ValueError, KeyError):
                continue

        r_min = min(r_values) if r_values else 1
        r_max = max(r_values) if r_values else 100

        # Define a scaling function to map r_values to min_radius...max_radius
        def scale_radius(r_val):
            if r_max == r_min:
                return self.min_radius
            # Linear scaling between min_radius and max_radius
            return self.min_radius + ((r_val - r_min) / (r_max - r_min)) * (self.max_radius - self.min_radius)


        # Group by group column if provided
        if self.group_column:
            # Group by the group column
            groups = {}
            for row in rows:
                group = row[self.group_column]
                if group not in groups:
                    groups[group] = []

                try:
                    x_val = float(row[x_column])
                    y_val = float(row[y_column])
                    r_raw = float(row[r_column])
                    r_val = scale_radius(r_raw)  # Scale the radius

                    bubble_data = {
                        'x': x_val,
                        'y': y_val,
                        'r': r_val
                    }

                    # Add label if bubble_label_column is provided
                    if self.bubble_label_column and self.bubble_label_column in row:
                        bubble_data['label'] = row[self.bubble_label_column]

                    # Add tooltip if tooltip_column is provided
                    if self.tooltip_column and self.tooltip_column in row:
                        bubble_data['tooltip'] = row[self.tooltip_column]

                    groups[group].append(bubble_data)
                except (ValueError, KeyError):
                    # Skip invalid rows
                    continue

            # Create a dataset for each group
            for group, bubble_data in groups.items():
                self.add_data_values(group, bubble_data)
        else:
            # No grouping, create a single dataset
            bubble_data = []
            for row in rows:
                try:
                    x_val = float(row[x_column])
                    y_val = float(row[y_column])
                    r_raw = float(row[r_column])
                    r_val = scale_radius(r_raw)  # Scale the radius

                    data_point = {
                        'x': x_val,
                        'y': y_val,
                        'r': r_val
                    }

                    # Add label if bubble_label_column is provided
                    if self.bubble_label_column and self.bubble_label_column in row:
                        data_point['label'] = row[self.bubble_label_column]

                    # Add tooltip if tooltip_column is provided
                    if self.tooltip_column and self.tooltip_column in row:
                        data_point['tooltip'] = row[self.tooltip_column]

                    bubble_data.append(data_point)
                except (ValueError, KeyError):
                    # Skip invalid rows
                    continue

            self.add_data_values("Bubbles", bubble_data)
        print(f"Bubble chart created with {len(self.data.datasets)} datasets from CSV file: {self.csv_file}")

def serve_example_bubble_chart():
    """
    Serve an example bubble chart.
    """
    from H5Gizmos import serve
    import random

    chart = BubbleChart(width=600, height=400, title="Bubble Chart with Tooltips and Labels")

    # Add some random bubbles in different colors with labels and tooltips
    chart.add_data_values(
        "Red Bubbles",
        [{'x': (x := random.randint(0, 100)),  # Assign x first
          'y': (y := random.randint(0, 100)),  # Assign y first
          'r': random.randint(5, 20),
          'label': f"R{i}",
          'tooltip': f"Red bubble #{i}: x={x}, y={y}"  # Use the same values
         }
         for i in range(8)],
        background_color="rgba(255, 99, 132, 0.5)"
    )

    chart.add_data_values(
        "Blue Bubbles",
        [{'x': (x := random.randint(0, 100)),
          'y': (y := random.randint(0, 100)),
          'r': (r := random.randint(5, 20)),
          'label': f"B{i}",  # Add label for each bubble
          'tooltip': f"Blue bubble #{i}: x={x}, y={y}, r={r}"}
         for i in range(10)],
        background_color="rgba(54, 162, 235, 0.5)"
    )

    # Set up click handler
    def click_callback(event):
        print("Click event:", event)
    chart.on_click_call(click_callback)

    # Serve the chart
    serve(chart.show())


def CSVBubbleChartScript():
    """Command-line entrypoint for CSVBubbleChart"""
    cli = CSVChartCLI(CSVBubbleChart,
                      {
                          "custom_commands_args": [
                              {
                                  "name": "r_column",
                                  "flags": ["-r", "--radius_column"],
                                    "help": "Column for bubble radius (size)",
                                    "required": True
                              }, {
                                  "name": "x_column",
                                  "flags": ["-x", "--x_column"],
                                  "help": "Column for x-axis values",
                                  "required": True
                              }, {
                                  "name": "y_column",
                                  "flags": ["-y", "--y_column"],
                                  "help": "Column for y-axis values",
                                  "required": True
                              }, {
                                  "name": "min_radius",
                                  "flags": ["--min_radius"],
                                  "help": "Minimum radius for bubbles",
                                  "required": False,
                                  "default": 5
                              }, {
                                    "name": "max_radius",
                                    "flags": ["--max_radius"],
                                    "help": "Maximum radius for bubbles",
                                    "required": False,
                                    "default": 20
                              }, {
                                  "name": "bubble_label_column",
                                  "flags": ["--bubble_label_column"],
                                  "help": "Column for bubble labels (grouping)",
                                  "required": False,
                                  "default": None
                              }, {
                                  "name": "tooltip_column",
                                  "flags": ["--tooltip_column"],
                                  "help": "Column to use for bubble tooltips on hover",
                                  "required": False,
                                  "default": None
                              }
                          ]
                      })
    cli.run()


if __name__ == "__main__":
    serve_example_bubble_chart()