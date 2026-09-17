"""Re-execute all preserved implementations on their recorded evaluation inputs."""
import json,hashlib
from experiment import E, execute, check
cases=json.loads((E/'evaluation-inputs.json').read_text())
records=json.loads((E/'evaluation-records.json').read_text())
sources={hashlib.sha256(p.read_bytes()).hexdigest():p for p in (E/'candidates').glob('*.py')}
sources.update({hashlib.sha256((E/'acquired.py').read_bytes()).hexdigest():E/'acquired.py'})
for record in records:
    source=sources[record['source_sha256']].read_text()
    case=next(c for c in cases if c['seed']==record['seed'])
    failures=check(execute(source,[case]),[case])
    assert bool(not failures)==record['success'],(record['arm'],record['seed'],failures)
print('Replayed all 32 observed outcomes in fresh containers.')
