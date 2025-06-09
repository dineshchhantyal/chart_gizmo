# Bubble Chart CLI

The `csv-bubble-gizmo` command-line tool allows you to quickly create bubble charts from CSV data files. It's based on the [BubbleChart API](../api/bubbles.md).

![Sample Bubble Chart](../screenshots/bubblechart.png)

This CLI is built on top of the [`ChartCLI`](chartcli.md) base class. For more details on the base CLI class, see the [ChartCLI Documentation](chartcli.md).

## Basic Usage

```bash
csv-bubble-gizmo filename -x "x-column" -y "y-column" -r "r-column"
```

This will create a bubble chart from the CSV file, using the "x-column" for x-axis, "y-column" for y-axis, and "r-column" for the bubble size.

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

### With Multiple Tooltip Columns

```bash
csv-bubble-gizmo gapminderDataFiveYear.csv -x "gdpPercap" -y "lifeExp" -r "pop" -g "continent" --tooltip_columns "country,year"
```

### Complete Customization Example

```bash
csv-bubble-gizmo gapminderDataFiveYear.csv -x "gdpPercap" -y "lifeExp" -r "pop" -g "continent" --min_radius 3 --max_radius 20 --width 800 --height 600 --title "Global Health & Wealth" --tooltip_columns country,gdpPercap,lifeExp,pop,year
```

## All Options

-   `-x`: Column name for x-axis values
-   `-y`: Column name for y-axis values
-   `-r`: Column name for radius/bubble size values
-   `-g`: Column name for grouping/coloring bubbles
-   `--min_radius`: Minimum radius size (default: 5)
-   `--max_radius`: Maximum radius size (default: 15)
-   `-w`, `--width`: Width of chart in pixels
-   `--height`: Height of chart in pixels
-   `--title`: Chart title
-   `--bubble_label_column`: Column for bubble labels
-   `--tooltip_columns`: **One or more columns to use for bubble tooltips on hover.** Accepts single comma-separated string.
-   `--animate`: Enable animations (default: no animation)

## Example

```bash
csv-bubble-gizmo gapminderDataFiveYear.csv -x "gdpPercap" -y "lifeExp" -r "pop" --animate
```

This will create a bubble chart with animations enabled, using the "gdpPercap" column for x-axis, "lifeExp" for y-axis, and "pop" for bubble size.
