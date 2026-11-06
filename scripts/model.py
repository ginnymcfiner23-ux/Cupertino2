#!/usr/bin/env python3
"""Public projection generator intentionally disabled.

The repository must not contain private property inputs or unsupported outputs.
Use the source-linked formulas on costs.html and scenarios.html, and keep any
owner-specific records in a private workspace. No model output is generated.
"""


def main() -> int:
    print(
        "No property-specific projection was generated. This public repository "
        "does not store private values, assumptions, or scenario outputs."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
