from chart_gizmo.bubbles import CSVBubbleChart
from H5Gizmos import serve

# Create a bubble chart from CSV data
chart = CSVBubbleChart(
    csv_file="gapminderDataFiveYear.csv",
    x_column="gdpPercap",
    y_column="lifeExp",
    r_column="pop",
    group_column="continent",
    width=900,
    height=600,
    min_radius=3,
    max_radius=20,
    title="GDP vs Life Expectancy",
    tooltip_columns=["country", "year"],  # Multiple columns for tooltip
    bubble_label_column="country"
)
chart.logarithmic(axis="x")

# Display the chart
serve(chart.show())