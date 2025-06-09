# ChartCLI

The `ChartCLI` class is the base class for all command-line interfaces in the `chart_gizmo` library. It provides a flexible framework for creating charts from the command line, handling argument parsing, chart creation, and chart display.

## Description

The `ChartCLI` class is designed to be subclassed by specific chart CLI implementations. Subclasses should implement the `create_chart` method to define how charts are created based on parsed arguments.

### Subclasses

-   [`CSVChartCLI`](bubble.md): Handles charts created from CSV files.

## Usage

### Running as Gizmos Window

If the user wants to run the CLI as a gizmos window, the implementation can look like this:

```python
def CSVPieChartScript():
    """Command-line entrypoint for CSVPieChart"""
    cli = CSVChartCLI(CSVPieChart,
                      {
                          "custom_commands_args": [
                              {
                                  "name": "donut",
                                  "flags": ["-d", "--donut"],
                                  "help": "Create a donut chart instead of a pie chart",
                                  "action": "store_true"  # No type or required for boolean flags
                              },
                              {
                                  "name": "donut_ratio",
                                  "flags": ["--donut-ratio"],
                                  "help": "Ratio for the donut hole size (0-1)",
                                  "required": False,
                                  "default": 0.5,
                                  "type": float
                              }
                          ]
                      }
                    )
    cli.run()
```

### Custom `create_chart` Method

Alternatively, users can define a custom `create_chart` method in their subclass to handle specific chart creation logic:

```python
from chart_gizmo.cli import ChartCLI

class MyCustomCLI(ChartCLI):
    def create_chart(self, args):
        # Custom chart creation logic
        pass

cli = MyCustomCLI(MyChartClass)
cli.run()
```

## Key Methods

-   `parse_args(args=None)`: Parse command-line arguments.
-   `create_chart(args)`: Create a chart from parsed arguments (must be implemented by subclasses).
-   `run(args=None)`: Parse arguments, create the chart, and serve it.

## Common Arguments

-   `--width`: Chart width in pixels (default: 400)
-   `--height`: Chart height in pixels (default: 400)
-   `--stacked`: Create a stacked chart
-   `--log`: Use logarithmic scale for the y-axis
-   `--log-x`: Use logarithmic scale for the x-axis
-   `--animate`: Enable or disable animations (default: `False`)

## Links

-   [API Documentation for ChartCLI](../api/charts.md)
-   [CLI Documentation Index](index.md)
