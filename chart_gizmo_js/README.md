
# `chart_gizmo` Javascript bundle build

This directory builds the Javascript bundle used
by the `chart_gizmo` Python package.

The bundle is "frozen" into the Python package
and is not automatically rebuilt.

To manually update and rebuild the bundle
run the following commands:

```
rm -rf package-lock.json node_modules dist
npm install
npm run build
```

The bundle will automatically be copied to `../chart_gizmo/js/chart_gizmo.umd.js`
in the Python package.
