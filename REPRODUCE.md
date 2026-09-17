# Reproduce

Requirements: uv, Docker with Linux containers, and the served model listed in
`evidence/model-inspect.json`. Endpoint configured in `scripts/experiment.py`.
No Python dependencies beyond the standard library. No credentials in this repo.

```sh
docker pull python@sha256:b64631e04e4920160c50fbe8d8df828f7f35f06f425cb44aa09bca53e708a35a
uv run --python 3.12 python scripts/test_harness.py
```

Original evidence is immutable for reproduction. Choose a **new** output directory:

```sh
export EER_RUN_DIR="$PWD/reproductions/run-01"
uv run --python 3.12 python scripts/experiment.py acquire
uv run --python 3.12 python scripts/experiment.py evaluate
uv run --python 3.12 python scripts/experiment.py summarize
```

Call directories refuse overwrite. A partially completed acquisition/evaluation is
not automatically resumed; preserve it and use another output directory for a new
run. The budget is at most 32 named model calls with at most one transport retry
per call and a 90-minute pre-call deadline. Requests use 300-second timeouts after the recorded initial acquisition timeout.
Temperature zero is not a cross-runtime bitwise reproducibility guarantee.

Model requests and full responses are under evidence/calls; response usage and
server timing fields are preserved. Candidate source, development checks, build
failures, held-out inputs, gold, outputs, source hashes and API-call traces are
separate files. Gold stays in the host-side evaluator; container execution receives
source and input only. The acquired source and original archive are researcher
artifacts; they are never passed to the lessons or initial cache prompts.

Each candidate is checked on all five development cases. Ready, archive and cached
invocations check those cases before the fresh request. A just-built candidate
uses its already-completed development check instead of redundantly repeating it.
All failed candidate checks must be included in costs. A known
single task family is dispatched by the harness; autonomous selection among many
skills is outside this study. The environment is deterministic and read-only.

For offline verification of original outputs, see `scripts/verify_evidence.py`
when available. For model-free re-execution, see `scripts/replay.py`. Neither
requires inference or a network connection after the container image is present.
