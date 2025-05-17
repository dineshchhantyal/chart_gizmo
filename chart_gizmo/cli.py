"""
Generic CSV → Chart → serve helper for any chart class whose constructor signature is:
    C(csv_file, label_column, value_column, group_column=None, width=..., height=..., stacked=..., configuration=None, options=None)
"""
def csv_chart_cli(chart_cls):
    import argparse, os, sys, csv
    from H5Gizmos import serve

    p = argparse.ArgumentParser(
        description=f"Create a {chart_cls.__name__} from a CSV file."
    )
    p.add_argument("csv_file", help="Path to CSV file")
    p.add_argument("-l", "--label_column", help="Label column name")
    p.add_argument("-v", "--value_column", help="Value column name")
    p.add_argument("-g", "--group_column", help="Group column name")
    p.add_argument("-w", "--width", type=int, default=400, help="Chart width")
    p.add_argument("-H", "--height", type=int, default=400, help="Chart height")
    p.add_argument("-s", "--stacked", action="store_true", help="Stacked bars")
    args = p.parse_args()

    if not os.path.exists(args.csv_file):
        print(f"Error: file not found: {args.csv_file}", file=sys.stderr)
        sys.exit(1)

    with open(args.csv_file, newline="") as f:
        dicts = list(csv.DictReader(f))

    # pick defaults from headers if not given
    headers = dicts[0].keys() if dicts else []
    lc = args.label_column or next(iter(headers), None)
    vc = args.value_column or (list(headers)[1] if len(headers) > 1 else None)
    gc = args.group_column or (list(headers)[2] if len(headers) > 2 else None)

    chart = chart_cls(
        args.csv_file, lc, vc, gc,
        width=args.width, height=args.height, stacked=args.stacked
    )
    serve(chart.show())