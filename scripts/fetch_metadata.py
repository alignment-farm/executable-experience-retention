"""One serialized API request, shared local lock, cached response, Retry-After honored."""
import fcntl, pathlib, time, urllib.request, urllib.error, email.utils, datetime
root=pathlib.Path(__file__).resolve().parents[1]
path=root/'sources/arxiv-metadata.xml'
if path.exists(): raise SystemExit('Using cached response')
with open('/tmp/alignment-farm-arxiv-api.lock','a+') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX)
    lock.seek(0)
    try: last=float(lock.read())
    except ValueError: last=0
    time.sleep(max(0,3-(time.time()-last)))
    url='https://export.arxiv.org/api/query?id_list=2603.00718v2,2507.22069v2'
    req=urllib.request.Request(url,headers={'User-Agent':'ExecutableExperienceRetentionStudy/0.1 (local methods verification; serialized cached client)'})
    try:
        with urllib.request.urlopen(req,timeout=60) as response: path.write_bytes(response.read())
    except urllib.error.HTTPError as exc:
        (root/'sources/arxiv-metadata-error.txt').write_text(str(exc)+'\n'+str(exc.headers))
        retry=exc.headers.get('Retry-After')
        if retry:
            try: delay=float(retry)
            except ValueError: delay=max(0,email.utils.parsedate_to_datetime(retry).timestamp()-time.time())
            last=time.time()+delay
    finally:
        lock.seek(0);lock.truncate();lock.write(str(max(last,time.time())))
