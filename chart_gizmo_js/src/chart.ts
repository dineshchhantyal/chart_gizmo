import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  Title,
  Legend,
  Tooltip,
  ChartConfiguration
} from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import annotationPlugin from 'chartjs-plugin-annotation';

Chart.register(
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  Title,
  Legend,
  Tooltip,
  ChartDataLabels,
  annotationPlugin
);

export { Chart };
export type { ChartConfiguration };
