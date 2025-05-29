# chart_gizmo

H5Gizmos Library wrapper for Chart.js for creating applications including interactive charts.

# Development install

```bash
pip install --upgrade pip setuptools build
pip install -e .
```

# Examples

Each of the following examples launches a browser frame.
The application will terminate when you close the frame.

```bash
cd (repository)/examples
python example_barchart.py
python raw_chart.py
python state_barcharts.py
python example_linechart.py
python state_linecharts.py
python example_bubblechart.py
python gapimder_bubblecharts.py
```

# Scripts

```bash
cd (repository)/examples
csv-bar-gizmo life1999.csv -l "Country Name" -v "Value" -g "Disaggregation"
csv-line-gizmo life1999.csv -l "Country Name" -v "Value" -g "Disaggregation"
csv-bubble-gizmo gapminderDataFiveYear.csv -x "gdpPercap" -y "lifeExp" -r "pop" -g "continent" --min_radius 3 --max_radius 20

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
