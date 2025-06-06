# Chart Gizmo

## Interactive Charts for Python with Chart.js and H5Gizmos

Chart Gizmo is a Python library that provides a wrapper around Chart.js using the H5Gizmos framework. It enables you to create interactive, browser-based visualizations directly from your Python code or command line.

## Features

- **Multiple Chart Types**: Create bar charts, line charts, bubble charts, histograms, and pie/donut charts
- **Simple API**: Clean, Pythonic interface for chart creation and manipulation
- **Command-line Tools**: Quickly visualize data from CSV files and other sources
- **Interactive**: Browser-based rendering with dynamic updates
- **Customizable**: Extensive options for styling and configuring charts

## Screenshots

<table>
  <tr>
    <td><img src="/docs/screenshots/barchart.png" alt="Bar Chart Example"></td>
    <td><img src="/docs/screenshots/linechart.png" alt="Line Chart Example"></td>
  </tr>
  <tr>
    <td><img src="/docs/screenshots/bubblechart.png" alt="Bubble Chart Example"></td>
    <td><img src="/docs/screenshots/histogram.png" alt="Histogram Example"></td>
  </tr>
  <tr>
    <td><img src="/docs/screenshots/pie.png" alt="Pie Chart Example"></td>
    <td><img src="/docs/screenshots/donut.png" alt="Donut Chart Example"></td>
  </tr>
  <tr>
    <td><img src="/docs/screenshots/boxplot.png" alt="Box Plot Example"></td>
  </tr>
</table>

## Installation

### Development Installation

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

## Quick Start

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

## Documentation

Chart Gizmo uses Material for MkDocs for its documentation. You can access the documentation online or run it locally.

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

Each of the following examples launches a browser frame. The application will terminate when you close the frame.

```bash
cd (repository)/examples
python example_barchart.py
python raw_chart.py
python state_barcharts.py
python example_linechart.py
python state_linecharts.py
python example_bubblechart.py
python gapimder_bubblecharts.py
python example_histogram.py
python example_boxplot.py
python state_population_boxplot.py
```

## Command-Line Tools

Chart Gizmo provides several command-line tools for quick data visualization:

### Bar Chart from CSV

```bash
csv-bar-gizmo life1999.csv -l "Country Name" -v "Value" -g "Disaggregation"
```

### Line Chart from CSV

```bash
csv-line-gizmo life1999.csv -l "Country Name" -v "Value" -g "Disaggregation"
```

### Bubble Chart from CSV

```bash
csv-bubble-gizmo gapminderDataFiveYear.csv -x "gdpPercap" -y "lifeExp" -r "pop" -g "continent" --min_radius 3 --max_radius 20
```

### Histogram

```bash
# Basic histogram with default settings
histogram-gizmo data/sample_10000.txt

# Customize the number of bins (e.g., 20, 50 bins)
histogram-gizmo data/sample_10000.txt -b 20
histogram-gizmo data/sample_10000.txt -b 50

# Create a normalized density plot instead of frequency count
histogram-gizmo data/sample_10000.txt -d

# Focus on a specific range (e.g., only values between 30-70)
histogram-gizmo data/sample_10000.txt -r 30 70

# Change the chart dimensions
histogram-gizmo data/sample_10000.txt -w 1200 --height 700

# Add a custom title
histogram-gizmo data/sample_10000.txt --title "Distribution of 10,000 Random Numbers"

# Customize axis labels
histogram-gizmo data/sample_10000.txt --x-label "Value" --y-label "Frequency"

# Combine multiple options
histogram-gizmo data/sample_10000.txt -b 50 -d -r 20 80 --title "Sample Data Distribution" -w 1000 --height 600 --x-label "Sample Values" --y-label "Probability Density"

# Read numpy file
histogram-gizmo data/perfect_normal.npy
```

### Pie Chart and Doughnut Chart from CSV

```bash
csv-pie-gizmo life1999.csv -l "Disaggregation" -v "Value" --width 800 --height 600
csv-pie-gizmo life1999.csv -l "Disaggregation" -v "Value" --width 800 --height 600 --donut
csv-pie-gizmo data/data.csv -l "Category" -v "Amount" -g "Year" --donut --donut-ratio .9
```

### Box Plot from CSV

```bash
boxplot-gizmo data/data.csv --columns "Amount" -g "Category"
```

## Credits

Chart Gizmo is built on top of the following libraries:

- [Chart.js](https://www.chartjs.org/) - Simple yet flexible JavaScript charting library
- [H5Gizmos](https://github.com/AaronWatters/H5Gizmos) - HTML5 components for Python
- [Chart.js BoxPlot plugin](https://github.com/sgratzl/chartjs-chart-boxplot) - Box plot support
