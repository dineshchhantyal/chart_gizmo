from chart_gizmo.bubbles import BubbleChart
from H5Gizmos import serve

# Create a simple bubble chart for city data
chart = BubbleChart(width=600, height=400, title="Population vs. Cost of Living")

chart.options["responsive"] = False


# Add bubble data values (list of dicts with x, y, r)
chart.add_data_values("West Coast", [
    {"x": 10, "y": 20, "r": 8, "tooltip": "San Francisco: High tech hub"},
    {"x": 25, "y": 15, "r": 12, "tooltip": "LA: Entertainment capital"},
    {"x": 40, "y": 30, "r": 6,  "tooltip": "Portland: Rose City"}
], background_color="rgba(54, 162, 235, 0.5)")

chart.add_data_values("East Coast", [
    {"x": 15, "y": 25, "r": 10, "tooltip": "NYC: Financial center"},
    {"x": 30, "y": 18, "r": 7, "tooltip": "Boston: Academic hub"},
], background_color="rgba(255, 99, 132, 0.5)")

# Display the chart
serve(chart.show())