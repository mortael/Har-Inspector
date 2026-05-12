from __future__ import annotations

import argparse
import sys

from .har import validate_har_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="har-inspector-desktop")
    parser.add_argument(
        "--validate",
        metavar="PATH",
        help="Validate a HAR file (no GUI). Returns 0 if valid.",
    )
    args = parser.parse_args(argv)

    if args.validate:
        ok, error = validate_har_file(args.validate)
        if ok:
            return 0
        print(error or "Invalid HAR", file=sys.stderr)
        return 2

    from .gui import run_gui

    run_gui()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

