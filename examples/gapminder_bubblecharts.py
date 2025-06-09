import os
from chart_gizmo import bubbles
from H5Gizmos import serve, Stack

# point at the gapminder file
data_path = os.path.join(os.path.dirname(__file__), "gapminderDataFiveYear.csv")

class GapminderBubbleVisualizer:
    """Bubble chart: X=GDP per Capita, Y=Life Expectancy,
       Size=Population, Color=Continent."""

    def __init__(self, path=data_path):
        self.data_path = path
        # Simple color palette
        self.colors = {
            "Asia":    "#1f77b4",
            "Europe":  "#ff7f0e",
            "Africa":  "#2ca02c",
            "Americas":"#d62728",
            "Oceania": "#9467bd"
        }

    def create_bubble_chart(self):
        # Create a bubble chart using CSVBubbleChart
        chart = bubbles.CSVBubbleChart(
            csv_file=self.data_path,
            x_column="gdpPercap",
            y_column="lifeExp",
            r_column="pop",
            group_column="continent",
            width=900,
            height=600,
            min_radius=3,
            max_radius=20,
            title="Gapminder: GDP vs Life Expectancy",
            tooltip_columns=["country", "gdpPercap", "lifeExp", "pop", "year"],
        )

        # Alternative approach
        chart.logarithmic(axis="x")

        # Customize datasets with colors
        for dataset in chart.data.datasets:
            continent = dataset.label
            color = self.colors.get(continent, "#888")
            dataset.backgroundColor = color + "80"
            dataset.borderColor = color

        return chart

    def serve_visualization(self):
        # Create and serve the visualization
        chart = self.create_bubble_chart()
        display = Stack([
            "Gapminder Bubble Chart - GDP vs Life Expectancy",
            chart
        ])
        serve(display.show())

if __name__ == "__main__":
    GapminderBubbleVisualizer().serve_visualization()