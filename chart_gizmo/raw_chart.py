
#from H5Gizmos import Html, Text, Button, Stack, serve, do
from H5Gizmos import jQueryComponent, do, get
import importlib.resources

class RawChart(jQueryComponent):

    def __init__(self, configuration=None, width=400, height=400):
        # canvas tag with width and height
        tag = f'<canvas id="myChart" width="{width}" height="{height}"></canvas>'
        super().__init__(tag)
        package_root = importlib.resources.files("chart_gizmo")
        # load the js file from the package
        js_path = package_root / "js" / "chart_gizmo.umd.js"
        self.js_file(str(js_path))
        self.configuration = configuration

    def get_configuration(self):
        # override this method to get the configuration in subclasses
        return self.configuration

    def configure_jQuery_element(self, element):
        super().configure_jQuery_element(element)
        dom_canvas = element[0].querySelector('*')
        Chart = self.window.chart_gizmo_js.Chart
        console = self.window.console
        #do(console.log("test log", self.window))
        #do(console.log("chart_gizmo_js loaded", self.window.chart_gizmo_js))
        #do(console.log("Chart loaded", Chart))
        #do(console.log("dom_canvas", dom_canvas))
        configuration = self.get_configuration()
        my_chart = self.cache("my_chart", self.new(Chart, dom_canvas, configuration))
        self.chart = my_chart

    async def getBase64URL(self, type=None, quality=1):
        if type is not None:
            return await get(self.chart.toBase64Image(type, quality))
        else:
            return await get(self.chart.toBase64Image())
        
    async def getBase64ImageData(self):
        # only for png
        url = await self.getBase64URL()
        prefix = "data:image/png;base64,"
        assert url.startswith(prefix), f"Invalid base64 image data: {url[:40]}..."
        base64_data = url[len(prefix):]
        return base64_data
    
    async def getImageBinary(self):
        import base64
        base64_data = await self.getBase64ImageData()
        # decode the base64 data
        binary_data = base64.b64decode(base64_data)
        # convert to bytes
        return bytes(binary_data)
    
    async def saveImage(self, filename):
        # save the image to a file
        binary_data = await self.getImageBinary()
        with open(filename, "wb") as f:
            f.write(binary_data)

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
    from H5Gizmos import serve, Button, Stack, Html, schedule_task, Text
    # create a button to get the base64 image
    def button_clicked(*arguments):
        schedule_task(snapshot())
    async def snapshot():
        # get the base64 image
        base64_image = await chart.getBase64URL()
        txt = repr(base64_image[:40])
        display.add(Text(f"Base64 image: {txt}..."))
        # create an image tag with the base64 image
        img_tag = f'<img src="{base64_image}" />'
        # show the image in a new window
        snap = Html(img_tag)
        display.add(snap)
        await chart.saveImage("chart.png")
        display.add(Text("Image saved as chart.png"))
    button = Button("Get Base64 Image", on_click=button_clicked)
    chart = example_bar_chart()
    display = Stack([button, chart])
    serve(display.show())

if __name__ == "__main__":
    # run the example
    serve_example()