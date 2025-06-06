from chart_gizmo.boxplot import CSVBoxPlotChart
from H5Gizmos import serve

chart = CSVBoxPlotChart(
    csv_file="data/data.csv",
    columns=["Amount"],
    group_column="Year",
    title="Box Plot Example",
)
serve(chart.show())