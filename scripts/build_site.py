#!/usr/bin/env python3
"""Audit the static privacy-safe dashboard; there is no data-driven build step.

The former generator could reproduce owner-provided financial inputs and
unsupported projections. It is intentionally replaced by a static-site audit.
Run from the repository root with: python3 scripts/build_site.py
"""
import sys
sys.dont_write_bytecode = True

from check_site import main

if __name__ == "__main__":
    raise SystemExit(main())
