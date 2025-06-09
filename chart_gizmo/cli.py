"""
Class-based command-line interface for chart_gizmo.
Provides flexible CSV chart creation from the command line.
"""
import argparse
import csv
import os
import sys

from H5Gizmos import serve


class ChartCLI:
    """
    Base class for chart command-line interfaces.

    This class provides a flexible framework for creating charts from the command line.
    It handles argument parsing, chart creation, and chart display.

    Subclasses should implement the `create_chart` method to define how charts are created
    based on parsed arguments.

    **Subclasses:**
    - [`CSVChartCLI`](../api/cli.md): Handles charts created from CSV files.

    **Usage:**
    ```python
    from chart_gizmo.cli import ChartCLI

    class MyCustomCLI(ChartCLI):
        def create_chart(self, args):
            # Custom chart creation logic
            pass

    cli = MyCustomCLI(MyChartClass)
    cli.run()
    ```

    **Key Methods:**
    - `parse_args(args=None)`: Parse command-line arguments.
    - `create_chart(args)`: Create a chart from parsed arguments (must be implemented by subclasses).
    - `run(args=None)`: Parse arguments, create the chart, and serve it.

    **Common Arguments:**
    - `--width`: Chart width in pixels (default: 400)
    - `--height`: Chart height in pixels (default: 400)
    - `--stacked`: Create a stacked chart
    - `--log`: Use logarithmic scale for the y-axis
    """

    def __init__(self, chart_cls, description=None):
        """
        Initialize a CLI for the given chart class.

        Parameters
        ----------
        chart_cls : class
            The chart class to create (e.g., CSVBarChart, CSVLineChart)
        description : str, optional
            Custom description for the CLI
        """
        self.chart_cls = chart_cls
        self.description = description or f"Create a {chart_cls.__name__}"
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create the argument parser with common chart options.

        Returns
        -------
        argparse.ArgumentParser
            Configured argument parser
        """
        parser = argparse.ArgumentParser(description=self.description)
        self._add_common_arguments(parser)
        return parser

    def _add_common_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Add arguments common to all chart types.

        Parameters
        ----------
        parser : argparse.ArgumentParser
            Parser to add arguments to
        """
        parser.add_argument("-w", "--width", type=int, default=400,
                           help="Chart width in pixels")
        parser.add_argument("-H", "--height", type=int, default=400,
                           help="Chart height in pixels")
        parser.add_argument("-s", "--stacked", action="store_true",
                           help="Create a stacked chart")
        parser.add_argument("--log", action="store_true",
                           help="Use logarithmic scale for y-axis")
        parser.add_argument("--log-x", action="store_true",
                           help="Use logarithmic scale for x-axis")

    def parse_args(self, args=None):
        """
        Parse command-line arguments.

        Parameters
        ----------
        args : list, optional
            Arguments to parse (default: sys.argv)

        Returns
        -------
        argparse.Namespace
            Parsed arguments
        """
        return self.parser.parse_args(args)

    def create_chart(self, args):
        """
        Create a chart from parsed arguments.

        Must be implemented by subclasses.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed arguments

        Returns
        -------
        Chart
            The created chart object
        """
        raise NotImplementedError("Subclasses must implement create_chart")

    def run(self, args=None):
        """
        Run the CLI: parse args, create and serve the chart.

        Parameters
        ----------
        args : list, optional
            Command-line arguments (default: sys.argv)
        """
        parsed_args = self.parse_args(args)
        chart = self.create_chart(parsed_args)

        # Apply common settings
        if getattr(parsed_args, "log", False):
            chart.logarithmic()
        if getattr(parsed_args, "log_x", False):
            chart.logarithmic(axis="x")

        # Serve the chart
        serve(chart.show())


class CSVChartCLI(ChartCLI):
    """
    CLI for creating charts from CSV files.
    """
    def __init__(self, chart_cls, custom_args=None, description=None):
        """
        Initialize a CLI for the given chart class.

        Parameters
        ----------
        chart_cls : class
            The chart class to create (e.g., CSVBarChart, CSVLineChart)
        custom_args : dict, optional
            Custom arguments configuration e.g. {
                "custom_commands_args": [
                    {"name": "custom_arg", "flags": ["-x", "--custom-arg"], "help": "Custom argument", "required": False}
                ]
            }
        description : str, optional
            Custom description for the CLI
        """
        self.custom_args = custom_args or {}
        super().__init__(chart_cls, description)

    def _add_common_arguments(self, parser):
        """Add CSV-specific, custom, and common chart arguments."""
        super()._add_common_arguments(parser)
        parser.add_argument("csv_file", help="Path to CSV file")
        parser.add_argument("-l", "--label_column", help="Column for labels (x-axis)")
        parser.add_argument("-v", "--value_column", help="Column for values (y-axis)")
        parser.add_argument("-g", "--group_column", help="Column for grouping data series")
        parser.add_argument("-t", "--title", help="Chart title")
        parser.add_argument(
            '--animate',
            action='store_true',
            help='Enable animations (default: no animation)'
        )


        # Add any custom command arguments
        self._add_custom_arguments(parser)

    def _has_custom_arg(self, arg_name):
        """Check if there's a custom argument with a given name"""
        if not self.custom_args or "custom_commands_args" not in self.custom_args:
            return False

        for arg in self.custom_args.get("custom_commands_args", []):
            flags = arg.get("flags", [])
            if any(flag.replace("-", "") == arg_name.replace("-", "") for flag in flags):
                return True
        return False

    def _add_custom_arguments(self, parser):
        """Add custom arguments from configuration"""
        if not self.custom_args or "custom_commands_args" not in self.custom_args:
            return

        for arg in self.custom_args.get("custom_commands_args", []):
            name = arg.get("name")
            flags = arg.get("flags", [])
            help_text = arg.get("help", "")
            required = arg.get("required", False)
            action = arg.get("action", None)
            arg_type = arg.get("type", None)
            default = arg.get("default", None)

            if not flags or not name:
                continue

            kwargs = {"help": help_text}

            # Handle action arguments differently (like store_true for boolean flags)
            if action:
                kwargs["action"] = action
            else:
                kwargs["required"] = required
                if arg_type is not None:
                    kwargs["type"] = arg_type
                if default is not None:
                    kwargs["default"] = default

            parser.add_argument(*flags, dest=name, **kwargs)

    def create_chart(self, args):
        """Create a chart from a CSV file based on parsed arguments."""
        # Validate CSV file exists
        if not os.path.exists(args.csv_file):
            print(f"Error: file not found: {args.csv_file}", file=sys.stderr)
            sys.exit(1)

        # Read CSV and determine columns
        with open(args.csv_file, newline="") as f:
            dicts = list(csv.DictReader(f))

        if not dicts:
            print(f"Error: CSV file is empty or invalid", file=sys.stderr)
            sys.exit(1)

        # Pick column names (from args or default to first columns)
        headers = list(dicts[0].keys())
        label_col = args.label_column or headers[0]
        value_col = args.value_column or (headers[1] if len(headers) > 1 else None)
        group_col = args.group_column or (headers[2] if len(headers) > 2 else None)

        # Extract all args as kwargs for the chart constructor
        kwargs = {
            "csv_file": args.csv_file,
            # "label_column": label_col,
            # "value_column": value_col,
            # "group_column": group_col,
            "width": args.width,
            "height": args.height,
            "stacked": args.stacked
        }

        # Add custom args and other specific args (like r_column) if present
        for key, value in vars(args).items():
            if key not in kwargs and value is not None and key != "log" and key != "log_x":
                kwargs[key] = value

        return self.chart_cls(**kwargs)

