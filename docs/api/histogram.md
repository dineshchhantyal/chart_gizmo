# Histogram

The `HistogramBarChart` class provides histogram chart functionality based on [Chart.js Bar Charts](https://www.chartjs.org/docs/latest/charts/bar.html) with histogram-specific configuration. It uses [NumPy's histogram function](https://numpy.org/doc/stable/reference/generated/numpy.histogram.html) for data binning and analysis. Learn more about histograms on [Wikipedia](https://en.wikipedia.org/wiki/Histogram).

![Sample Histogram Chart](../screenshots/histogram.png)

## Basic Usage

```python
from H5Gizmos import serve
import numpy as np
from chart_gizmo.histogrambar import HistogramBarChart

# Generate sample data - a mix of two normal distributions
np.random.seed(42)  # For reproducibility
data1 = np.random.normal(loc=0, scale=1, size=1000)  # Mean 0, Std dev 1
data2 = np.random.normal(loc=3, scale=0.5, size=500)  # Mean 3, Std dev 0.5
combined_data = np.concatenate([data1, data2])

# Create the histogram with 40 bins
histogram = HistogramBarChart(
    data=combined_data,
    y_label="Probability Density"
)

# Display the histogram
serve(histogram.show())
```

## Class: HistogramBarChart

**Location:** `chart_gizmo/histogrambar.py`

### Description

A class to represent a histogram bar chart. Inherits from [`AbstractChart`](../api/charts.md).

Creates a histogram bar chart from numerical data using numpy's histogram functionality. Inherits from `BarChart`.

### Constructor Parameters

-   `width` (int): Chart width in pixels (default: 600)
-   `height` (int): Chart height in pixels (default: 400)
-   `title` (str): Chart title
-   `bins` (int): Number of bins for the histogram
-   `animate` (bool): Enable or disable animations. Default is `False` (no animation). Controlled by the symbolic constant `ANIMATION_DEFAULT`.

### Key Methods

-   `create_histogram(data)`: Create a histogram from data.
-   `from_file(filename, **kwargs)`: Create a histogram from a file.
-   `add_label(label)`: Add a label for each data point to the chart. The label should match the dataset value size.
-   `set_data(data)`: Set the data for the histogram. Data should be a list or NumPy array of numerical values.
-   `on_click_call(callback, action='click', selection='nearest')`: Set a callback function for click events on the chart. See [OnClick Event Example](../examples/#onclick-event-example).
-   `saveImage(filepath)`: Asynchronous method to save the chart as a PNG image file. Must be awaited when called. See [Chart Image Export Example](../examples/#chart-image-export).
    -   `filepath`: Path where the image file will be saved

## Example

```python
from chart_gizmo.histogrambar import HistogramBarChart
from H5Gizmos import serve

chart = HistogramBarChart(title="Example Histogram", animate=False)

chart.set_data([1, 2, 2, 3, 3, 3, 4, 4, 4, 4])

serve(chart.show())
```

### Command-line Script

-   `HistogramGizmoScript()`: Command-line script to create histogram from file.

See the [Histogram CLI documentation](../cli/histogram.md) for detailed usage instructions on the command-line tool.
