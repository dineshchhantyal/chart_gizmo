import {
  Chart,
  // Controllers
  BarController,
  BubbleController,
  DoughnutController,
  LineController,
  PieController,
  PolarAreaController,
  RadarController,
  ScatterController,

  // Elements
  ArcElement,
  BarElement,
  LineElement,
  PointElement,

  // Scales
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  RadialLinearScale,
  TimeScale,
  TimeSeriesScale,

  // Plugins
  Decimation,
  Filler,
  Legend,
  SubTitle,
  Title,
  Tooltip,
} from "chart.js";

import {
  BoxPlotController,
  BoxAndWiskers,
} from "@sgratzl/chartjs-chart-boxplot";

import ChartDataLabels from "chartjs-plugin-datalabels";
import annotationPlugin from "chartjs-plugin-annotation";

Chart.register(
  // Controllers
  BarController,
  BubbleController,
  DoughnutController,
  LineController,
  PieController,
  PolarAreaController,
  RadarController,
  ScatterController,
  BoxPlotController,
  BoxAndWiskers,

  // Elements
  ArcElement,
  BarElement,
  LineElement,
  PointElement,

  // Scales
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  RadialLinearScale,
  TimeScale,
  TimeSeriesScale,

  // Plugins
  Decimation,
  Filler,
  Legend,
  SubTitle,
  Title,
  Tooltip,

  // additional plugins
  ChartDataLabels,
  annotationPlugin
);

export { Chart };
export type { ChartConfiguration };
