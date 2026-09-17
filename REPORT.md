# Retaining executable experience: bounded stable-use result

**Completed 17 September 2026.** In this small, fully specified invoice-reconciliation
workload, retaining code avoided repeated model generation without improving observed
accuracy. All four conditions passed all eight fresh requests. When reconstruction
was allowed to cache its first implementation, its later reconstruction cost disappeared.
Direct recovery from an archive also avoided generation. The demonstrated benefit is
availability of executable source under these policies, not a special property of a
formal skill library.

## Observed future behavior and work

| Persistence policy | Complete success | Future model calls | Prompt / completion tokens | All API reads | Measured wall time |
|---|---:|---:|---:|---:|---:|
| Ready acquired source | 8/8 | 0 | 0 / 0 | 698 | 1.91 s |
| Procedural lessons, source discarded each session | 8/8 | 8 | 57,216 / 6,476 | 698 | 668.08 s |
| Source in recoverable archive | 8/8 | 0 | 0 / 0 | 698 | 1.93 s |
| Lessons, then cache first reconstruction | 8/8 | 1 | 7,150 / 795 | 698 | 86.87 s |

These are all eight paired requests, not success-conditioned averages. Six have
nonempty positive balances; all four arms also passed both empty-result cases.
There were no evaluation repair calls, failed candidates, runtime failures or hidden
quality failures. Each reconstruction passed its development checks on the first
candidate. Every arm incurred 440 development-check page reads and 258 current-data
page reads. Thus the observed difference is not extra environment access or search
for a successful evaluation candidate.

The cache arm spent 85.17 s on its first request and 1.70 s on the remaining seven
combined, with no further model calls. The matching seven ready-source requests took
1.66 s. This descriptive difference does not establish a meaningful execution-speed
difference. Archive recovery directly loaded the original source; it never asked the
model to rewrite it. Its source hash matched the ready implementation on every request.

The server reported 38 cached prompt tokens per evaluation generation: 304 in lessons
and 38 in cache. These are subsets of prompt tokens. Most prompt processing was not
reported as cached. Executable disk caching and model prefix caching are different
mechanisms. No token-to-dollar conversion or inference of unreported KV capabilities
is made. Wall times are measured on this shared machine, not an isolated benchmark.

## Acquisition, failures and setup costs

Two initial default-thinking requests each timed out after 180 s without returning
a candidate. Both failures are preserved; their token usage is unknown. A diagnostic
probe supported selecting the server's non-thinking option. Before evaluation, we
froze that mode for acquisition and every reconstruction, retaining the same weights
and 4,096-token cap and extending the HTTP deadline to 300 s.

The selected acquisition produced a 3,399-byte implementation in one successful call:
6,467 prompt and 848 completion tokens, 81.22 s of model wait, plus 0.26 s and 55 API
reads for development checks. The routine passed complete-output checks, not merely
syntax or execution checks.

Lesson construction cost 7,326 prompt / 618 completion tokens and 73.73 s. Investigator
review found an incorrect assertion that no events implies empty output. The source
and contract instead preserve unpaid invoice balances. One targeted correction cost
1,086 prompt / 632 completion tokens and 40.10 s. Both lesson versions and an explicit
unpaid-invoice diagnostic remain local. The corrected 2,695-byte prose contains no
recoverable implementation. This was a real representation-construction error and
repair, not an evaluation failure or proof that prose must lose information.

For a selected deployment starting from the same acquired experience, add successful
acquisition and checking to every arm, and lesson construction/correction only to the
two lesson-based arms. Instrumented setup-plus-eight-request costs are:

| Policy | Prompt / completion tokens | Instrumented seconds | API reads |
|---|---:|---:|---:|
| Ready | 6,467 / 848 | 83.39 | 753 |
| Archive | 6,467 / 848 | 83.41 | 753 |
| Lessons | 72,095 / 8,574 | 863.40 | 753 |
| Cache | 22,029 / 2,893 | 282.18 | 753 |

These selected costs exclude the abandoned serving-mode search. Across the entire
study, the structured ledger records 14 HTTP attempts, including the two timeouts,
79,245 known prompt and 9,369 known completion tokens, and 1,303.65 s of measured HTTP
wait. Two additional capability probes add 74 prompt and 33 completion tokens, for
**16 HTTP attempts and 88,721 known tokens, plus unknown timeout usage**. The initial
probe is a transcription from tool output; the second has a saved raw response.
The retry also incurred its prescribed three-second backoff. This is not an exact
whole-study token total.

Research overhead additionally includes paper retrieval, harness/workload construction,
Python/container downloads, investigator review, diagnostic execution, harness tests,
and final replay. These are not assigned zero cost: investigator tokens and much of
this overhead were not instrumented. Artifact packaging and audit time are also not
fully timed. The tables cover measured model and execution work, not a complete
financial or engineering-cost accounting. Replay alone re-executed all 32 current
requests (1,032 API page reads), separately from deployment costs.

## What this comparison identifies

The full business contract, schemas, Python environment and five labeled development
cases are supplied to every arm. The model acquires an implementation from those
materials; it does not discover hidden business rules. Lessons are derived from the
same successful acquisition and keep the full contract available. Every condition
uses executable data flow, current observations, checking and repair opportunities.
There is no primitive-action-versus-code comparison.

The lessons-only condition deliberately excludes source and recoverable logs from
future model inputs. Raw researcher logs remain for audit, outside the model's tools
and the networkless execution container. Therefore its repeated-generation cost is
conditional on that retention policy. An agent that keeps source in a log is represented
by the archive condition, and one that changes policy after reconstructing is represented
by cache. It would be incorrect to generalize the lessons-only cost to either of them.

The results support EX1's avoided-work prediction for this stable workload, with no
observed quality advantage. The cache and archive controls delimit that explanation:
the savings arise from having usable code available, and reconstruction need only be
paid once if its result may persist. Equal checks/API reads and no extra evaluation
sampling address part of EX3, but this is not a causal estimate for arbitrary agent
architectures. EX2 (interface/requirement changes) was not tested; a revision experiment
was unnecessary to resolve the stable-use question within this commission.

Limits include one served model/digest, one synthetic deterministic family, eight
requests, no stochastic replications and supplied dispatch to a known routine. The
interface asks for a reusable function even for an empty request; another solver could
short-circuit a known empty customer list. These costs are not a lower bound on all
competent task-solving policies. A tie on eight cases does not prove equal reliability.
There is no claim about neural learning, broad skill selection, mutable adapters or
changing task requirements.

## Provenance and reproduction

Public method donors are [SkillCraft 2603.00718v2](https://arxiv.org/html/2603.00718v2)
for acquired executable routines and checking, and the
[TroVE compute-matched re-evaluation 2507.22069v2](https://arxiv.org/html/2507.22069v2)
for accounting for sampling and selection work. No donor code or dataset was reused,
and no author-reported benchmark result was reproduced. Versioned HTML and serialized,
cached arXiv query metadata are in [sources](sources/README.md).

Initial protocol/harness: `bc3ea13`; serving diagnosis: `d49fa90`; frozen evaluation
code and acquired artifacts: `3328619` (full hash in
[evaluation-code-revision.txt](evidence/evaluation-code-revision.txt)). The served
model bundle is `sha256:f04d0a543b642a6f0d06590973b124bc4e8700ddf7e99b669ec6c4ab1ef561ef`;
all 12 instrumented successful responses ended with `stop` and reported backend
fingerprint `b1-72874f5`. The container digest is also pinned locally.

The [reproduction guide](REPRODUCE.md), [protocol and amendments](protocol/initial.md),
[detailed methods/limits](results/methods-and-limits.md), [paired tables](results/tables.md),
[machine-readable summary](results/summary.json) and raw [evaluation records](evidence/evaluation-records.json)
provide the full trail. The offline audit recomputed all eight gold outputs and checked
all 32 recorded scores/source identities; fresh-container replay reproduced all 32
outcomes. Verification logs and a SHA256 file manifest accompany the evidence.
