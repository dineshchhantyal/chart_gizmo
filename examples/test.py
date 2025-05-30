from chart_gizmo.bars import BarChart
from H5Gizmos import serve
import asyncio

# Step 1: Create the chart first without any async operations
def create_chart():
    # Create a bar chart comparing quarterly sales data
    chart = BarChart(width=50, height=200, stacked=False)

    # Add product categories
    chart.add_label("Electronics")
    chart.add_label("Clothing")
    chart.add_label("Home Goods")

    # Add quarterly data for each product category
    chart.add_data_values("Q1", [45000, 32000, 28000], background_color="#3366CC")
    chart.add_data_values("Q2", [52000, 38000, 31000], background_color="#DC3912")
    chart.add_data_values("Q3", [48000, 42000, 36000], background_color="#FF9900")
    chart.add_data_values("Q4", [60000, 52000, 40000], background_color="#109618")

    return chart

# Step 2: Create a separate function to handle displaying the chart
def display_chart():
    # Get the chart object
    chart = create_chart()
    
    # Let's use the raw_chart approach that works with H5Gizmos
    from H5Gizmos import Button, Stack, Text, schedule_task

    async def save_image_task():
        try:
            await chart.saveImage("quarterly_sales_comparison.png")
            feedback.text = "Chart image saved as quarterly_sales_comparison.png"
        except Exception as e:
            feedback.text = f"Error saving image: {e}"

    # Create a button to save the image
    save_button = Button("Save Chart Image", on_click=lambda *args: schedule_task(save_image_task()))
    
    # Create a text element for feedback
    feedback = Text("Click the button to save image")
    
    # Create a layout with the chart and controls
    component = Stack([save_button, feedback, chart])
    
    # The show() method returns a coroutine that needs to be awaited first,
    # but serve() expects a component directly, not a coroutine
    serve(component)

# Run the display function directly (no asyncio.run needed)
# This lets serve() manage its own event loop
display_chart()