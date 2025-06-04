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
    def __init__(self, configuration=None, width=400, height=400, stacked=False, options=None, title=None):
        """
        Initialize the BubbleChart.
        """
        super().__init__(configuration, width, height, stacked, options, title)
        self.type = "bubble"


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

    def get_default_options(self):
        """
        Get the default options for the bubble chart.
        """
        default_options = super().get_default_options()


        return default_options



class CSVBubbleChart(CSVBarChart):
    """
    Loads a CSV and creates a bubble chart.
    """
    def __init__(self, csv_file, x_column, y_column, r_column,
                 group_column=None, width=400, height=400, stacked=False,
                 configuration=None, options=None, min_radius=5, max_radius=20, title=None):

        # Initialize with parent's constructor first
        super().__init__(
            csv_file,
            x_column,  # Using x_column as label_column
            y_column,  # Using y_column as value_column
            group_column,
            width,
            height,
            stacked,
            configuration,
            options,
            title=title
        )

        self.csv_file = csv_file
        # After initialization, set the chart type to bubble
        self.type = "bubble"
        self.title = title

        # Store additional parameters - ensure they're numeric
        self.r_column = r_column
        self.min_radius = int(min_radius) if min_radius is not None else 5
        self.max_radius = int(max_radius) if max_radius is not None else 20

        # Transform the data to bubble format
        self._transform_to_bubble_data(x_column, y_column, r_column)

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
    def _transform_to_bubble_data(self, x_column, y_column, r_column):
        """Transform bar chart data to bubble chart format"""
        import csv

        # Read CSV file again to process it as bubble data
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

        # Configure chart options for bubble visualization
        self.options = {
            "responsive": True,
            "scales": {
                "x": {
                    "type": "logarithmic",  # Use log scale for GDP
                    "title": {"display": True, "text": x_column}
                },
                "y": {
                    "title": {"display": True, "text": y_column}
                }
            },
            "plugins": {
                "title": {
                    "display": True,
                    "text": self.title if self.title else f"Bubble Chart: {y_column} vs {x_column}"
                },
                "legend": {"position": "right"},
                "datalabels": {
                    "display": False  # Disable data labels for bubbles
                }
            }
        }

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
                    groups[group].append({
                        'x': x_val,
                        'y': y_val,
                        'r': r_val
                    })
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
                    bubble_data.append({
                        'x': x_val,
                        'y': y_val,
                        'r': r_val
                    })
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

    chart = BubbleChart(width=600, height=400)

    for i in range(10):
        # Add labels for the x-axis
        chart.add_label(f"Label {i}")

    # Add some random bubbles in different colors
    chart.add_data_values(
        "Red Bubbles",
        [{'x': random.randint(0, 100),
          'y': random.randint(0, 100),
          'r': random.randint(5, 20)}
         for _ in range(8)],
        background_color="rgba(255, 99, 132, 0.5)"
    )

    chart.add_data_values(
        "Blue Bubbles",
        [{'x': random.randint(0, 100),
          'y': random.randint(0, 100),
          'r': random.randint(5, 20)}
         for _ in range(10)],
        background_color="rgba(54, 162, 235, 0.5)"
    )

    chart.add_data_values(
        "Green Bubbles",
        [{'x': random.randint(0, 100),
          'y': random.randint(0, 100),
          'r': random.randint(5, 20)}
         for _ in range(10)],
        background_color="rgba(75, 192, 192, 0.5)"
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
                              }
                          ]
                      })
    cli.run()


if __name__ == "__main__":
    serve_example_bubble_chart()