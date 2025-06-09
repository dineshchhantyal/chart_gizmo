"""
BoxPlotChart for creating box plots using Chart.js and chartjs-chart-boxplot plugin.
"""

from chart_gizmo.abstract_chart import AbstractChart
from chart_gizmo.cli import CSVChartCLI
import csv
import numpy as np

class BoxPlotChart(AbstractChart):
    """
    A class to represent a box plot chart.
    """
    def __init__(
        self,
        configuration=None,
        width=600,
        height=400,
        options=None,
        title=None,
        stacked=False,
        animate=AbstractChart.ANIMATION_DEFAULT,
        **kwargs
    ):
        super().__init__(configuration, width, height, options, title, animate=animate, **kwargs)

        self.type = "boxplot"
        self.data = None
        if configuration is None:
            self.data = {"labels": [], "datasets": []}
        if self.options is None:
            self.options = {}
        if "plugins" not in self.options:
            self.options["plugins"] = {}
        self.options["plugins"]["datalabels"] = self.options.get("plugins", {}).get("datalabels", {})
        self.options["plugins"]["datalabels"]["display"] = False

    def add_label(self, label):
        self.data["labels"].append(label)

    def add_data_values(self, label, values, background_color=None, border_color=None, border_width=1, **kwargs):
        dataset = {
            **kwargs,
            "label": label,
            "data": values,
            "backgroundColor": background_color or "rgba(100, 130, 255, 0.7)",
            "borderColor": border_color or "rgba(100, 130, 255, 1.0)",
            "borderWidth": border_width,
        }
        self.data["datasets"].append(dataset)

class CSVBoxPlotChart(BoxPlotChart):
    """
    Loads a CSV and creates a boxplot chart.
    Each column is a group, each row is a sample.
    """
    def __init__(self, csv_file, labels=None, columns=None, group_column=None, animate=AbstractChart.ANIMATION_DEFAULT, **kwargs):
        super().__init__(animate=animate, **kwargs)
        self.csv_file = csv_file
        self.labels = labels
        self.columns = self.cleaned_columns(columns) if columns else None
        self.group_column = group_column
        self._transform_data_boxplot(csv_file)

    def cleaned_columns(self, columns):
        """
        Clean and validate the columns parameter.
        """
        if isinstance(columns, str):
            return [col.strip() for col in columns.split(",") if col.strip()]
        elif isinstance(columns, list):
            return [col.strip() for col in columns if isinstance(col, str) and col.strip()]
        else:
            raise ValueError("Columns must be a comma-separated string or a list of strings.")

    def _transform_data_boxplot(self, csv_file):
        """
        Transform the data for boxplot representation.
        If group_column is provided, group the data by that column and show all columns that are passed.
        Each group becomes a box, and each value in the box comes from the specified columns for that group.
        """
        with open(csv_file, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        if not rows:
            raise ValueError(f"CSV file is empty or invalid: {csv_file}")

        # If no columns specified, use all columns except group_column
        if self.columns is None:
            columns = [col for col in rows[0].keys() if col != self.group_column]
        else:
            columns = [col for col in self.columns if col != self.group_column and col in rows[0].keys()]

        if not self.group_column:
            file_labels = columns
            data = []
            for col in columns:
                arr = []
                for row in rows:
                    try:
                        arr.append(float(row[col]))
                    except Exception:
                        continue
                data.append(arr)
            if self.labels:
                self.data["labels"] = self.labels
            else:
                self.data["labels"] = file_labels
            self.add_data_values("Boxplot", data)
            return

        # Group by group_column
        if self.group_column not in rows[0]:
            raise ValueError(f"Group column '{self.group_column}' not found in CSV file: {csv_file}")

        group_values = sorted(set(row[self.group_column] for row in rows if row[self.group_column] != ""))
        data = []
        for group in group_values:
            group_arr = []
            for col in columns:
                col_values = [
                    float(row[col])
                    for row in rows
                    if row[self.group_column] == group and row[col] not in ("", None)
                ]
                if col_values:
                    group_arr.append(col_values)
            # If only one column, flatten one level
            if len(group_arr) == 1:
                group_arr = group_arr[0]
            data.append(group_arr)
        if self.labels:
            self.data["labels"] = self.labels
        else:
            self.data["labels"] = group_values

        self.add_data_values("Boxplot", data)
def BoxPlotChartScript():
    """
    Command-line entrypoint for BoxPlotChart using CSVChartCLI.
    """
    cli = CSVChartCLI(
        CSVBoxPlotChart,
        {
            "custom_commands_args": [
                {
                    "name": "columns",
                    "flags": ["--columns"],
                    "help": "Comma-separated list of columns to include as boxes (default: all except group_column)",
                    "required": False,
                    "default": None,
                },

            ]
        },
        description="Create a boxplot from a CSV file. By default, each column is a group (box), each row is a sample. Use --group-column to group by a column and show all specified columns as boxes within each group."
    )
    cli.run()

def serve_example_boxplot_chart():
    from H5Gizmos import serve
    chart = BoxPlotChart(title="Example Box Plot")
    for label in ['January', 'February', 'March', 'April', 'May', 'June', 'July']:
        chart.add_label(label)
    def random_values(n, low, high):
        return [round(x, 2) for x in np.random.uniform(low, high, n)]
    chart.add_data_values(
        "Dataset 1",
        [
            random_values(100, 0, 100),
            random_values(100, 0, 20),
            random_values(100, 20, 70),
            random_values(100, 60, 100),
            random_values(40, 50, 100),
            None,
            random_values(100, 80, 100)
        ],
        background_color="rgba(255,0,0,0.5)",
        border_color="red",
        border_width=1,
        outlierColor="#999999",
        padding=10,
        itemRadius=0
    )
    chart.add_data_values(
        "Dataset 2",
        [
            random_values(100, 60, 100),
            random_values(100, 0, 100),
            random_values(100, 0, 20),
            random_values(100, 20, 70),
            random_values(40, 60, 120),
            random_values(100, 20, 100),
            random_values(100, 80, 100)
        ],
        background_color="rgba(0,0,255,0.5)",
        border_color="blue",
        border_width=1,
        outlierColor="#999999",
        padding=10,
        itemRadius=0
    )
    serve(chart.show())

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1].endswith(".csv"):
        BoxPlotChartScript()
    else:
        serve_example_boxplot_chart()