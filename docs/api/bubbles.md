# Bubbles

The `BubbleChart` and related classes provide bubble chart functionality based on [Chart.js Bubble Charts](https://www.chartjs.org/docs/latest/charts/bubble.html).

## Basic Usage

```python
from chart_gizmo.bubbles import BubbleChart
from H5Gizmos import serve

# Create a simple bubble chart for city data
chart = BubbleChart()

# Add bubble data values (list of dicts with x, y, r)
chart.add_data_values("West Coast", [
    {"x": 10, "y": 20, "r": 8},   # City A
    {"x": 25, "y": 15, "r": 12},  # City B
    {"x": 40, "y": 30, "r": 6}    # City C
], background_color="rgba(54, 162, 235, 0.5)")

chart.add_data_values("East Coast", [
    {"x": 15, "y": 25, "r": 10},   # City D
    {"x": 30, "y": 18, "r": 7},    # City E
], background_color="rgba(255, 99, 132, 0.5)")

# Display the chart
serve(chart.show())
```

## Class: BubbleChart

**Location:** `chart_gizmo/bubbles.py`

### Description

A class to represent a bubble chart. Inherits from `AbstractChart`.

### Key Methods

- `add_data_values(label, values=(), background_color=None, border_color=None, border_width=1)`: Add data values to the chart.
- `get_default_options()`: Get the default options for the bubble chart.
- `saveImage(filepath)`: Save the chart as a PNG image file. This is an async method and must be used with `await`.

## Class: CSVBubbleChart

Loads a CSV and creates a bubble chart.

### Command-line Script

- `CSVBubbleChartScript()`: Command-line entrypoint for CSVBubbleChart.

See the [Bubble Chart CLI documentation](../cli/bubble.md) for detailed usage instructions on the command-line tool.
