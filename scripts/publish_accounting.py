"""Derive auditable cost tables; does not invoke a model."""
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]; E=R/'evidence'
summary=json.loads((R/'results/summary.json').read_text())
records=json.loads((E/'evaluation-records.json').read_text())
lines=['| Retention policy | Exact success | Model calls | Prompt tokens | Completion tokens | Reported cached tokens | API calls, all checks + current | Total wall seconds |',
       '|---|---:|---:|---:|---:|---:|---:|---:|']
for arm,a in summary['arms'].items():
    api=a['execution_api_calls']+a['candidate_check_api_calls']
    lines.append(f'| {arm} | {a["successes"]}/{a["requests"]} | {a["model_calls"]} | {a["prompt_tokens"]:,} | {a["completion_tokens"]:,} | {a["cached_tokens"]:,} | {api:,} | {a["wall_seconds"]:.3f} |')
lines.extend(['','All evaluation attempts are included. Setup is separate. Cached tokens are a subset of prompt tokens, not an additional token charge. Wall seconds include model calls and local orchestration; hardware exclusivity was not established.','',
              '| Seed | ready | lessons | archive | cache |','|---|---:|---:|---:|---:|'])
for seed in range(8101,8109):
    vals=[]
    for arm in ['ready','lessons','archive','cache']:
        r=next(r for r in records if r['seed']==seed and r['arm']==arm)
        vals.append(('pass' if r['success'] else 'FAIL')+f' ({r["wall_seconds"]:.3f}s)')
    lines.append('| '+str(seed)+' | '+' | '.join(vals)+' |')
(R/'results/tables.md').write_text('\n'.join(lines)+'\n')
# Full instrumented setup by named call; timed-out calls have unknown tokens.
setup=[]
for c in summary['calls']:
    if not c['name'].startswith(('acquisition','lesson-')):continue
    setup.append(c)
(R/'results/setup-accounting.json').write_text(json.dumps(setup,indent=2)+'\n')
print('\n'.join(lines))

# Shared acquisition plus representation-specific setup for one selected deployment.
cs={c['name']:c for c in summary['calls']}
a=cs['acquisition-compact-0']
lesson=[cs['lesson-construction'],cs['lesson-repair']]
shared_wall=a['wall_seconds']+summary['setup']['candidate_check_wall_seconds']
selected={}
for arm,v in summary['arms'].items():
    uses_lessons=arm in ['lessons','cache']
    selected[arm]={
        'known_prompt_tokens':a['prompt_tokens']+v['prompt_tokens']+(sum(c['prompt_tokens'] for c in lesson) if uses_lessons else 0),
        'known_completion_tokens':a['completion_tokens']+v['completion_tokens']+(sum(c['completion_tokens'] for c in lesson) if uses_lessons else 0),
        'instrumented_wall_seconds':shared_wall+v['wall_seconds']+(sum(c['wall_seconds'] for c in lesson) if uses_lessons else 0),
        'api_calls':55+v['candidate_check_api_calls']+v['execution_api_calls']}
(R/'results/selected-deployment.json').write_text(json.dumps(selected,indent=2)+'\n')
