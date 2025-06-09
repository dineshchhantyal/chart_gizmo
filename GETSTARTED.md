# Getting Started with Chart Gizmo

Welcome to Chart Gizmo! This guide will help you get started with creating interactive charts using Python and Chart.js through the H5Gizmos framework.

## Installation

To begin, clone the repository and set up your environment:

```bash
# Clone the repository
git clone https://github.com/AaronWatters/chart_gizmo.git
cd chart_gizmo

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install --upgrade pip setuptools build
pip install -e .
```

## Quick Start Example

Here is a simple example to create a bar chart:

```python
from H5Gizmos import serve
import chart_gizmo.bars as bars

# Create a bar chart
chart = bars.BarChart()

# Add labels
chart.add_label("Category A")
chart.add_label("Category B")
chart.add_label("Category C")

# Add data
chart.add_data_values("Series 1", [45, 32, 28], background_color="#3366CC")
chart.add_data_values("Series 2", [52, 38, 31], background_color="#DC3912")

# Display the chart
serve(chart.show())
```

Save this code to a file (e.g., `example_barchart.py`) and run it:

```bash
python example_barchart.py
```

This will open a browser window displaying your chart. Close the browser window to terminate the application.

## Documentation

Chart Gizmo uses [MkDocs](https://www.mkdocs.org/) with the Material theme for its documentation. You can access the documentation online or run it locally.

### Online Documentation

Visit our [documentation site](https://AaronWatters.github.io/chart_gizmo/) for comprehensive guides, API references, and examples.

### Local Documentation

To build and view the documentation locally:

1. Install MkDocs and the Material theme:

   ```bash
   pip install mkdocs mkdocs-material
   ```

2. Preview the documentation:

   ```bash
   mkdocs serve
   ```

   This will start a local server at `http://127.0.0.1:8000/` where you can view the documentation.

3. Build the documentation as static files:

   ```bash
   mkdocs build
   ```

   This will generate the static site in the `site/` directory.

## Examples

Explore more examples in the [Examples Documentation](https://AaronWatters.github.io/chart_gizmo/api/examples/). These examples demonstrate various chart types, including bar charts, line charts, bubble charts, histograms, and pie charts.

To run the examples, navigate to the `examples` directory and execute the desired script. For example:

```bash
cd examples
python example_barchart.py
python example_linechart.py
python example_bubblechart.py
```

## Next Steps

- Experiment with the provided examples to understand the capabilities of Chart Gizmo.
- Refer to the API documentation for detailed information on available methods and options.
- Use the command-line tools for quick data visualization from CSV files and other sources.

Enjoy creating interactive charts with Chart Gizmo!