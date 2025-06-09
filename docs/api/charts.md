# Charts (Base Class)

The `AbstractChart` class is the base for all chart types in Chart Gizmo. It provides common methods and configuration for bar, line, bubble, and histogram charts, building upon the functionality of [Chart.js](https://www.chartjs.org/docs/latest/) and delivered through [H5Gizmos](https://github.com/AaronWatters/H5Gizmos).

## Class: AbstractChart

**Location:** `chart_gizmo/abstract_chart.py`

**Inherits from:** `RawChart`

**Description:**
Base class for all chart types (bar, line, bubble, etc.) that provides common functionality while specific chart types set their own chart type. It handles data configuration, chart options, and interactions with the Chart.js library.

### Constructor

```python
AbstractChart(configuration=None, width=400, height=400, stacked=False, options=None)
```

**Parameters:**

-   `configuration`: Optional dictionary with chart configuration. If provided, it overrides other parameters.
-   `width`: Chart width in pixels (default: 400)
-   `height`: Chart height in pixels (default: 400)
-   `stacked`: Boolean indicating whether the chart should be stacked (default: False)
-   `options`: Optional dictionary with Chart.js options
-   `animate`: Boolean to enable or disable animations (default: False, controlled by the symbolic constant `ANIMATION_DEFAULT`)

### Key Methods

-   `clear()`: Clear the chart data and return the chart instance for method chaining.
-   `update()`: Update the chart's rendered data and return the chart instance.
-   `add_label(label, values=())`: Add a label to the chart with optional values. Returns the chart instance.
    -   `label`: Label text
    -   `values`: Optional values associated with the label
-   `add_dataset(dataset)`: Add a dataset object to the chart. Returns the chart instance.
    -   `dataset`: A `DataSet` object containing data to be visualized
-   `add_data_values(label, values=(), background_color=None, border_color=None, border_width=1)`: Add data values to the chart with styling options. Returns the chart instance.
    -   `label`: Label for the dataset
    -   `values`: Values for the dataset
    -   `background_color`: Background color for the dataset elements
    -   `border_color`: Border color for the dataset elements
    -   `border_width`: Border width for the dataset elements
-   `get_configuration()`: Get the complete chart configuration as a dictionary ready for Chart.js.
-   `get_default_options()`: Get the default chart options, can be overridden by subclasses.
-   `saveImage(filepath)`: Asynchronous method to save the chart as a PNG image file. Must be awaited when called. See [Chart Image Export Example](../examples/#chart-image-export).
    -   `filepath`: Path where the image file will be saved
-   `on_click_call(callback, action='click', selection='nearest')`: Set a callback function for click events on the chart. This method uses the [Chart.js getElementsAtEventForMode API](https://www.chartjs.org/docs/latest/developers/api.html#getelementsateventformode-e-mode-options-usefinalposition) under the hood. See [OnClick Event Example](../examples/#onclick-event-example).
    -   `callback`: Function to be called when the chart is clicked.
    -   `action`: Type of action to listen for (default: `'click'`).
    -   `selection`: Selection mode for the click event (default: `'nearest'`).
-   `logarithmic(axis='y', value=True)`: Set the specified axis (default: 'y') to a logarithmic scale. This method modifies the chart configuration to use a logarithmic scale for the given axis. It can be chained with other methods for configuration. Returns the chart instance for method chaining.

    -   `axis` (str): The axis to set to logarithmic scale. Default is `'y'`.
    -   `value` (bool): Whether to enable (`True`) or disable (`False`) the logarithmic scale. Default is `True`.

All specific chart types inherit from this class and may override or extend its methods. The configuration options follow [Chart.js documentation](https://www.chartjs.org/docs/latest/configuration/) but are exposed through a Python interface.
