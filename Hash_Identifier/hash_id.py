# CLI entrypoint

#!/usr/bin/env python3
"""hash_id — identify hash formats by prefix, length, and shape."""

import argparse
import sys
from hash_id.identifier import identify
from hash_id.display import render


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="hash_id",
        description="Identify hash types from a hash string.",
    )
    parser.add_argument(
        "hash",
        nargs="?",
        help="Hash string to identify. Reads from stdin if omitted.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of the rich table.",
    )
    args = parser.parse_args()

    if args.hash:
        value = args.hash
    elif not sys.stdin.isatty():
        value = sys.stdin.read().strip()
    else:
        parser.print_help()
        sys.exit(3)

    result = identify(value)

    if args.json:
        import json
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["candidates"] else 2)
    else:
        sys.exit(render(result))


if __name__ == "__main__":
    main()
