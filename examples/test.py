from chart_gizmo.pie import CSVPieChart
from H5Gizmos import serve



chart = CSVPieChart("data/data.csv", label_column="Category", value_column="Amount", width=400, height=400, stacked=False, donut=True, donut_ratio=0.8)


serve(chart.show())
