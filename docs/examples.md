# Examples

Each of the following examples launches a browser frame. The application will terminate when you close the frame.

## Running the Examples

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
```

## Raw Chart Example

```bash
python raw_chart.py
```

## Code Examples

### Bar Chart: Monthly Sales Data Example

```python
from H5Gizmos import serve
import chart_gizmo.bars as bars

# Create a bar chart comparing monthly sales data
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

### Basic Line Chart

```python
from H5Gizmos import serve
import chart_gizmo.lines as lines

# Create a simple line chart
chart = lines.LineChart()

# Add labels (e.g., months)
chart.add_label("Jan")
chart.add_label("Feb")
chart.add_label("Mar")
chart.add_label("Apr")
chart.add_label("May")
chart.add_label("Jun")

# Add data values for a dataset
chart.add_data_values("Sample Data", [12, 19, 3, 5, 2, 3])

# Display the chart
serve(chart.show())
```

### Basic Bubble Chart

```python
from H5Gizmos import serve
import chart_gizmo.bubbles as bubbles

# Create a simple bubble chart
chart = bubbles.BubbleChart()

# Add a group label
chart.add_label("Cities")

# Add bubble data values (list of dicts with x, y, r)
chart.add_data_values("Population", [
    {"x": 10, "y": 20, "r": 8},   # City A
    {"x": 25, "y": 15, "r": 12},  # City B
    {"x": 40, "y": 30, "r": 6}    # City C
])

# Display the chart
serve(chart.show())
```

### Bubble Chart: City Data Comparison with X-axis and Y-axis label

```python
from H5Gizmos import serve
import chart_gizmo.bubbles as bubbles

# Create a bubble chart showing city data
chart = bubbles.BubbleChart()

# Define the current year
current_year = 2023

# Add city data with population, GDP per capita, and life expectancy
cities_data = [
    {"name": "City A", "population": 1500000, "gdp_per_capita": 25000, "life_expectancy": 75, "area": 400},
    {"name": "City B", "population": 8200000, "gdp_per_capita": 45000, "life_expectancy": 82, "area": 600},
    {"name": "City C", "population": 600000, "gdp_per_capita": 15000, "life_expectancy": 72, "area": 300}
]

# Add data values with size (r) proportional to population
chart.add_data_values("Cities", [
    {"x": city["gdp_per_capita"],
     "y": city["life_expectancy"],
     "r": city["population"] / 100000,  # Scale population for reasonable bubble size
     "name": city["name"]}  # Add name for tooltips
    for city in cities_data
])

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
            "text": f"City Comparison ({current_year})",
            "font": {"size": 18}
        },
    }
}

# Display the chart
serve(chart.show())
```
