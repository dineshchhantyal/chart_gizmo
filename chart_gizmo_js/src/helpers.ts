import { Chart } from "./chart";

export const name = "chart_gizmo_js"; // for testing purposes

// example for testing purposes
export function createSimpleBarChart(
  ctx: CanvasRenderingContext2D,
  labels: string[],
  data: number[]
) {
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Example",
          data,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(255, 159, 64, 0.2)",
            "rgba(255, 205, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(54, 162, 235, 0.2)",
            "rgba(153, 102, 255, 0.2)",
            "rgba(201, 203, 207, 0.2)",
          ],
        },
      ],
    },
    options: {
      plugins: {
        datalabels: {
          anchor: "end",
          align: "top",
        },
      },
    },
  });
}

/**
 * Configure chart.js options to use a logarithmic scale for the y-axis.
 * @param {config} - The chart configuration object, modified in place.
 * @param {axis} - The axis to configure (default is 'y').
 */
export function configureLogarithmicScale(config: any, axis: string = "y") {
  const scales = config.options.scales || {};
  const yAxis = scales[axis] || {};
  yAxis.type = "logarithmic";
  yAxis.ticks = {
    callback: function (value: number) {
      if (value === 0) {
        return "0";
      } else if (value < 0) {
        return "";
      } else {
        return Number.isInteger(Math.log10(value)) ? value : "";
      }
    },
  };
  config.options.scales = scales;
  return config;
}

/**
 * Replace the data in a chart.
 * @param {Chart} chart - The chart instance to update.
 * @param {any} data - The new data to set.
 */
export function replaceData(chart: Chart, data: any) {
  chart.data = data;
  chart.update();
}

/**
 * This function is used to add a click event listener to a canvas element
 * that contains a Chart.js chart. When the canvas is clicked, it retrieves
 * the data point closest to the click position and calls the provided callback
 * function with the index, label, value, and datasetIndex of that data point.
 *
 * @param {HTMLCanvasElement} canvas - The canvas element containing the chart.
 * @param {Chart} chart - The Chart.js chart instance.
 * @param {function} callback - The callback function to be called with the data point information.
 * @param {string} [action='click'] - The event action to listen for (default is 'click').
 * @param {string} [selection='nearest'] - The selection mode for the chart (default is 'nearest').
 * @returns {void}
 */
export function gizmo_click(
  canvas: HTMLCanvasElement,
  chart: Chart,
  callback: (arg0: any) => void,
  action = "click",
  selection = "nearest"
) {
  canvas.addEventListener(action, (event) => {
    const points = chart.getElementsAtEventForMode(
      event,
      selection,
      { intersect: true },
      false
    );
    if (points.length) {
      const firstPoint = points[0];
      const index = firstPoint.index;
      const datasetIndex = firstPoint.datasetIndex;
      const label = chart.data.labels?.[index] ?? null;
      const value = chart.data.datasets[datasetIndex].data[firstPoint.index];
      callback({ action, index, label, value, datasetIndex });
    }
  });
}

/**
 * Configures custom tooltips for bubble charts that can display custom data
 * from the tooltip property of data points.
 *
 * @param {Chart} chart - The Chart.js chart instance.
 * @returns {void}
 */
export function configureCustomTooltips(chart: Chart) {
  const tooltipPlugin = chart.options.plugins?.tooltip;
  console.log("Configuring custom tooltips for bubble chart");
  if (tooltipPlugin) {
    tooltipPlugin.callbacks = {
      label: function (context: any) {
        const dataPoint = context.raw;

        // Check if tooltip property exists on the data point
        if (dataPoint && dataPoint.tooltip) {
          return dataPoint.tooltip + " " + (context.dataset.label || "");
        }

        // Fallback to dataset label
        return context.dataset.label || "";
      },
    };
  }
}
