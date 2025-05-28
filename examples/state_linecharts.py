
"""
Interactive bar charts with state population data.
"""

from chart_gizmo import lines
import os

data_path =  os.path.join(os.path.dirname(__file__), "historical_state_population_by_year.csv")

def load_population_data(path=data_path):
    """
    Load population data from a CSV file.
    """
    import csv
    with open(path, "r") as f:
        for row in csv.reader(f):
            [abbrev, year, population] = row
            yield {
                "abbrev": abbrev,
                "year": int(year),
                "population": int(population)
            }

class PopulationData:
    """
    Class to hold population data.
    """
    def __init__(self, path=data_path, chart_class=lines.LineChart):
        self.chart_class = chart_class
        self.chart = chart_class()
        self.data = list(load_population_data(path))
        self.years = sorted(set([d["year"] for d in self.data]))
        self.states = sorted(set([d["abbrev"] for d in self.data]))

    def data_by_year(self, year):
        """
        Get population data for a specific year.
        """
        labels = [datum["abbrev"] for datum in self.data if datum["year"] == year]
        data = [
            f"Population in {year}",
            [datum["population"] for datum in self.data if datum["year"] == year]
        ]
        return labels, data

    def year_barchart(self, year=None):
        """
        Create a bar chart for a specific year.
        """
        if year is None:
            year = self.years[0]
        labels, data = self.data_by_year(year)
        chart = self.chart_class()
        for label in labels:
            chart.add_label(label)
        [title, values] = data
        #print("title", title)
        #print("values", values)
        chart.add_data_values(title, values)
        chart.logarithmic()
        self.year_chart = chart
        return chart
    def change_year(self, year):
        """
        Change the year for the bar chart.
        """
        labels, data = self.data_by_year(year)
        chart = self.year_chart
        chart.clear()
        for label in labels:
            chart.add_label(label)
        [title, values] = data
        chart.add_data_values(title, values)
        chart.update()

    def serve_year_barchart(self, year=None):
        """
        Serve a bar chart for a specific year.
        """
        from H5Gizmos import serve
        chart = self.year_barchart(year)
        serve(chart.show())

    def data_by_state(self, state):
        """
        Get population data for a specific state.
        """
        labels = [datum["year"] for datum in self.data if datum["abbrev"] == state]
        data = [
            f"Population in {state}",
            [datum["population"] for datum in self.data if datum["abbrev"] == state]
        ]
        return labels, data

    def state_barchart(self, state=None):
        """
        Create a bar chart for a specific state.
        """
        if state is None:
            state = self.states[0]
        labels, data = self.data_by_state(state)
        chart = self.chart_class()
        for label in labels:
            chart.add_label(label)
        [title, values] = data
        #print("title", title)
        #print("values", values)
        chart.add_data_values(title, values)
        chart.logarithmic()
        self.state_chart = chart
        return chart

    def change_state(self, state):
        """
        Change the state for the bar chart.
        """
        labels, data = self.data_by_state(state)
        chart = self.state_chart
        chart.clear()
        for label in labels:
            chart.add_label(label)
        [title, values] = data
        chart.add_data_values(title, values)
        chart.update()

    def serve_state_barchart(self, state=None):
        """
        Serve a bar chart for a specific state.
        """
        from H5Gizmos import serve
        chart = self.state_barchart(state)
        serve(chart.show())

    def serve_combined_charts(self):
        """
        Serve a combined bar chart for all states.
        """
        from H5Gizmos import serve, Stack
        state_chart = self.state_barchart()
        year_chart = self.year_barchart()
        display = Stack([
            "Top chart shows the population of a state over the years.",
            "Bottom chart shows the population of all states in a specific year.",
            "Click on the bars to change the year or state.",
            state_chart,
            year_chart,
            ])
        def state_chart_click(event):
            print("State chart click event:", event)
            year = event["label"]
            self.change_year(year)
        def year_chart_click(event):
            print("Year chart click event:", event)
            state = event["label"]
            self.change_state(state)
        state_chart.on_click_call(state_chart_click)
        year_chart.on_click_call(year_chart_click)
        serve(display.show())

if __name__ == "__main__":
    # Example usage
    population_data = PopulationData()
    #population_data.serve_year_barchart(2000)
    #population_data.serve_state_barchart("CA")
    population_data.serve_combined_charts()