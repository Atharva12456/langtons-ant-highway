"""Finite-state model of the width-four odd wake skeleton.

This file studies only the parity/residue skeleton, not chronological
realisability.  A column is the five-bit vector of odd translation classes on
transverse levels 0,...,4.  The signed residue theorem permits exactly six column
masks.  The y-residue theorem says that every five-column diagonal window must form
one of the same six masks.  Hence the skeletons form a one-dimensional shift of
finite type with four-column memory.
"""
from __future__ import annotations

import argparse
from itertools import product


ALLOWED = (0b00101, 0b01010, 0b10001, 0b10100, 0b10111, 0b11101)
ALLOWED_SET = frozenset(ALLOWED)


def signed_charge(mask):
    return sum((1 if t % 2 == 0 else -1)
               for t in range(5) if (mask >> t) & 1)


def diagonal_mask(window):
    """Bits t are taken from level t of column window[t]."""
    return sum(((window[t] >> t) & 1) << t for t in range(5))


def cyclic_valid(columns):
    m = len(columns)
    return all(diagonal_mask(tuple(columns[(r + t) % m] for t in range(5)))
               in ALLOWED_SET for r in range(m))


def brute_counts(max_m):
    for m in range(1, max_m + 1):
        total = with_extremes = 0
        growths = {}
        for columns in product(ALLOWED, repeat=m):
            if not cyclic_valid(columns):
                continue
            total += 1
            if any(c & 1 for c in columns) and any(c & 16 for c in columns):
                with_extremes += 1
            growth = sum(c.bit_count() for c in columns)
            growths[growth] = growths.get(growth, 0) + 1
        print(f"m={m:2d} total={total:8,d} with-extremes={with_extremes:8,d} "
              f"growths={growths}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-m", type=int, default=8)
    args = ap.parse_args()
    assert [m for m in range(32) if signed_charge(m) % 4 == 2] == list(ALLOWED)
    brute_counts(args.max_m)


if __name__ == "__main__":
    main()
