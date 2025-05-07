import { Chart } from './chart';

export const name = "chart_gizmo_js"; // for testing purposes

// example for testing purposes
export function createSimpleBarChart(
  ctx: CanvasRenderingContext2D,
  labels: string[],
  data: number[]
) {
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Example',
        data,
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(255, 159, 64, 0.2)',
          'rgba(255, 205, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(201, 203, 207, 0.2)'
        ],
      }]
    },
    options: {
      plugins: {
        datalabels: {
          anchor: 'end',
          align: 'top'
        },
      }
    }
  });
};

export function gizmo_click (canvas: HTMLCanvasElement, chart: Chart, callback: (arg0: any) => void) {
  canvas.addEventListener('click', (event) => {
    const points = chart.getElementsAtEventForMode(event, 'nearest', { intersect: true }, false);
    if (points.length) {
      const firstPoint = points[0];
      const index = firstPoint.index;
      const datasetIndex = firstPoint.datasetIndex;
      const label = chart.data.labels?.[index] ?? null;
      const value = chart.data.datasets[datasetIndex].data[firstPoint.index];
      callback({ index, label, value, datasetIndex });
    }
  });
}
