# Bubble Chart CLI

The `csv-bubble-gizmo` command-line tool allows you to quickly create bubble charts from CSV data files.

## Basic Usage

```bash
csv-bubble-gizmo data.csv -x "GDP" -y "Life_Expectancy" -r "Population"
```

This will create a bubble chart from the CSV file, using the "GDP" column for x-axis, "Life_Expectancy" column for y-axis, and "Population" for the bubble size.

## Examples

### Simple Bubble Chart

```bash
csv-bubble-gizmo gapminderDataFiveYear.csv -x "gdpPercap" -y "lifeExp" -r "pop"
```

### Bubble Chart with Color Grouping

```bash
csv-bubble-gizmo gapminderDataFiveYear.csv -x "gdpPercap" -y "lifeExp" -r "pop" -g "continent"
```

### With Custom Bubble Size Range

```bash
csv-bubble-gizmo gapminderDataFiveYear.csv -x "gdpPercap" -y "lifeExp" -r "pop" --min_radius 3 --max_radius 20
```

### Complete Customization Example

```bash
csv-bubble-gizmo gapminderDataFiveYear.csv -x "gdpPercap" -y "lifeExp" -r "pop" -g "continent" --min_radius 3 --max_radius 20 --width 800 --height 600 --title "Global Health & Wealth"
```

## All Options

- `-x`: Column name for x-axis values
- `-y`: Column name for y-axis values
- `-r`: Column name for radius/bubble size values
- `-g`, `--group`: Column name for grouping/coloring bubbles
- `--min_radius`: Minimum radius size (default: 5)
- `--max_radius`: Maximum radius size (default: 15)
- `-w`, `--width`: Width of chart in pixels
- `--height`: Height of chart in pixels
- `--title`: Chart title
- `--log_scale`: Use logarithmic scale for x-axis (useful for GDP/income data)
- `--x_min`: Minimum x-axis value
- `--x_max`: Maximum x-axis value
- `--y_min`: Minimum y-axis value
- `--y_max`: Maximum y-axis value
