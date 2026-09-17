# Environment and preparatory work

2026-09-17; local host Mac-Studio-7HR7.local. No other experiment processes were
visible in initial process listing. No pre-existing coordination file discovered.
All full model calls serialize with flock on /tmp/executable-experience-model.lock;
this is advisory and cannot exclude clients that ignore it. Wall times are descriptive,
not an isolated hardware benchmark. No heavy parallel experiment launched.
Initial SSH attempt failed host-key verification; no trust settings changed.
The advertised endpoint is on this local host; HTTPS generation succeeded.

Model discovery /engines/v1/models returned docker.io/ai/qwen3.8:27b-q4_K_M.
Docker model inspect is saved separately. Probe: user 'Reply with exactly READY.',
temperature 0, max_tokens 32; answer READY, finish_reason stop. Server usage was
57 prompt + 31 completion = 88 tokens, cached_tokens 0. Reported prompt_ms 847.288,
predicted_ms 1579.281. This probe preceded structured run logging; these values are
transcribed from tool output, not a preserved raw response. Probe is research setup.
Model response named Qwen3.8-27B-UD-Q4_K_M.gguf under the pinned bundle digest,
system_fingerprint b1-72874f5. No gradient, adapter or reusable KV interface tested
or used. Server prefix-cache reporting is preserved in full responses.

uv 0.12.13; uv-managed CPython 3.12.14. Execution in python:3.12-alpine by recorded
repo digest, network disabled, read-only filesystem, no project mount, 256MB,
1 CPU, dropped capabilities. Downloading Python and Docker image is research
infrastructure setup; not charged as repeated selected-deployment work. No dollar
billing/energy measurements; investigator/tool token use is not instrumented.
