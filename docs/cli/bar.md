# Bar Chart CLI

The `csv-bar-gizmo` command-line tool allows you to quickly create bar charts from CSV data files.

## Basic Usage

```bash
csv-bar-gizmo data.csv -l "Category" -v "Amount"
```

This will create a bar chart from the CSV file, using the "Category" column for labels and the "Amount" column for values.

## Examples

### Simple Bar Chart

```bash
csv-bar-gizmo life1999.csv -l "Country Name" -v "Value"
```

### Grouped Bar Chart

```bash
csv-bar-gizmo life1999.csv -l "Country Name" -v "Value" -g "Disaggregation"
```

### With Custom Dimensions

```bash
csv-bar-gizmo life1999.csv -l "Country Name" -v "Value" -g "Disaggregation" --width 800 --height 600
```

## All Options

- `-l`, `--label`: Column name for labels (x-axis)
- `-v`, `--value`: Column name for values (y-axis)
- `-g`, `--group`: Column name for grouping data into series
- `-w`, `--width`: Width of chart in pixels
- `--height`: Height of chart in pixels
- `--title`: Chart title
- `--stacked`: Use stacked bar chart (default: False)
- `--horizontal`: Use horizontal bar chart (default: False)
