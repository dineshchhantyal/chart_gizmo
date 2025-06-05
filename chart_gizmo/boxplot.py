"""
BoxPlotChart for creating box plots using Chart.js and chartjs-chart-boxplot plugin.
"""

from chart_gizmo.abstract_chart import AbstractChart

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
    ):
        super().__init__(configuration, width, height, stacked=False, options=options, title=title)
        self.type = "boxplot"
        self.data = None
        if configuration is None:
            self.data = {"labels": [], "datasets": []}
        self.options = self.options or {}

    def add_label(self, label):
        self.data["labels"].append(label)

    def add_boxplot_data(self, label, values, background_color=None, border_color=None, border_width=1):
        """
        Add a boxplot dataset.
        values: list of arrays, each array is a set of numbers for a box.
        """
        dataset = {
            "label": label,
            "data": values,
            "backgroundColor": background_color or "rgba(100, 130, 255, 0.7)",
            "borderColor": border_color or "rgba(100, 130, 255, 1.0)",
            "borderWidth": border_width,
            "type": "boxplot"
        }
        self.data["datasets"].append(dataset)

    def get_configuration(self):
        config = {
            "type": "boxplot",
            "data": self.data,
            "options": self.options,
        }
        return config

# Example usage (for your examples/ folder)
if __name__ == "__main__":
    from H5Gizmos import serve
    import numpy as np

    chart = BoxPlotChart(title="Example Box Plot")
    chart.add_label("A")
    chart.add_label("B")
    chart.add_label("C")
    chart.add_boxplot_data(
        "Sample Data",
        [
            np.random.normal(0, 1, 100).tolist(),
            np.random.normal(1, 1.5, 100).tolist(),
            np.random.normal(-1, 0.5, 100).tolist(),
        ]
    )
    serve(chart.show())