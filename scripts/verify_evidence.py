"""Offline audit; recompute hidden gold and scores from preserved inputs/outputs."""
import hashlib,json,pathlib
from workload import oracle
R=pathlib.Path(__file__).resolve().parents[1]
E=R/'evidence'
cases=json.loads((E/'evaluation-inputs.json').read_text())
records=json.loads((E/'evaluation-records.json').read_text())
assert [oracle(c) for c in cases]==json.loads((E/'evaluation-gold.json').read_text())
lookup={c['seed']:c for c in cases}
assert len(records)==32
assert len({(r['arm'],r['seed']) for r in records})==32
for r in records:
    result=r.get('execution',{}).get('results',[{}])[-1]
    assert r['success']==(result.get('output')==oracle(lookup[r['seed']]))
    if r['arm'] in ('ready','archive'):
        assert r['source_sha256']==hashlib.sha256((E/'acquired.py').read_bytes()).hexdigest()
print('Verified 32 paired-arm records and 8 independently recomputed gold outputs.')
