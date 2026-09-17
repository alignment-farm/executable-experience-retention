# Methods and interpretation boundaries

The original synthetic task reconciles paginated invoice and event records. Source
must select latest event revisions before filtering, handle duplicates, payments,
refunds, currencies, cutoff dates, void invoices, exact cents, positive balances,
and deterministic sorting/totals. Acquisition cases: seeds 101–105; fresh evaluation:
8101–8108. Six evaluation cases have positive output, one has no data and one has
no requested customers. Full inputs and expected outputs are preserved locally.

Supplied capability: business contract, schemas, read-only page API, Python standard
library, complete development inputs/answers, deterministic skill dispatch and check
runner. Acquired capability: generated solve implementation and a derived prose
procedure. The complete authoritative contract remains available to reconstruction;
this is implementation acquisition from an explicit specification, not discovery
of hidden business rules. Routine selection among unrelated tasks is not studied.

All arms can read current data by executing code, perform the same development
checks and receive runtime/development feedback for repair. Held-out gold is used
only for host-side scoring, never for selection/repair. Candidate generation has
up to three attempts. A just-built candidate's successful check is reused rather
than repeated; source-loading arms check before running the current case. Function
calls execute in fresh networkless containers with no project mount or oracle.

State across sessions:
- ready: accepted implementation file plus common tests/contract;
- lessons: corrected prose plus common tests/contract, with no implementation or
  recoverable trajectory exposed to the model;
- archive: accepted source and development experience inside ZIP with a manifest;
- cache: lessons initially, then the first successful reconstruction saved to disk.
The researcher retains raw logs for all conditions; those are not a model tool or
input in lessons-only sessions. This is an explicit restrictive retention policy,
not a claim that an agent with accessible logs would have to regenerate. Archive
recovery loads its code directly. Independent cache acquisition uses the same
stateless model prompt as the first lessons-only request and is charged separately.

Acquisition history: two 180s default-thinking HTTP timeouts produced no candidate.
A small serving-mode probe motivated one pre-evaluation switch to non-thinking mode,
300s deadlines, unchanged weights/cap. The selected candidate passed development
on its first attempt. A model-generated lesson incorrectly described empty events;
one targeted correction used the supplied contract and source audit. Original and
corrected notes remain. A separate no-event diagnostic is research audit work. No
held-out implementation outcome guided these adjustments. All subsequent generations
use the same selected configuration. No claim is made about default-thinking quality.

Costs: count API page reads, candidate checks, invocations, all model responses,
reported input/output/cache tokens and observed wall time. Model cache-token fields
are native server reports, not a billing calculation. Disk executable caching is a
different mechanism. Failed HTTP requests have wall time but unknown token usage.
Artifact packaging, manual audit, downloads and investigator/tool tokens are not
fully timed; they are disclosed research overhead, never silently assigned zero.
The measured deployment totals cover instrumented model and execution work, not a
complete economic cost or an isolated timing benchmark. Calls are serialized under
a local advisory lock; hardware exclusivity is not established. No dollars, joules,
confidence intervals or population-level significance are inferred.

Limits: one model/digest and one small, deterministic, stable task family; two empty
cases and six nonempty cases; no interface/requirement revisions, autonomous skill
retrieval, stochastic replications or trained memory. The task asks for a reusable
routine even on empty requests; a general-purpose agent could short-circuit a known
empty customer selection. Thus measured reconstruction work is policy-specific, not
a lower bound on every possible solver. Each generated implementation is checked
against small fixtures, not formally proved. Gold uses an independently written
Decimal-based reference plus hand-derived edge tests; broader reference bugs remain
possible. API data flow uses code in every arm: no primitive-versus-code effect is
identified. An equal observed success rate does not establish statistical equivalence.
