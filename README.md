# Small service requirements determine information freshness near saturation

Anonymous. Version 1.0.0-candidate, revised 20 October 2026.

Version DOI: [10.5281/zenodo.23501620](https://doi.org/10.5281/zenodo.23501620).

A lossless stationary M/G/1 egalitarian processor-sharing queue can have the same
population distribution for very different service laws, yet quite different
information freshness. This paper identifies the near-saturation age scale from
the service CDF near zero. It proves the limiting law and every positive moment
under finite mean alone.

The main pure-power theorem covers `G(x) ~ c x^beta`, beta > 0. The regularly
varying extension includes slowly varying factors, using an explicit integral
normalization. The exponential special case gives mean-age coefficient
`pi/(2 sqrt(2))`. All claims retain Poisson input, equal sharing, an infinite
buffer, retained obsolete jobs and the freshest-delivered timestamp convention.

## Start here

- `paper.md`: complete paper, proofs, examples, limitations and references.
- `CLAIMS.md`: exact claim and evidence boundaries.
- `REVISION_RESPONSE.md`: scientific changes, without private assessment metrics.
- `code/replay.py`: bounded fresh verification, including an independent rational
  finite-chain reconstruction and a small fresh-seed simulation.
- `code/verify.py`, `code/verify_erlang.py`: original simulation implementations.
- `evidence/historical/`: supplied simulation outputs, not claimed rerun.
- `AI_INDEX.md`: machine-readable navigation in plain Markdown.

## Reproduce bounded checks

Python 3 with NumPy is required. Fresh publication replay used Python 3.14.7 and
NumPy 2.4.2; see the receipts for exact hashes.

```sh
python3 -B code/replay.py
python3 -B -O code/replay.py
python3 -B -O code/replay.py --negative-control
```

The third command must fail with a finite-chain mismatch. Checks use explicit
exceptions and remain active under optimized Python. The random diagnostic is
not a proof or a replay of the large historical simulations. The original
historical NumPy version was not recorded; no bitwise identity is asserted.

The original scripts' main routines run much larger simulations and write new
outputs beside the scripts. Run them only in a fresh working copy, preserving
the historical evidence. They are not needed to verify the analytic proof.

## Evidence limits

This is an analytic research candidate with bounded computational checks and AI
review. It is not a proof-assistant formalization or external human peer review.
No finite-load approximation error bound, cancellation-policy theorem, historical
priority guarantee or practical deployment improvement is claimed.

Text and data: CC0-1.0. Code: MIT (see LICENSE).
