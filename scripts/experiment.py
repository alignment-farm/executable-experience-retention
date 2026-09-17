"""Run with uv run --python 3.12 python scripts/experiment.py acquire|evaluate|summarize."""
import argparse, contextlib, fcntl, hashlib, io, json, os, pathlib, re, subprocess, time, urllib.request, zipfile
from workload import CONTRACT, dev_cases, fixture, oracle
ROOT=pathlib.Path(__file__).resolve().parents[1]
E=ROOT/'evidence'; E.mkdir(exist_ok=True)
MODEL='docker.io/ai/qwen3.8:27b-q4_K_M'
URL='https://mac-studio-7hr7.taile71f88.ts.net/engines/v1/chat/completions'
IMAGE=(E/'container-image.txt').read_text().strip() if (E/'container-image.txt').exists() else 'python:3.12-alpine'

def save(path,value):
    path=pathlib.Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')

def call(name,messages,max_tokens=4096):
    directory=E/'calls'/name; directory.mkdir(parents=True,exist_ok=False)
    body=dict(model=MODEL,messages=messages,temperature=0,max_tokens=max_tokens,stream=False)
    save(directory/'request.json',body)
    with open('/tmp/executable-experience-model.lock','a+') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        lock.seek(0);lock.truncate();lock.write(f'{os.getpid()} {ROOT} {name}\n');lock.flush()
        for attempt in range(2):
            start=time.perf_counter()
            try:
                request=urllib.request.Request(URL,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(request,timeout=180) as response: result=json.load(response)
                save(directory/f'response-{attempt}.json',result)
                save(directory/f'measurement-{attempt}.json',{'wall_seconds':time.perf_counter()-start,'success':True})
                print(name,result.get('usage'),flush=True)
                return result['choices'][0]['message']['content']
            except Exception as exc:
                save(directory/f'measurement-{attempt}.json',{'wall_seconds':time.perf_counter()-start,'success':False,'error':repr(exc)})
                if attempt: raise
                time.sleep(3)

def extract(content):
    blocks=re.findall(r'```(?:python)?\s*\n(.*?)```',content,re.S)
    return max(blocks,key=len) if blocks else content

def execute(source,cases):
    start=time.perf_counter()
    cmd=['docker','run','--rm','-i','--network=none','--read-only','--memory=256m','--cpus=1',
         '--pids-limit=32','--cap-drop=ALL','--security-opt=no-new-privileges',
         IMAGE,'python','-I','-c',(ROOT/'scripts/worker.py').read_text()]
    try:
        p=subprocess.run(cmd,input=json.dumps({'source':source,'cases':cases}),text=True,capture_output=True,timeout=10)
        result=json.loads(p.stdout)
        result['stderr']=p.stderr;result['returncode']=p.returncode
    except Exception as exc: result={'harness_error':repr(exc)}
    result['container_wall_seconds']=time.perf_counter()-start
    return result

def check(batch,cases):
    if 'results' not in batch: return [batch]
    failures=[]
    for i,(out,case) in enumerate(zip(batch['results'],cases)):
        expected=oracle(case)
        if out.get('output')!=expected: failures.append({'case_index':i,'actual':out,'expected':expected})
    if len(batch['results'])!=len(cases):failures.append({'error':'wrong result count'})
    return failures

def examples():
    return [{'input':c,'expected':oracle(c)} for c in dev_cases()]

SYSTEM='You are implementing a reusable Python routine. Return only Python source defining solve(api, request). No external packages. Do not hardcode examples. Be concise and correct.'

def build(name, lessons=None, current=None, initial=None):
    prompt=CONTRACT+'\nDevelopment checks available to you:\n'+json.dumps(examples())
    if lessons is not None: prompt+='\nRetained procedural lessons (source not retained):\n'+lessons
    if current is not None: prompt+='\nCurrent request and page interface parameters:\n'+json.dumps({'request':current['request'],'page_size':current['page_size']})
    if initial is not None: prompt+='\nExisting implementation available to repair:\n'+initial
    messages=[{'role':'system','content':SYSTEM},{'role':'user','content':prompt}]
    attempts=[]
    for i in range(3):
        content=call(f'{name}-{i}',messages)
        source=extract(content)
        path=E/'candidates'/f'{name}-{i}.py';path.parent.mkdir(exist_ok=True);path.write_text(source)
        batch=execute(source,dev_cases()); failures=check(batch,dev_cases())
        save(E/'checks'/f'{name}-{i}.json',batch)
        attempt={'source_path':str(path.relative_to(ROOT)),'check_path':f'evidence/checks/{name}-{i}.json','failures':failures}
        attempts.append(attempt)
        save(E/'builds'/f'{name}.json',attempts)
        if not failures: return source
        messages.extend([{'role':'assistant','content':content},{'role':'user','content':'Development check failed. Repair using this feedback:\n'+json.dumps(failures)}])
    raise RuntimeError(f'{name}: acquisition/reconstruction failed after 3 candidates')

def acquire():
    save(E/'development.json',examples())
    source=build('acquisition')
    (E/'acquired.py').write_text(source)
    lessons=call('lesson-construction',[{'role':'system','content':'Write concise procedural lessons for future implementation from this successful experience. Preserve all essential decisions and edge cases. Plain prose only, no code, no pseudocode. The future model also gets the full contract and same development examples.'},
              {'role':'user','content':CONTRACT+'\nAcquired source:\n'+source+'\nObserved successful development cases:\n'+json.dumps(examples())}],max_tokens=2048)
    (E/'lessons.md').write_text(lessons)
    with zipfile.ZipFile(E/'acquisition-archive.zip','w',zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('manifest.json',json.dumps({'implementation':'acquisition/accepted.py','contract_version':'initial'}))
        archive.writestr('acquisition/accepted.py',source)
        archive.writestr('acquisition/development-checks.json',json.dumps(examples()))
    print('ACQUIRED',flush=True)

def evaluate():
    sources={}; all_records=[]
    lessons=(E/'lessons.md').read_text()
    cases=[fixture(seed,n) for seed,n in zip(range(8101,8109),[9,17,31,52,9,17,0,31])]
    for index,case in enumerate(cases):
        case['request']['customers']=[['alfa'],['alfa','beta'],['alfa','beta','gamma']][index%3]
    cases[-1]['request']['customers']=[]
    save(E/'evaluation-inputs.json',cases)
    save(E/'evaluation-gold.json',[oracle(c) for c in cases])
    # Rotated arm order; all model calls sequential. No held-out feedback enters build().
    for index,case in enumerate(cases):
        arms=['ready','lessons','archive','cache']; arms=arms[index%4:]+arms[:index%4]
        for arm in arms:
            start=time.perf_counter(); load_start=time.perf_counter(); build_name=None
            if arm=='ready': source=(E/'acquired.py').read_text()
            elif arm=='archive':
                with zipfile.ZipFile(E/'acquisition-archive.zip') as archive:
                    manifest=json.loads(archive.read('manifest.json'))
                    source=archive.read(manifest['implementation']).decode()
            elif arm=='cache' and arm in sources: source=sources[arm]
            else:
                build_name=f'{arm}-{case["seed"]}'
                try: source=build(build_name,lessons,current=case)
                except RuntimeError as exc:
                    all_records.append({'arm':arm,'seed':case['seed'],'success':False,'error':str(exc),'wall_seconds':time.perf_counter()-start,'build_name':build_name})
                    save(E/'evaluation-records.json',all_records);continue
            load_seconds=time.perf_counter()-load_start
            batch=execute(source,dev_cases()+[case])
            dev_failures=check({'results':batch.get('results',[])[:5]},dev_cases()) if 'results' in batch else [batch]
            out=batch.get('results',[{}])[-1]
            initial_batch=batch
            # Runtime or development failure can trigger repair; hidden quality failure cannot.
            repair_name=None
            if dev_failures or 'error' in out or 'results' not in batch:
                repair_name=f'{arm}-{case["seed"]}-repair'
                # Provide actual runtime observations without hidden oracle answers.
                repair_lessons=lessons+'\nRuntime feedback: '+json.dumps(batch)+'\nCurrent observations: '+json.dumps(case)
                try:
                    source=build(repair_name,repair_lessons,current=case,initial=source)
                    batch=execute(source,dev_cases()+[case]);out=batch.get('results',[{}])[-1]
                except RuntimeError: pass
            if arm=='cache' and 'output' in out and not dev_failures: sources[arm]=source
            record={'arm':arm,'seed':case['seed'],'success':out.get('output')==oracle(case),
                    'wall_seconds':time.perf_counter()-start,'load_or_build_seconds':load_seconds,
                    'build_name':build_name,'repair_name':repair_name,'source_sha256':hashlib.sha256(source.encode()).hexdigest(),
                    'source_bytes':len(source.encode()),'execution':batch,'initial_execution':initial_batch if repair_name else None}
            all_records.append(record);save(E/'evaluation-records.json',all_records)
            print('EVAL',case['seed'],arm,record['success'],round(record['wall_seconds'],3),flush=True)
    summarize()

def summarize():
    records=json.loads((E/'evaluation-records.json').read_text())
    calls=[]
    for path in sorted((E/'calls').glob('*')):
        usage={};seconds=0
        for p in path.glob('response-*.json'):
            response=json.loads(p.read_text());usage=response.get('usage',{})
        for p in path.glob('measurement-*.json'): seconds+=json.loads(p.read_text())['wall_seconds']
        calls.append({'name':path.name,'wall_seconds':seconds,**usage})
    def costs(selected):
        return {'model_calls':len(selected),'prompt_tokens':sum(c.get('prompt_tokens',0) for c in selected),
                'completion_tokens':sum(c.get('completion_tokens',0) for c in selected),
                'cached_tokens':sum(c.get('prompt_tokens_details',{}).get('cached_tokens',0) for c in selected),
                'model_wall_seconds':sum(c['wall_seconds'] for c in selected)}
    summary={'setup':costs([c for c in calls if c['name'].startswith(('acquisition-','lesson-construction'))]),'arms':{},'calls':calls}
    for arm in ['ready','lessons','archive','cache']:
        rs=[r for r in records if r['arm']==arm]
        cs=[c for c in calls if c['name'].startswith(arm+'-')]
        summary['arms'][arm]={**costs(cs),'requests':len(rs),'successes':sum(r['success'] for r in rs),
            'wall_seconds':sum(r['wall_seconds'] for r in rs),
            'execution_api_calls':sum(len(x['api_calls']) for r in rs for x in r.get('execution',{}).get('results',[])),
            'current_api_calls':sum(len(r.get('execution',{}).get('results',[{'api_calls':[]}])[-1]['api_calls']) for r in rs)}
    save(ROOT/'results/summary.json',summary)
    print(json.dumps(summary['arms'],indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['acquire','evaluate','summarize']);args=parser.parse_args()
    globals()[args.mode]()
