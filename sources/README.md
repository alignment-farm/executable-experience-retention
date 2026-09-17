# Method provenance

Retrieved 2026-09-17. arXiv query API response is cached in arxiv-metadata.xml;
one connection and one request for both version identifiers, under shared local
advisory lock with a minimum three-second gap. HTML snapshots are local, pinned
versions; SHA256 manifest will accompany final evidence.

- SkillCraft, **2603.00718v2**, https://arxiv.org/html/2603.00718v2:
  methods §§3, B, D.2 motivate acquiring executable routines, checking, retaining
  them and comparing direct execution. Here the original synthetic workload uses
  a deterministic page API and exact output checks; no public benchmark results
  are reproduced, and no donor implementation is reused.
- Compute-Matched Re-Evaluation of TroVE on MATH, **2507.22069v2**,
  https://arxiv.org/html/2507.22069v2: motivates accounting for generated candidates
  and failed work, rather than attributing different sampling budgets to memory.
  We measure incurred token counts and do not force both arms to spend equal work.

Author-reported findings are not experimental observations of this repository.
README's other suggested papers were not needed for this bounded stable-use test.
The original code, workload generator, protocol and tests are pinned in Git.
