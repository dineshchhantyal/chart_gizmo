from chart_gizmo.pie import PieChart
from H5Gizmos import serve, Text, Stack


# Create a pie chart
pie_chart = PieChart(width=600, height=400)

# Add labels and data
pie_chart.add_label("Apples")
pie_chart.add_label("Oranges")
pie_chart.add_label("Bananas")
pie_chart.add_label("Grapes")
pie_chart.add_label("Kiwi")
pie_chart.add_data_values(
    "Fruits",
    [45, 25, 15, 10, 5],
    background_color=[
        "rgba(255, 99, 132, 0.7)",
        "rgba(54, 162, 235, 0.7)",
        "rgba(255, 206, 86, 0.7)",
        "rgba(75, 192, 192, 0.7)",
        "rgba(153, 102, 255, 0.7)"
    ]
)

# Create a text component to display click information
click_info = Text("Click on a segment to see details.")

# Define the click callback function
def click_callback(event):
    if event and "label" in event:
        click_info.text(f"You clicked on: {event['label']} with value: {event['value']}")
    else:
        click_info.text("Click event did not contain label information.")

def hover_callback(event):
    if event and "label" in event:
        click_info.text(f"Hovering over: {event['label']} with value: {event['value']}")
    else:
        click_info.text("Hover event did not contain label information.")

# Set the click callback
pie_chart.on_click_call(click_callback)
pie_chart.on_click_call(hover_callback, "hover")

# Create a stack to display the chart and the text component
interface = Stack([
    "Pie Chart Example",
    pie_chart,
    click_info
])

# Serve the interface
serve(interface.show())