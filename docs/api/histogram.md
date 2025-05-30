# Histogram

The `HistogramBarChart` class provides histogram chart functionality.

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

Creates a histogram bar chart from numerical data using numpy's histogram functionality. Inherits from `BarChart`.

### Key Methods

- `create_histogram(data)`: Create a histogram from data.
- `from_file(filename, **kwargs)`: Create a histogram from a file.

### Command-line Script

- `HistogramGizmoScript()`: Command-line script to create histogram from file.
