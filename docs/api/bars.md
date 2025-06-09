# Bars

The `BarChart` and related classes provide bar chart functionality based on [Chart.js Bar Charts](https://www.chartjs.org/docs/latest/charts/bar.html).

![Sample Bar Chart](../screenshots/barchart.png)

## Basic Usage

```python
from chart_gizmo.bars import BarChart
from H5Gizmos import serve

# Create a bar chart comparing quarterly sales data
chart = BarChart()

# Add product categories
chart.add_label("Electronics")
chart.add_label("Clothing")
chart.add_label("Home Goods")

# Add quarterly data for each product category
chart.add_data_values("Q1", [45000, 32000, 28000], background_color="#3366CC")
chart.add_data_values("Q2", [52000, 38000, 31000], background_color="#DC3912")
chart.add_data_values("Q3", [48000, 42000, 36000], background_color="#FF9900")
chart.add_data_values("Q4", [60000, 52000, 40000], background_color="#109618")

# Display the chart
serve(chart.show())
```

## Class: BarChart

**Location:** `chart_gizmo/bars.py`

### Description

A class to represent a bar chart. Inherits from [`AbstractChart`](../api/charts.md).

### Key Methods

-   `add_label(label, values=())`: Add a label to the chart.
-   `add_dataset(dataset)`: Add a dataset to the chart.
-   `add_data_values(label, values=(), background_color=None, border_color=None, border_width=1)`: Add data values to the chart.
-   `get_configuration()`: Get the chart configuration.
-   `saveImage(filepath)`: Asynchronous method to save the chart as a PNG image file. Must be awaited when called. See [Chart Image Export Example](../examples/#chart-image-export).
    -   `filepath`: Path where the image file will be saved
-   `on_click_call(callback, action='click', selection='nearest')`: Set a callback function for click events on the chart. See [OnClick Event Example](../examples/#onclick-event-example).

## Class: TabularBarChart

**Location:** `chart_gizmo/bars.py`

### Description

Create a bar chart from a tabular data source (a list of dictionaries).

### Constructor Parameters

-   `dictionaries`: List of dictionaries containing the data
-   `label_column`: Name of the column to use for x-axis labels
-   `value_column`: Name of the column to use for y-axis values
-   `group_column`: Name of the column to use for grouping (optional)
-   `width`: Chart width in pixels (default: 400)
-   `height`: Chart height in pixels (default: 400)
-   `stacked`: Whether to use stacked bars (default: False)
-   `configuration`: Chart.js configuration (optional)
-   `options`: Additional chart options (optional)
-   `title`: Chart title (optional)
-   `animate` (bool): Enable or disable animations. Default is `False` (no animation). Controlled by the symbolic constant `ANIMATION_DEFAULT`.

### Example

```python
from chart_gizmo.bars import TabularBarChart
from H5Gizmos import serve

data = [
    {"label": "A", "group": "Red", "value": 12},
    {"label": "B", "group": "Red", "value": 1},
    {"label": "A", "group": "Blue", "value": 1},
    {"label": "B", "group": "Blue", "value": 19},
]
chart = TabularBarChart(
    dictionaries=data,
    label_column="label",
    group_column="group",
    value_column="value",
    stacked=True,
)
serve(chart.show())
```

## Class: CSVBarChart

**Location:** `chart_gizmo/bars.py`

### Description

Create a bar chart from a CSV file. Inherits from `TabularBarChart`.

### Constructor Parameters

-   `csv_file`: Path to the CSV file
-   `label_column`: Name of the column to use for x-axis labels
-   `value_column`: Name of the column to use for y-axis values
-   `group_column`: Name of the column to use for grouping (optional)
-   `width`: Chart width in pixels (default: 400)
-   `height`: Chart height in pixels (default: 400)
-   `stacked`: Whether to use stacked bars (default: False)
-   `configuration`: Chart.js configuration (optional)
-   `options`: Additional chart options (optional)
-   `title`: Chart title (optional)
-   `animate` (bool): Enable or disable animations. Default is `False` (no animation). Controlled by the symbolic constant `ANIMATION_DEFAULT`.

### Example

```python
from chart_gizmo.bars import CSVBarChart
from H5Gizmos import serve

chart = CSVBarChart(
    csv_file="data.csv",
    label_column="Category",
    value_column="Amount",
    group_column="Year",
    width=800,
    height=600,
    stacked=True,
    title="Sales by Category and Year"
)
serve(chart.show())
```

### Command-line Script

-   `CSVBarChartScript()`: Command-line entrypoint for CSVBarChart.

See the [Bar Chart CLI documentation](../cli/bar.md) for detailed usage instructions on the command-line tool.
