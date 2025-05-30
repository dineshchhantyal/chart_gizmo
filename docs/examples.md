# Examples

Each of the following examples launches a browser frame. The application will terminate when you close the frame.

## Running the Examples

> **Note:** All example commands below assume you are running them from the `/examples` directory of your Chart Gizmo installation.

Navigate to the examples directory in the repository:

```bash
cd (repository)/examples
```

## Bar Chart Examples

```bash
python example_barchart.py
python state_barcharts.py
```

## Line Chart Examples

```bash
python example_linechart.py
python state_linecharts.py
```

## Bubble Chart Examples

```bash
python example_bubblechart.py
python gapimder_bubblecharts.py
python tooltip_customization.py
```

## Raw Chart Example

```bash
python raw_chart.py
```

## Code Examples

### Bar Chart: Quarterly Sales Comparison

```python
from H5Gizmos import serve
import chart_gizmo.bars as bars

# Create a bar chart comparing quarterly sales data
chart = bars.BarChart()

# Add product categories
chart.add_label("Electronics")
chart.add_label("Clothing")
chart.add_label("Home Goods")

# Add quarterly data for each product category
chart.add_data_values("Q1", [45000, 32000, 28000], background_color="#3366CC")
chart.add_data_values("Q2", [52000, 38000, 31000], background_color="#DC3912")
chart.add_data_values("Q3", [48000, 42000, 36000], background_color="#FF9900")
chart.add_data_values("Q4", [60000, 52000, 40000], background_color="#109618")

# Display the chart
serve(chart.show())
```

### Line Chart: Monthly Temperature Trends

```python
from H5Gizmos import serve
import chart_gizmo.lines as lines

# Create a line chart for monthly temperature data
chart = lines.LineChart()

# Add month labels
chart.add_label("Jan")
chart.add_label("Feb")
chart.add_label("Mar")
chart.add_label("Apr")
chart.add_label("May")
chart.add_label("Jun")

# Add temperature data for two cities
chart.add_data_values("New York", [3, 4, 8, 15, 21, 26],
                      background_color="rgba(54, 162, 235, 0.2)",
                      border_color="rgba(54, 162, 235, 1)")
chart.add_data_values("San Francisco", [12, 13, 14, 15, 16, 17],
                      background_color="rgba(255, 99, 132, 0.2)",
                      border_color="rgba(255, 99, 132, 1)")

# Customize chart options
chart.options = {
    "responsive": True,
    "maintainAspectRatio": False,
    "plugins": {
        "title": {
            "display": True,
            "text": "Average Monthly Temperatures (°C)",
            "font": {"size": 16}
        }
    },
    "scales": {
        "y": {
            "title": {"display": True, "text": "Temperature (°C)"}
        },
        "x": {
            "title" : {"display": True, "text": "Month"}
        }
    }
}

# Display the chart
serve(chart.show())
```

### Bubble Chart: Simple City Data

```python
from H5Gizmos import serve
import chart_gizmo.bubbles as bubbles

# Create a simple bubble chart for city data
chart = bubbles.BubbleChart()

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

# Customize chart options
chart.options = {
    "responsive": True,
    "maintainAspectRatio": False,
    "plugins": {
        "title": {
            "display": True,
            "text": "City Data Comparison",
            "font": {"size": 16}
        }
    },
    "scales": {
        "x": {
            "title": {"display": True, "text": "Metric X"}
        },
        "y": {
            "title": {"display": True, "text": "Metric Y"}
        }
    }
}

# Display the chart
serve(chart.show())
```

### Bubble Chart: Economics and Health Indicators

```python
from H5Gizmos import serve
import chart_gizmo.bubbles as bubbles

# Create a bubble chart showing economic and health data
chart = bubbles.BubbleChart()

# Define the reference year
current_year = 2023

# Add city data with population, GDP per capita, and life expectancy
cities_data = [
    {"name": "New York", "population": 8500000, "gdp_per_capita": 75000, "life_expectancy": 81, "area": 784},
    {"name": "Tokyo", "population": 13900000, "gdp_per_capita": 45000, "life_expectancy": 84, "area": 2194},
    {"name": "Mumbai", "population": 20400000, "gdp_per_capita": 12000, "life_expectancy": 74, "area": 603},
    {"name": "Berlin", "population": 3700000, "gdp_per_capita": 41000, "life_expectancy": 82, "area": 892},
    {"name": "Rio", "population": 6700000, "gdp_per_capita": 17000, "life_expectancy": 76, "area": 1221}
]

# Add data values with size (r) proportional to population
chart.add_data_values("Global Cities", [
    {"x": city["gdp_per_capita"],
     "y": city["life_expectancy"],
     "r": city["population"] / 500000,  # Scale population for reasonable bubble size
    } for city in cities_data
], background_color="rgba(75, 192, 192, 0.6)", border_color="rgba(75, 192, 192, 1)")

# Configure chart options
chart.options = {
    "responsive": True,
    "maintainAspectRatio": False,
    "scales": {
        "x": {
            "type": "logarithmic",
            "min": 10000,
            "max": 100000,
            "title": {"display": True, "text": "GDP per Capita (log scale)"}
        },
        "y": {
            "min": 70,
            "max": 85,
            "title": {"display": True, "text": "Life Expectancy (years)"}
        }
    },
    "plugins": {
        "title": {
            "display": True,
            "text": f"Global Cities Comparison ({current_year})",
            "font": {"size": 18}
        },
        "subtitle": {
            "display": True,
            "text": "Bubble size represents population",
            "font": {"size": 14},
            "padding": {"top": 10, "bottom": 30}
        },

    }
}

# Display the chart
serve(chart.show())
```

### Histogram: Bimodal Distribution Analysis

```python
"""
Example of creating and displaying a histogram using HistogramBarChart
"""
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
    bins=40,
    width=900,
    height=500,
    density=True,  # Normalize to create a probability density
    x_label="Value",
    y_label="Probability Density"
)

# Customize the chart appearance
histogram.options["plugins"]["title"]["text"] = "Bimodal Distribution Analysis"
histogram.options["plugins"]["title"]["font"]["size"] = 18
histogram.options["plugins"]["subtitle"] = {
    "display": True,
    "text": "Mixture of Two Normal Distributions (μ₁=0, σ₁=1, n₁=1000; μ₂=3, σ₂=0.5, n₂=500)",
    "font": {"size": 14},
    "padding": {"top": 10, "bottom": 30}
}

# Display the histogram
serve(histogram.show())
```

### Bar Chart: API Methods Demonstration

```python
from H5Gizmos import serve, Stack
from chart_gizmo.bars import BarChart
from chart_gizmo.data_config import DataSet

# Create a bar chart
chart = BarChart(width=800, height=500)

# Add region labels
chart.add_label("Region 1")
chart.add_label("Region 2")

# Method 1: Add data values with custom styling
chart.add_data_values("Revenue", [350, 420],
                     background_color="rgba(54, 162, 235, 0.6)",
                     border_color="rgba(54, 162, 235, 1)",
                     border_width=2)

# Method 2: Create and add a dataset using DataSet class
dataset = DataSet("Expenses", [250, 310])
dataset.background_color = "rgba(255, 99, 132, 0.6)"
dataset.border_color = "rgba(255, 99, 132, 1)"
dataset.border_width = 2
chart.add_dataset(dataset)

# Method 3: Add data values with default styling
chart.add_data_values("Profit", [100, 110])

# Customize chart options
chart.options = {
    "responsive": True,
    "maintainAspectRatio": False,
    "plugins": {
        "title": {
            "display": True,
            "text": "Financial Performance by Region",
            "font": {"size": 16}
        },
        "legend": {"position": "bottom"}
    },
    "scales": {
        "x": {
            "title": {"display": True, "text": "Regions"},
            "grid": {
                "offset": True  # Align grid lines with bar edges
            }
        },
        "y": {
            "title": {"display": True, "text": "Amount ($1000s)"}
        }
    }
}

# Get and print the chart configuration (useful for debugging)
config = chart.get_configuration()
print("Chart configuration:")
print(config)

# Create a stack with the chart and show it
stack = Stack(["API Methods Demonstration", chart])
serve(stack.show())
```

## Pie Chart Examples

### Basic Pie Chart

```python
from H5Gizmos import serve
from chart_gizmo.pie import PieChart

# Create a new pie chart
chart = PieChart(width=600, height=400)

# Add labels for each slice
for fruit in ["Apples", "Oranges", "Bananas", "Grapes", "Kiwi"]:
    chart.add_label(fruit)

# Add data with colors
chart.add_data_values(
    "Fruits",
    [45, 25, 15, 10, 5],
    background_color=[
        "rgba(255, 99, 132, 0.7)",
        "rgba(54, 162, 235, 0.7)",
        "rgba(255, 206, 86, 0.7)",
        "rgba(75, 192, 192, 0.7)",
        "rgba(153, 102, 255, 0.7)"
    ],
    border_color="rgba(255, 255, 255, 0.8)",
    border_width=2
)

# Add click handler
def on_click(event):
    print(f"Clicked on: {event}")

chart.on_click_call(on_click)

# Serve the chart
serve(chart.show())
```

### Donut Chart

```python
from H5Gizmos import serve
from chart_gizmo.pie import PieChart

# Create a new chart and convert to donut
chart = PieChart(width=600, height=400)
chart.as_donut(0.6)  # Hole size is 60% of the radius

# Add labels and data
for category in ["Housing", "Food", "Transport", "Entertainment", "Savings"]:
    chart.add_label(category)

chart.add_data_values(
    "Budget",
    [35, 25, 15, 10, 15],
    background_color=[
        "rgba(255, 99, 132, 0.7)",
        "rgba(54, 162, 235, 0.7)",
        "rgba(255, 206, 86, 0.7)",
        "rgba(75, 192, 192, 0.7)",
        "rgba(153, 102, 255, 0.7)"
    ]
)

# Add custom options
chart.options = chart.options or {}
chart.options["plugins"] = chart.options.get("plugins", {})
chart.options["plugins"]["title"] = {
    "display": True,
    "text": "Monthly Budget Breakdown",
    "font": {"size": 18}
}

# Serve the chart
serve(chart.show())
```

### CSV Pie Chart

```python
from H5Gizmos import serve
from chart_gizmo.pie import CSVPieChart

# Create chart from CSV file
chart = CSVPieChart(
    csv_file="data/data.csv",
    label_column="Category",
    value_column="Amount",
    width=800,
    height=600,
    donut=True,
    donut_ratio=0.5
)

# Serve the chart
serve(chart.show())
```
