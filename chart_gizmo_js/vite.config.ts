import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  build: {
    lib: {
      entry: path.resolve(__dirname, 'src/index.ts'),
      name: 'MyChartLib',
      fileName: () => 'chart_gizmo_js.umd.js',
      formats: ['umd']
    },
    rollupOptions: {
      output: {
        inlineDynamicImports: true
      }
    },
    target: 'es2018',
    minify: false
  }
});
