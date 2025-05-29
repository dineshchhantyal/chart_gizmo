# Command Line Scripts

Chart Gizmo provides several command-line scripts for quick visualization of data.

## Bar Chart Script

```bash
csv-bar-gizmo life1999.csv -l "Country Name" -v "Value" -g "Disaggregation"
```

### Options
- `-l`, `--label`: Column name for labels
- `-v`, `--value`: Column name for values
- `-g`, `--group`: Column name for grouping

## Line Chart Script

```bash
csv-line-gizmo life1999.csv -l "Country Name" -v "Value" -g "Disaggregation"
```

### Options
- `-l`, `--label`: Column name for labels
- `-v`, `--value`: Column name for values
- `-g`, `--group`: Column name for grouping

## Bubble Chart Script

```bash
csv-bubble-gizmo gapminderDataFiveYear.csv -x "gdpPercap" -y "lifeExp" -r "pop" -g "continent" --min_radius 3 --max_radius 20
```

### Options
- `-x`: Column name for x-axis values
- `-y`: Column name for y-axis values
- `-r`: Column name for radius values
- `-g`, `--group`: Column name for grouping
- `--min_radius`: Minimum radius size
- `--max_radius`: Maximum radius size

## Histogram Script

### Basic histogram with default settings
```bash
histogram-gizmo data/sample_10000.txt
```

### Customize the number of bins
```bash
histogram-gizmo data/sample_10000.txt -b 20
histogram-gizmo data/sample_10000.txt -b 50
```

### Create a normalized density plot instead of frequency count
```bash
histogram-gizmo data/sample_10000.txt -d
```

### Focus on a specific range
```bash
histogram-gizmo data/sample_10000.txt -r 30 70
```

### Change the chart dimensions
```bash
histogram-gizmo data/sample_10000.txt -w 1200 --height 700
```

### Add a custom title
```bash
histogram-gizmo data/sample_10000.txt --title "Distribution of 10,000 Random Numbers"
```

### Customize axis labels
```bash
histogram-gizmo data/sample_10000.txt --x-label "Value" --y-label "Frequency"
```

### Combine multiple options
```bash
histogram-gizmo data/sample_10000.txt -b 50 -d -r 20 80 --title "Sample Data Distribution" -w 1000 --height 600 --x-label "Sample Values" --y-label "Probability Density"
```

### Read numpy file
```bash
histogram-gizmo data/perfect_normal.npy
```

### Options
- `-b`, `--bins`: Number of bins for the histogram
- `-d`, `--density`: Create a density plot instead of frequency count
- `-r`, `--range`: Range of values to include (min max)
- `-w`, `--width`: Width of the chart in pixels
- `--height`: Height of the chart in pixels
- `--title`: Chart title
- `--x-label`: Label for x-axis
- `--y-label`: Label for y-axis
