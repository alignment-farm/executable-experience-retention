# Amendment 01 — during acquisition, before evaluation

The first full acquisition HTTP request exceeded the 180s timeout. Its failed
attempt is preserved in evidence/calls/acquisition-0/measurement-0.json. Native
server metrics during this call showed one busy slot and zero deferred requests;
reported generation throughput was about 20 tokens/s. A 4096-token cap plus prompt
prefill can exceed 180s. This is a transport deadline issue, not yet evidence of
failure to acquire the task.

The already-running process keeps its predeclared single retry. Subsequent
processes use a 300s HTTP deadline, same model and token cap. This accommodates the
full predeclared generation budget without selecting on answer quality. Unknown
tokens in timed-out requests must be disclosed, not silently treated as zero.
Generation wall time includes the failed transport attempt. Initial call timestamps
and response finish reasons are retained. No evaluation outcome was seen when this
amendment was written. The original 90min/32-call research bounds remain.

Implementation corrections before evaluation: cache uses a persisted file;
summary counts candidate-check executions as well as final invocations; isolated
containers are cleaned up on host timeout; fresh reproduction output directories
are supported. None changes workload or information supplied to the model.

Avoid redundant checks: a freshly built candidate's successful development check
serves as the invocation check; only its current request is then executed. Ready,
archive and cached calls run development plus current in one container batch.
All arms therefore execute the same five checks per successful request, with extra
checks only for actual failed candidates. The extra container for build vs current
is recorded and is a harness implementation cost, not intrinsic to reconstruction.
