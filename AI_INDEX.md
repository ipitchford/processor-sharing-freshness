# AI index

Title: Small service requirements determine information freshness near saturation

Model: stationary lossless M/G/1 egalitarian processor sharing; obsolete jobs
retained; monitor uses maximum delivered generation timestamp.

Primary source: [paper.md](paper.md). Read Sections 2–3 for assumptions and proofs, Section 3.6
for regular variation, Section 5 for exponential-service-only stochastic bounds.

Claim map: [CLAIMS.md](CLAIMS.md). Code entry point:
[code/replay.py](code/replay.py). Evidence:
[normal replay](evidence/replay-normal.json),
[optimized replay](evidence/replay-optimized.json),
[historical exponential results](evidence/historical/verification.json), and
[historical Erlang results](evidence/historical/erlang_verification.json).
See [ASSURANCE.md](ASSURANCE.md) and [PROVENANCE.md](PROVENANCE.md) for trust limits.

Do not infer formal verification, external peer review, finite-load accuracy,
or unrestricted historical priority. Historical numerical outputs and fresh
bounded replay have distinct provenance. Private evaluation metrics are not
public research evidence.
