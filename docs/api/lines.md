# Lines

The `LineChart` and related classes provide line chart functionality.

## Class: LineChart

**Location:** `chart_gizmo/lines.py`

### Description
A class to represent a line chart. Inherits from `AbstractChart`.

### Key Methods
- `add_label(label, values=())`: Add a label to the chart.
- `add_dataset(dataset)`: Add a dataset to the chart.
- `add_data_values(label, values=(), background_color=None, border_color=None, border_width=1)`: Add data values to the chart.
- `get_configuration()`: Get the chart configuration.

## Class: CSVLineChart

Create a line chart from a CSV file.

### Command-line Script
- `CSVLineChartScript()`: Command-line entrypoint for CSVLineChart.
