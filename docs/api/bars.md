# Bars

The `BarChart` and related classes provide bar chart functionality.

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

A class to represent a bar chart. Inherits from `RawChart`.

### Key Methods

- `add_label(label, values=())`: Add a label to the chart.
- `add_dataset(dataset)`: Add a dataset to the chart.
- `add_data_values(label, values=(), background_color=None, border_color=None, border_width=1)`: Add data values to the chart.
- `get_configuration()`: Get the chart configuration.

## Class: TabularBarChart

Create a bar chart from a tabular data source.

## Class: CSVBarChart

Create a bar chart from a CSV file.

### Command-line Script

- `CSVBarChartScript()`: Command-line entrypoint for CSVBarChart.
