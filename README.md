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
```

# Scripts

```bash
cd (repository)/examples
csv-bar-gizmo life1999.csv -l "Country Name" -v "Value" -g "Disaggregation"
```
