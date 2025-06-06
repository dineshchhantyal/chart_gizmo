import csv
from collections import defaultdict
from chart_gizmo.boxplot import BoxPlotChart  # Assuming this is the correct import for BoxPlotChart
from H5Gizmos import serve

filename = "historical_state_population_by_year.csv"
data = []
with open(filename, newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        # Each row: [state, year, population]
        state, year, population = row
        data.append((state, int(year), int(population)))

# Group populations by state
state_populations = defaultdict(list)
for state, year, population in data:
    state_populations[state].append(population)

labels = sorted(state_populations.keys())
box_data = [state_populations[state] for state in labels]

chart = BoxPlotChart(title="Population Distribution per State (All Years)")
chart.data["labels"] = labels
chart.add_data_values("Population", box_data)
serve(chart.show())