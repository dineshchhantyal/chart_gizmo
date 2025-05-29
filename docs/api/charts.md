# Charts (Base Class)

The `AbstractChart` class is the base for all chart types in Chart Gizmo. It provides common methods and configuration for bar, line, bubble, and histogram charts.

## Class: AbstractChart

**Location:** `chart_gizmo/abstract_chart.py`

### Key Methods
- `clear()`: Clear the chart data.
- `update()`: Update the chart data.
- `add_label(label, values=())`: Add a label to the chart.
- `add_dataset(dataset)`: Add a dataset to the chart.
- `add_data_values(label, values=(), background_color=None, border_color=None, border_width=1)`: Add data values to the chart.
- `get_configuration()`: Get the chart configuration.
- `get_default_options()`: Get the default chart options.

All specific chart types inherit from this class and may override or extend its methods.
