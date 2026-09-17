# Amendment 02 — bounded acquisition diagnosis, before evaluation

Both initial acquisition HTTP attempts timed out at 180s; no candidate source or
quality result was returned. Preserve both failures and unknown token usage.
A diagnostic 64-token READY probe using chat_template_kwargs.enable_thinking=false
returned READY in 2 completion tokens, no reasoning_content, versus 31 completion
tokens and reasoning_content in the original probe. Raw response is retained in
evidence/no-thinking-probe.json. Probe prompt identical; temperature 0. This verifies
observable behavior of the option for this server, not a guarantee about internals.

Select this non-thinking serving mode for a single recovery acquisition and every
subsequent generation/lesson/reconstruction in the experiment. Same fixed weights,
4096-token cap, 300s deadline, maximum 3 candidate attempts. Use acquisition-compact
as the recovery attempt prefix. If no functioning acquisition results, stop with
the preserved resource/quality limitation. No further workload tuning is planned.
This is research search cost, not a silently removed failed deployment.

No held-out candidate performance has been observed. The selected deployment will
be reported with its successful setup; total research costs will also include the
two timed-out requests and both capability probes. Native metrics snapshots do not
provide exact billed/generated tokens for canceled requests, so no exact total-token
claim can include those unknown amounts.
