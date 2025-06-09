# Bar Chart CLI

The `csv-bar-gizmo` command-line tool allows you to quickly create bar charts from CSV data files. It's based on the [BarChart API](../api/bars.md).

![Sample Bar Chart](../screenshots/barchart.png)

This CLI is built on top of the [`ChartCLI`](chartcli.md) base class. For more details on the base CLI class, see the [ChartCLI Documentation](chartcli.md).

## Basic Usage

```bash
csv-bar-gizmo data/data.csv -l "Category" -v "Amount" -g "Year"
```

This will create a bar chart from the CSV file, using the "Category" column for labels and the "Amount" column for values.

## Examples

### Simple Grouped Bar Chart

```bash
csv-bar-gizmo life1999.csv -l "Country Name" -v "Value" -g "Disaggregation"
```

### With Custom Dimensions

```bash
csv-bar-gizmo life1999.csv -l "Country Name" -v "Value" -g "Disaggregation" --width 800 --height 600
```

## All Options

-   `-l`, `--label_column`: Column name for labels (x-axis)
-   `-v`, `--value_column`: Column name for values (y-axis)
-   `-g`, `--group_column`: Column name for grouping data into series
-   `-w`, `--width`: Width of chart in pixels
-   `-H`, `--height`: Height of chart in pixels
-   `--title`: Chart title
-   `--stacked`: Use stacked bar chart (default: False)
-   `--animate`: Enable animations (default: no animation)
