# Frozen initial protocol — 2026-09-17

Question: on a stable, deterministic reconciliation workload, what future work is
avoided by preserving acquired executable source, and what remains if a competent
reconstructor caches its first implementation?

Method donors: SkillCraft 2603.00718v2 §§3/B/D.2 (generate, execute, verify,
retain); TroVE re-evaluation 2507.22069v2 §§2–4 (count generation and selection
work). This is an original small synthetic workload, not a benchmark reproduction.
No donor code or datasets are reused. Local HTML snapshots pin paper versions.

Supplied: complete business contract, Python stdlib, deterministic paginated
read-only API, function dispatch, 5 labeled development examples and checker.
Acquired: model-written implementation; model-written contextual lessons from
that implementation and its observed checks. No gradient/adapters/KV persistence
is assumed. Endpoint-reported prefix caching is measured where returned.

Four arms on 8 fresh inputs (seeds 8101–8108), after acquisition on 101–105:
1. ready: retain acquired implementation and tests; directly load and execute.
2. lessons: retain prose lessons and tests, no source/trajectory; reconstruct in
   each fresh session. This is an explicit restricted persistence policy.
3. archive: same source survives inside ZIP acquisition log; directly recover,
   check and execute, never force regeneration.
4. cache: lessons initially; reconstruct on first request and retain the successful
   reconstruction for remaining requests. Cache is ordinary executable disk storage.

Every arm sees the same contract, current request and API and development tests.
Every invocation checks all 5 development tests, then runs the current request.
Checker feedback consists only of development failures and runtime exceptions;
held-out expected results are never model feedback. Both arms may inspect current
API data through execution; full current observations supplied to repair on runtime
failure. Repairs: at most 2 after initial candidate; acquisition at most 3 candidates.
If acquisition fails, diagnose once and freeze a new protocol before fresh evaluation.
Lesson construction: 1 call, preserve response verbatim and audit for omissions/code.
No source in reconstruction prompts. No primitive-action-only comparison.

Exact equality of complete output is primary. Save outputs, API calls, all generation
attempts, prompts/responses, failures, checks, input/output/cache tokens, wall times,
source bytes, archive recovery and actual selected deployment work. Failed attempts
count. 8 paired requests, descriptive findings only, no population-level claims.
The cache arm independently acquires its reconstruction; do not charge the whole
search to any one deployment. Aggregate acquisition separately from evaluation;
report shared vs representation-specific setup and break-even only if warranted.

Model: docker.io/ai/qwen3.8:27b-q4_K_M, pinned digest in evidence/model-inspect.json.
Temperature 0, max_tokens 4096, fixed weights; endpoint may not guarantee determinism.
Single sequential connection, 180s request deadline, at most one retry of transport
failure (logged). Shared Mac local advisory flock /tmp/executable-experience-model.lock.
No claim of isolated timing. Budget <=32 full model calls, <=90 min experiment.
Controlled execution: Python Docker image digest recorded, network none, read-only
filesystem, no host project mount, 256MB, 1 CPU, max 10s execution per batch.
Research costs (probe, method lookup, workload/harness construction) are separate
from deployable acquisition/invocation; investigator tokens not available here.

Scope stop: stable evaluation explains savings or acquisition limitation. Interface
change experiment only if needed to resolve a remaining consequential ambiguity.

Pre-run workload sizing: development invoice counts 3,4,0,5,2 (plus edge case);
evaluation counts 9,17,31,52,9,17,0,31 (plus edge case). Evaluation customer lists
cycle alfa / alfa+beta / all three, with final request explicitly selecting nobody.
This avoids an accidentally mostly-empty random workload and keeps development
context compact. Set before acquisition; no acquired program evaluated yet.
