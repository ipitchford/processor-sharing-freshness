"""Bounded verification; does not rerun the large historical simulations.

The analytic theorems are proved in paper.md. These checks concern exact
finite-chain calculations, scale constants and a small fresh-seed simulation.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path
import platform
import sys

import numpy as np
from verify import sample_age


def require(condition, message):
    if not condition:
        raise ValueError(message)


def solve(matrix, rhs):
    """Independent Gauss--Jordan implementation over fractions."""
    rows = [list(row) + [value] for row, value in zip(matrix, rhs)]
    for col in range(len(rows)):
        pivot = next(i for i in range(col, len(rows)) if rows[i][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        divisor = rows[col][col]
        rows[col] = [x / divisor for x in rows[col]]
        for i in range(len(rows)):
            if i != col:
                factor = rows[i][col]
                rows[i] = [a - factor * b for a, b in zip(rows[i], rows[col])]
    return [row[-1] for row in rows]


def finite_mean(capacity):
    states = [(old, new) for old in range(capacity + 1)
              for new in range(capacity + 1 - old)]
    indices = {state: i for i, state in enumerate(states)}
    matrix = [[Q(0) for _ in states] for _ in states]
    for row, (old, new) in enumerate(states):
        n = old + new
        if n < capacity:
            matrix[row][row] += Q(1, 2)
            matrix[row][indices[(old, new + 1)]] -= Q(1, 2)
        if old:
            matrix[row][row] += Q(old, n)
            matrix[row][indices[(old - 1, new)]] -= Q(old, n)
        if new:
            matrix[row][row] += Q(new, n)
    times = solve(matrix, [Q(1) for _ in states])
    weights = [Q(1, 2) ** n for n in range(capacity + 1)]
    return sum(w * times[indices[(n, 0)]] for n, w in enumerate(weights)) / sum(weights)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    expected = [Q(10, 3), Q(45, 14), Q(1292, 405)]
    if args.negative_control:
        expected[1] += 1
    observed = [finite_mean(k) for k in (1, 2, 3)]
    require(observed == expected, "finite-chain mean mismatch (negative control if requested)")
    # Exact algebra for the pure-power normalisation q=(eps/a)^(1/(beta+1)).
    for beta in (1, 2, 3, 4, 7):
        q, a = Q(1, 11), Q(5, 3)
        eps = a * q ** (beta + 1)
        b = q / eps
        require(b * a * q ** beta == 1, "normalisation balance")
        require(a * q ** (beta + 1) / (beta + 1) == eps / (beta + 1),
                "integral normalisation")
    # Diagnostic for the logarithmic example, gamma=1, beta=1.
    # F(q)=q log(1/q) near zero: integral=q^2(log(1/q)/2+1/4).
    logarithmic = []
    for n in (10, 20, 40, 80):
        q = math.exp(-n)
        eps = q * q * (n + 0.5)
        b = q / eps
        approximation = math.sqrt(2) / math.sqrt(eps * math.log(1 / eps))
        logarithmic.append({"minus_log_q": n, "bFq": b * q * n,
                            "b_over_asymptotic": b / approximation})
    require(abs(logarithmic[-1]["b_over_asymptotic"] - 1) < 0.03,
            "logarithmic scale diagnostic")
    sample = sample_age(0.999, 2000, 20261020)
    mean_limit = math.pi / (2 * math.sqrt(2))
    require(abs(sample["scaled_mean"] - mean_limit) <
            6 * sample["scaled_mean_se"] + 0.03, "small-sample diagnostic")
    root = Path(__file__).resolve().parents[1]
    files = ("paper.md", "code/replay.py", "code/verify.py", "code/verify_erlang.py")
    report = {
        "status": "pass", "scope": "finite exact checks and diagnostic simulation; not a proof certificate",
        "python": platform.python_version(), "numpy": np.__version__,
        "optimized": not __debug__, "finite_means": list(map(str, observed)),
        "logarithmic_scale_diagnostic": logarithmic, "fresh_seed_sample": sample,
        "sha256": {f: hashlib.sha256((root / f).read_bytes()).hexdigest() for f in files},
    }
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered)


if __name__ == "__main__":
    main()
