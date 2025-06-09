"""
HistogramBarChart for creating histograms from numerical data.
"""

import numpy as np
from chart_gizmo.bars import BarChart
from chart_gizmo.cli import ChartCLI
from H5Gizmos import serve
import argparse
import os
import sys

class HistogramBarChart(BarChart):
    """
    Creates a histogram bar chart from numerical data using numpy's histogram functionality.
    """

    def __init__(self, data=None, bins=10, range=None, density=False, weights=None,
                 x_label=None, y_label=None, **kwargs):
        """
        Initialize a histogram bar chart.

        Parameters
        ----------
        data : array-like, optional
            Input data to be binned
        bins : int or sequence, default=10
            Number of bins or bin edges
        range : tuple, optional
            Lower and upper range of bins
        density : bool, default=False
            If True, the result is the value of the probability density function at the bin
        weights : array-like, optional
            Weights for each data point
        width : int, default=600
            Width of the chart in pixels
        height : int, default=400
            Height of the chart in pixels
        configuration : dict, optional
            Custom chart.js configuration
        options : dict, optional
            Custom chart.js options
        x_label : str, optional
            Custom X-axis label (defaults to "Value")
        y_label : str, optional
            Custom Y-axis label (defaults to "Frequency" or "Density")
        animate : bool, optional
            Enable or disable animations
        """
        super().__init__(**kwargs)

        # Store histogram parameters
        self.bins = bins
        self.range = range
        self.density = density
        self.weights = weights
        self.x_label = x_label
        self.y_label = y_label

        # Create histogram if data is provided
        if data is not None:
            self.create_histogram(data)

    def set_data(self, data):
        """
        Set the data for the histogram and create the histogram.

        Parameters
        ----------
        data : array-like
            Input data to be binned

        Returns
        -------
        self : HistogramBarChart
            The histogram chart instance
        """
        return self.create_histogram(data)

    def create_histogram(self, data):
        """
        Create a histogram from the given data.

        Parameters
        ----------
        data : array-like
            Input data to be binned

        Returns
        -------
        self : HistogramBarChart
            The histogram chart instance
        """
        # Convert data to numpy array if it's not already
        if not isinstance(data, np.ndarray):
            data = np.array(data, dtype=float)

        # Compute histogram
        hist_values, bin_edges = np.histogram(
            data,
            bins=self.bins,
            range=self.range,
            density=self.density,
            weights=self.weights
        )

        # Clear existing data
        self.clear()

        # Create labels from bin edges with appropriate format
        if max(bin_edges) > 100:
            # Use integer format for large numbers
            labels = [f"{int(bin_edges[i])}-{int(bin_edges[i+1])}" for i in range(len(bin_edges)-1)]
        elif max(bin_edges) > 10:
            # Use 1 decimal place for medium numbers
            labels = [f"{bin_edges[i]:.1f}-{bin_edges[i+1]:.1f}" for i in range(len(bin_edges)-1)]
        else:
            # Use 2 decimal places for small numbers
            labels = [f"{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}" for i in range(len(bin_edges)-1)]

        # Add labels
        for label in labels:
            self.add_label(label)

        # Add histogram data with specific styling for a proper histogram
        # Use border_width=0 to eliminate gaps between bars
        self.add_data_values(
            "Frequency",
            hist_values,
            background_color="rgba(100, 130, 255, 0.7)",  # Semi-transparent blue
            border_color="rgba(100, 130, 255, 1.0)",      # Matching border color
            border_width=0                                # No border to avoid gaps
        )

        # Configure for true histogram appearance
        title_text = "Histogram" + (" (Density)" if self.density else "")

        # Use custom labels or defaults
        x_label = self.x_label or "Value"
        y_label = self.y_label or ("Density" if self.density else "Frequency")

        self.options = {
            "responsive": True,
            "maintainAspectRatio": False,
            "indexAxis": "x",
            "scales": {
                "x": {
                    "title": {"display": True, "text": x_label},
                    "barPercentage": 1.0,         # Full width bars
                    "categoryPercentage": 1.0,    # No gap between categories
                    "grid": {
                        "offset": False           # Ensure grid lines align with bar edges
                    }
                },
                "y": {
                    "title": {"display": True, "text": y_label},
                    "beginAtZero": True
                }
            },
            "plugins": {
                "title": {
                    "display": True,
                    "text": title_text,
                    "font": {"size": 16}
                },
                "legend": {"display": False},
                "datalabels": {
                    "display": False  # Disable data labels
                }
            },
            "datasets": {
                "bar": {
                    "barPercentage": 1.0,
                    "categoryPercentage": 1.0,
                    "borderWidth": 0
                }
            },
            "animation": {
                "duration": 800 if self.animate else 0,  # Use animation duration if enabled
                "easing": "easeInOutQuad" if self.animate else "linear"
            }
        }

        return self

    @classmethod
    def from_file(cls, filename, **kwargs):
        """
        Create a histogram from a file.

        Parameters
        ----------
        filename : str
            Path to the file. Can be either a .npy, .npz, or a text file with whitespace-separated numbers.
        **kwargs : dict
            Additional arguments to pass to the histogram constructor

        Returns
        -------
        HistogramBarChart
            The histogram chart instance
        """
        try:
            if filename.endswith(".npz"):
                # Load npz and extract the first array
                npz = np.load(filename)
                keys = list(npz.keys())
                if not keys:
                    raise ValueError(f"No arrays found in npz file: {filename}")
                data = npz[keys[0]]
            else:
                # Try numpy binary
                data = np.load(filename)
        except Exception:
            # If that fails, try loading as text
            try:
                data = np.loadtxt(filename)
            except Exception:
                raise ValueError(f"Could not load data from file: {filename}")

        # Create and return the histogram
        return cls(data=data, **kwargs)


class HistogramBarChartCLI(ChartCLI):
    """
    Command-line interface for creating histogram bar charts.
    """
    def __init__(self, chart_cls, custom_args=None, description=None):
        """
        Initialize the CLI with custom arguments.

        Parameters
        ----------
        chart_cls : class
            The chart class to create (e.g., HistogramBarChart)
        custom_args : dict, optional
            Custom arguments configuration, e.g., {
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
        """Add common and custom arguments to the parser."""
        super()._add_common_arguments(parser)
        parser.add_argument("file", help="File to read (.npy or text file with whitespace-separated numbers)")
        parser.add_argument("-b", "--bins", type=int, default=10, help="Number of bins")
        parser.add_argument("-r", "--range", type=float, nargs=2, help="Range for binning (min max)")
        parser.add_argument("-d", "--density", action="store_true", help="Normalize to create a probability density")
        parser.add_argument("--title", type=str, help="Chart title")
        parser.add_argument("--x-label", type=str, help="Custom X-axis label")
        parser.add_argument("--y-label", type=str, help="Custom Y-axis label")
        parser.add_argument("--animate", action="store_true", help="Enable animations")



    def create_chart(self, args):
        """
        Create a histogram bar chart from parsed arguments.

        Parameters
        ----------
        args : argparse.Namespace
            Parsed arguments

        Returns
        -------
        HistogramBarChart
            The created histogram chart instance
        """
        # Validate file existence
        if not os.path.exists(args.file):
            raise FileNotFoundError(f"File not found: {args.file}")

        # Load data and create histogram
        data = np.loadtxt(args.file) if args.file.endswith(".txt") else np.load(args.file)
        histogram = HistogramBarChart(
            data=data,
            bins=args.bins,
            range=tuple(args.range) if args.range else None,
            density=args.density,
            width=args.width,
            height=args.height,
            x_label=args.x_label,
            y_label=args.y_label,
            animate=args.animate
        )

        # Apply logarithmic scale if specified
        if args.log:
            histogram.logarithmic(axis="y", value=True)

        # Set custom title if provided
        if args.title:
            histogram.options["plugins"]["title"]["text"] = args.title

        return histogram


def HistogramGizmoScript():
    """Command-line script to create histogram from file"""
    cli = HistogramBarChartCLI(HistogramBarChart, description="Create a histogram bar chart from a file of numbers.")
    cli.run()


def serve_example_histogram():
    """
    Serve an example histogram.
    """
    import numpy as np
    data = np.random.randn(10000)  # 10000 points from standard normal distribution
    histogram = HistogramBarChart(data, bins=30)
    serve(histogram.show())



if __name__ == "__main__":
    # Example usage
    import numpy as np
    data = np.random.randn(10000)  # 10000 points from standard normal distribution
    histogram = HistogramBarChart(data, bins=30)
    serve(histogram.show())