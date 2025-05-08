
#from H5Gizmos import Html, Text, Button, Stack, serve, do
from H5Gizmos import jQueryComponent, do
import importlib.resources

class RawChart(jQueryComponent):
    def __init__(self, configuration, width=400, height=400):
        # canvas tag with width and height
        tag = f'<canvas id="myChart" width="{width}" height="{height}"></canvas>'
        super().__init__(tag)
        package_root = importlib.resources.files("chart_gizmo")
        # load the js file from the package
        js_path = package_root / "js" / "chart_gizmo.umd.js"
        self.js_file(str(js_path))
    def configure_jQuery_element(self, element):
        super().configure_jQuery_element(element)
        dom_canvas = element[0].querySelector('*')
        Chart = self.window.chart_gizmo_js.Chart
        console = self.window.console
        do(console.log("test log", self.window))
        do(console.log("chart_gizmo_js loaded", self.window.chart_gizmo_js))
        do(console.log("Chart loaded", Chart))
        do(console.log("dom_canvas", dom_canvas))
        my_chart = self.cache("my_chart", self.new(Chart, dom_canvas, configuration))
        self.chart = my_chart

# example usage
true = True
configuration = dict(
    type= 'bar',
    data= dict(
        labels= ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets= [dict(
            label= '# of Votes',
            data= [12, 19, 3, 5, 2, 3],
            backgroundColor= [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor= [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth= 1
        )]
    ),
    options= dict(
        scales= dict(
            y=dict(
                beginAtZero= true
            ),
        ),
        responsive= False,
    ),
)

def example_bar_chart():
    # create a RawChart object
    chart = RawChart(configuration)
    # return the chart object
    return chart

def serve_example():
    from H5Gizmos import serve
    chart = example_bar_chart()
    serve(chart.show())

if __name__ == "__main__":
    # run the example
    serve_example()