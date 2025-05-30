# Pie Charts

Pie charts are useful for showing proportional parts of a whole. They display data as slices of a circle with sizes proportional to their values.

## Basic Usage

```python
from chart_gizmo.pie import PieChart
from H5Gizmos import serve

# Create a new pie chart
chart = PieChart(width=600, height=400)

# Add labels for each slice
for fruit in ["Apples", "Oranges", "Bananas", "Grapes", "Kiwi"]:
    chart.add_label(fruit)

# Add data with colors
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
    border_color="rgba(255, 255, 255, 0.8)"
)

# Display the chart
serve(chart.show())
```

## Donut Charts

You can convert a pie chart to a donut chart using the `as_donut()` method:

```python
from chart_gizmo.pie import PieChart
from H5Gizmos import serve

# Create a new chart and convert to donut
chart = PieChart(width=600, height=400)
chart.as_donut(0.6)  # Hole size is 60% of the radius

# Add labels and data
for category in ["Housing", "Food", "Transport", "Entertainment", "Savings"]:
    chart.add_label(category)

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

# Display the chart
serve(chart.show())
```

## Creating Pie Charts from CSV

You can easily create pie charts from CSV files using the `CSVPieChart` class:

```python
from chart_gizmo.pie import CSVPieChart
from H5Gizmos import serve

# Create chart from CSV, specifying label and value columns
chart = CSVPieChart(
    csv_file="data/data.csv",
    label_column="Country",
    value_column="Population",
    width=800,
    height=600
)

# Display the chart
serve(chart.show())
```

## Command Line Usage

Chart Gizmo provides a command-line tool for quick visualization of CSV data:

```bash
# Basic pie chart
csv-pie-gizmo data/data.csv -l "Category" -v "Amount" --width 800 --height 600

# Donut chart
csv-pie-gizmo data/data.csv -l "Category" -v "Amount" --donut --donut-ratio 0.7

# Example with Gapminder dataset - Population by continent
csv-pie-gizmo gapminderDataFiveYear.csv -l "continent" -v "pop" --width 800 --height 600 --donut

# Example with grouping
csv-pie-gizmo data/data.csv -l "Category" -v "Amount" -g "Year" --donut --donut-ratio 0.7
```

## API Reference

### PieChart

```python
PieChart(configuration=None, width=400, height=400, donut=False, donut_ratio=0.5, options=None)
```

**Parameters:**

- `configuration`: Optional chart configuration
- `width`: Chart width in pixels
- `height`: Chart height in pixels
- `donut`: If True, creates a donut chart instead of a pie chart
- `donut_ratio`: The size of the hole in a donut chart (0-1)
- `options`: Additional Chart.js options

**Methods:**

- `add_label(label)`: Add a slice label to the chart
- `add_data_values(label, values, background_color, border_color, border_width)`: Add data values with colors
- `as_donut(ratio)`: Convert to a donut chart with the specified hole ratio
- `show()`: Returns a gizmo for display

### CSVPieChart

```python
CSVPieChart(csv_file, label_column=None, value_column=None, width=400, height=400, donut=False, donut_ratio=0.5, configuration=None, options=None)
```

**Parameters:**

- `csv_file`: Path to the CSV file
- `label_column`: Name of the column to use for slice labels
- `value_column`: Name of the column to use for slice values
- `width`: Chart width in pixels
- `height`: Chart height in pixels
- `donut`: If True, creates a donut chart
- `donut_ratio`: The size of the hole in a donut chart (0-1)
- `configuration`: Optional chart configuration
- `options`: Additional Chart.js options
