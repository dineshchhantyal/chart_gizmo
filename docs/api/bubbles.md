# Bubbles

The `BubbleChart` and related classes provide bubble chart functionality.

## Class: BubbleChart

**Location:** `chart_gizmo/bubbles.py`

### Description
A class to represent a bubble chart. Inherits from `AbstractChart`.

### Key Methods
- `add_data_values(label, values=(), background_color=None, border_color=None, border_width=1)`: Add data values to the chart.
- `get_default_options()`: Get the default options for the bubble chart.

## Class: CSVBubbleChart

Loads a CSV and creates a bubble chart.

### Command-line Script
- `CSVBubbleChartScript()`: Command-line entrypoint for CSVBubbleChart.
