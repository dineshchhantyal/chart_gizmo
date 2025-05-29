import os
import csv
from chart_gizmo import bubbles
from H5Gizmos import serve, Stack

# point at the gapminder file
data_path = os.path.join(os.path.dirname(__file__), "gapminderDataFiveYear.csv")

def load_gapminder_data(path=data_path):
    """Load Gapminder CSV into dicts."""
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield {
                "country": row["country"],
                "year": int(row["year"]),
                "pop": float(row["pop"]),
                "continent": row["continent"],
                "lifeExp": float(row["lifeExp"]),
                "gdpPercap": float(row["gdpPercap"]),
            }

class GapminderBubbleVisualizer:
    """Bubble chart: X=GDP per Capita, Y=Life Expectancy,
       Size=Population, Color=Continent."""
    def __init__(self, path=data_path):
        self.data = list(load_gapminder_data(path))
        self.years = sorted({d["year"] for d in self.data})
        self.continents = sorted({d["continent"] for d in self.data})
        # simple color palette
        self.colors = {
            "Asia":    "#1f77b4",
            "Europe":  "#ff7f0e",
            "Africa":  "#2ca02c",
            "Americas":"#d62728",
            "Oceania": "#9467bd"
        }

    def create_bubble_chart(self):
        # Use the most recent year
        year = self.years[-1]

        # Create a basic chart with simpler options first
        chart = bubbles.BubbleChart(width=900, height=600)
        chart.options = {
            "responsive": True,
            "maintainAspectRatio": False,
            "scales": {
                "x": {
                    "type": "logarithmic",  # Explicitly set logarithmic scale
                    "min": 200,
                    "max": 100000,
                    "title": {"display": True, "text": "GDP per Capita (log scale)"}
                },
                "y": {
                    "min": 30,
                    "max": 85,
                    "title": {"display": True, "text": "Life Expectancy (years)"}
                }
            },
            "plugins": {
                "title": {
                    "display": True,
                    "text": f"Gapminder Data ({year})",
                    "font": {"size": 18}
                },
                "datalabels": {
                    "display": False  # Disable data labels for clarity
                }

            }
        }

        # Make bubbles better sized for visibility
        buckets = {c: [] for c in self.continents}
        for d in self.data:
            if d["year"] != year:
                continue

            # Better bubble scaling
            r = max(3, min(20, round((d["pop"]**0.4)/120, 1)))  # Better scaling with min/max bounds

            buckets[d["continent"]].append({
                "x": d["gdpPercap"],
                "y": d["lifeExp"],
                "r": r,
                "country": d["country"],
                "pop": d["pop"]
            })

        # Add each continent as a series
        for cont, pts in buckets.items():
            if not pts:
                continue

            base = self.colors.get(cont, "#888")
            chart.add_data_values(
                cont,
                pts,
                background_color=base+"80",
                border_color=base
            )


        return chart

    def serve_visualization(self):
        # Create a simple visualization
        chart = self.create_bubble_chart()
        display = Stack([
            "Gapminder Bubble Chart - GDP vs Life Expectancy",
            chart
        ])
        serve(display.show())

if __name__ == "__main__":
    GapminderBubbleVisualizer().serve_visualization()