# Bars

The `BarChart` and related classes provide bar chart functionality.

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
