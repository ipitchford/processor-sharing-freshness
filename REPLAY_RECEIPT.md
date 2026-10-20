# Bounded replay record

The fresh normal and optimized checks are retained in
`evidence/replay-normal.json` and `evidence/replay-optimized.json`. Each records
the source hashes at that check, interpreter mode and bounded results. Later
typesetting or archival metadata changes do not retroactively change those
historical hashes.

Both modes reconstructed the three finite-chain expectations exactly as
10/3, 45/14 and 1292/405, checked the pure-power normalizations and ran a
2,000-sample diagnostic with seed 20261020. That diagnostic returned mean
1.1074825966707935 and standard error 0.019863254275483373. It is an illustration,
not an independent proof, historical-simulation replay or finite-load guarantee.

`python3 -B code/check_negative.py` also passed: it launches the optimized
checker with an intentionally corrupted expectation and requires its rejection.
The direct `--negative-control` command is supposed to exit unsuccessfully.

The original large simulation outputs remain separately labelled under
`evidence/historical/`; they were not rerun for this revision. The analytic
proofs, not these finite checks, establish the asymptotic theorem and its
regularly varying extension.
