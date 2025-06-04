# Line Chart CLI

The `csv-line-gizmo` command-line tool allows you to quickly create line charts from CSV data files. It's based on the [LineChart API](../api/lines.md).

![Sample Line Chart](../screenshots/linechart.png)

## Basic Usage

```bash
csv-line-gizmo data.csv -l "Date" -v "Value"
```

This will create a line chart from the CSV file, using the "Date" column for labels (x-axis) and the "Value" column for values (y-axis).

## Examples

### Simple Line Chart

```bash
csv-line-gizmo life1999.csv -l "Country Name" -v "Value"
```

### Multiple Series Line Chart

```bash
csv-line-gizmo life1999.csv -l "Country Name" -v "Value" -g "Disaggregation"
```

### With Custom Dimensions

```bash
csv-line-gizmo life1999.csv -l "Country Name" -v "Value" --width 800 --height 600
```

## All Options

- `-l`, `--label`: Column name for labels (x-axis)
- `-v`, `--value`: Column name for values (y-axis)
- `-g`, `--group`: Column name for grouping data into series
- `-w`, `--width`: Width of chart in pixels
- `--height`: Height of chart in pixels
- `--title`: Chart title
