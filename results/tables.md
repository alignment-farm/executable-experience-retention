| Retention policy | Exact success | Model calls | Prompt tokens | Completion tokens | Reported cached tokens | API calls, all checks + current | Total wall seconds |
|---|---:|---:|---:|---:|---:|---:|---:|
| archive | 8/8 | 0 | 0 | 0 | 0 | 698 | 1.925 |
| cache | 8/8 | 1 | 7,150 | 795 | 38 | 698 | 86.871 |
| lessons | 8/8 | 8 | 57,216 | 6,476 | 304 | 698 | 668.084 |
| ready | 8/8 | 0 | 0 | 0 | 0 | 698 | 1.909 |

All evaluation attempts are included. Setup is separate. Cached tokens are a subset of prompt tokens, not an additional token charge. Wall seconds include model calls and local orchestration; hardware exclusivity was not established.

| Seed | ready | lessons | archive | cache |
|---|---:|---:|---:|---:|
| 8101 | pass (0.248s) | pass (82.507s) | pass (0.249s) | pass (85.172s) |
| 8102 | pass (0.244s) | pass (82.441s) | pass (0.243s) | pass (0.247s) |
| 8103 | pass (0.242s) | pass (82.474s) | pass (0.241s) | pass (0.241s) |
| 8104 | pass (0.246s) | pass (82.442s) | pass (0.252s) | pass (0.245s) |
| 8105 | pass (0.238s) | pass (82.420s) | pass (0.233s) | pass (0.241s) |
| 8106 | pass (0.225s) | pass (82.389s) | pass (0.235s) | pass (0.238s) |
| 8107 | pass (0.235s) | pass (82.440s) | pass (0.238s) | pass (0.239s) |
| 8108 | pass (0.231s) | pass (90.971s) | pass (0.235s) | pass (0.247s) |
