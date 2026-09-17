"""Runs inside a networkless Docker container; no oracle or project mount."""
import json, sys, time, traceback
payload=json.load(sys.stdin)
ns={}
try:
    exec(compile(payload['source'],'candidate.py','exec'),ns)
except BaseException:
    print(json.dumps({'compile_error':traceback.format_exc()}));sys.exit(0)
results=[]
for case in payload['cases']:
    calls=[]
    class API:
        def page(self, resource, cursor=None):
            if len(calls)>10000: raise RuntimeError('API call budget exceeded')
            if resource not in ('invoices','events'): raise ValueError(resource)
            idx=0 if cursor is None else int(cursor.split(':')[1])
            items=case['data'][resource]; size=case['page_size']
            end=min(idx+size,len(items))
            out={'items':json.loads(json.dumps(items[idx:end])), 'next_cursor':f'{resource}:{end}' if end<len(items) else None}
            calls.append({'resource':resource,'cursor':cursor,'items':len(out['items'])})
            return out
    start=time.perf_counter()
    try: result={'output':ns['solve'](API(),case['request'])}
    except BaseException: result={'error':traceback.format_exc()}
    result.update(seconds=time.perf_counter()-start,api_calls=calls)
    results.append(result)
print(json.dumps({'results':results}))
