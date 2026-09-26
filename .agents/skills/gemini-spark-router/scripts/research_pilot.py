"""Local draft-only adapter for X source briefs. No network calls or external writes."""
from __future__ import annotations
import argparse, hashlib, ipaddress, json, os, re, sys, tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl

MODES=('existing','google-deep-research-app','google-spark-app')
CHECKS=('claims_supported','sources_primary','rules_preserved','format_usable','no_private_data','no_external_writes')

def now():return datetime.now(timezone.utc)
def stamp():return now().isoformat()
def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def atomic(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.pilot-',dir=path.parent)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)
def digest(data):return hashlib.sha256(data).hexdigest()
def url(value):
    if not isinstance(value,str):raise ValueError('URL must be a string')
    u=urlsplit(value)
    if u.scheme!='https' or not u.hostname or u.username or u.password:raise ValueError('Only public HTTPS sources without credentials')
    host=u.hostname.lower()
    _=u.port  # urlsplit validates numeric/range constraints only when port is accessed.
    if host=='localhost' or '.' not in host or host.endswith(('.local','.internal','.localhost')):raise ValueError('Local source is not allowed')
    try:
        address=ipaddress.ip_address(host)
    except ValueError:
        if re.fullmatch(r'[0-9.]+',host):raise ValueError('Ambiguous numeric host is not allowed')
        ascii_host=host.encode('idna').decode('ascii')
        if not re.fullmatch(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}',ascii_host):raise ValueError('Invalid public hostname')
    else:
        if not address.is_global:raise ValueError('Non-public IP is not allowed')
    if any(re.search(r'token|secret|key|password|auth|session|signature',k,re.I) for k,v in parse_qsl(u.query)):raise ValueError('Credential-like URL query is not allowed')
    if re.search(r'(token|secret|key|password|auth|session|signature)[^=&#]*=',u.fragment,re.I):raise ValueError('Credential-like URL fragment is not allowed')
    return value
def validate_case(case):
    if not isinstance(case,dict) or type(case.get('version')) is not int or case['version']!=1 or case.get('task')!='x-source-brief':raise ValueError('Unsupported case schema')
    if case.get('public_only') is not True:raise ValueError('Only explicitly public input is accepted')
    if not isinstance(case.get('prompt'),str) or not 30<=len(case['prompt'].strip())<=12000:raise ValueError('Prompt must have 30..12000 meaningful characters')
    sources=case.get('sources')
    if not isinstance(sources,list) or not 1<=len(sources)<=12:raise ValueError('Select 1..12 public sources')
    for s in sources:url(s)
    if len(set(sources))!=len(sources):raise ValueError('Duplicate source URLs')
    if type(case.get('timeout_minutes')) is not int or not 1<=case['timeout_minutes']<=60:raise ValueError('Timeout must be 1..60 minutes')
    if type(case.get('max_words')) is not int or not 100<=case['max_words']<=2000:raise ValueError('max_words must be 100..2000')
    return case
def locked(job):
    class Lock:
        def __enter__(self):
            self.path=Path(job)/'.mutation.lock';self.file=self.path.open('a+b')
            if self.file.tell()==0:self.file.write(b'0');self.file.flush()
            self.file.seek(0)
            try:
                if os.name=='nt':
                    import msvcrt
                    msvcrt.locking(self.file.fileno(),msvcrt.LK_NBLCK,1)
                else:
                    import fcntl
                    fcntl.flock(self.file.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
            except OSError:
                self.file.close();raise ValueError('Another local process is updating this job; retry status after it finishes')
            return self
        def __exit__(self,*args):
            self.file.seek(0)
            if os.name=='nt':
                import msvcrt
                msvcrt.locking(self.file.fileno(),msvcrt.LK_UNLCK,1)
            else:
                import fcntl
                fcntl.flock(self.file.fileno(),fcntl.LOCK_UN)
            self.file.close()
    return Lock()
def state(job):return read(Path(job)/'state.json')
def save(job,s):s['updated_at']=stamp();atomic(Path(job)/'state.json',s);return s
def pending(s):
    if s['status'] in ('canceled','accepted','rejected'):raise ValueError('Terminal local job; no automatic retry')
    if now()>datetime.fromisoformat(s['deadline']):raise ValueError('Job expired; keep existing route, inspect provider before any new launch')
def prepare(case_file,base,mode='existing'):
    if mode not in MODES:raise ValueError('Unknown mode')
    case=validate_case(read(case_file));raw=json.dumps(case,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    job_id=digest(raw)[:24];job=Path(base)/(job_id+'-'+mode)
    job.mkdir(parents=True,exist_ok=True)
    with locked(job):
        if (job/'state.json').exists():
            s=state(job)
            if s['input_sha256']!=digest(raw):raise ValueError('Job ID collision')
            return s
        atomic(job/'input.json',case)
        (job/'prompt.md').write_text(case['prompt'],encoding='utf-8')
        s={'version':1,'id':job_id,'mode':mode,'job_dir':str(job.resolve()),'input_sha256':digest(raw),'status':'prepared','created_at':stamp(),'deadline':(now()+timedelta(minutes=case['timeout_minutes'])).isoformat(),'provider_url':None,'provider_task_id':None,'provider_launches':0,'max_provider_launches':1,'external_writes':False,'result_sha256':None,'network_used_by_adapter':False}
        return save(job,s)
def register(job,provider_url,task_id=None):
    u=urlsplit(url(provider_url))
    if u.hostname!='gemini.google.com' or u.query or u.fragment:raise ValueError('Use the actual Gemini task or conversation URL')
    with locked(job):
        s=state(job);pending(s)
        if s['mode']=='existing':raise ValueError('Existing mode does not register a Google run')
        if s['mode']=='google-deep-research-app' and (not re.fullmatch(r'/app/[0-9a-f]+',u.path) or task_id):raise ValueError('Use the actual Deep Research conversation URL')
        if s['mode']=='google-spark-app':
            if not isinstance(task_id,str) or not re.fullmatch(r'goal-c_[0-9a-f]+',task_id):raise ValueError('Spark needs an observed goal-c_ task ID')
            if u.path not in ('/spark/tasks','/spark/chat/'+task_id.removeprefix('goal-c_')):raise ValueError('Spark URL must match the observed task ID')
        if s['provider_url']:
            if s['provider_url']==provider_url and s.get('provider_task_id')==task_id:return s
            if s['mode']=='google-spark-app' and s.get('provider_task_id')==task_id and urlsplit(s['provider_url']).path=='/spark/tasks' and u.path=='/spark/chat/'+task_id.removeprefix('goal-c_'):
                s['provider_url']=provider_url
                return save(job,s)
            raise ValueError('A provider job is already registered; inspect it instead of relaunching')
        s.update(provider_url=provider_url,provider_task_id=task_id,provider_launches=1,status='awaiting_result',registered_at=stamp())
        return save(job,s)
def import_result(job,result_file):
    data=Path(result_file).read_bytes()
    if len(data)>2_000_000:raise ValueError('Result too large')
    body=data.decode('utf-8-sig');sha=digest(data)
    if len(body.strip())<200 or '\x00' in body:raise ValueError('Empty or damaged result')
    sources=set(re.findall(r'https://[^\s<>\]\)"\x27]+',body))
    if len(sources)<3:raise ValueError('At least 3 inspectable source URLs required; export citations')
    for source in sources:url(source.rstrip('.,;'))
    with locked(job):
        s=state(job)
        if s['result_sha256']==sha and s['status'] in ('review_required','accepted','rejected'):return s
        pending(s)
        if s['result_sha256']:raise ValueError('Different result already imported; do not overwrite the evidence')
        if s['mode']!='existing' and not s['provider_url']:raise ValueError('Register actual run before importing')
        case=read(Path(job)/'input.json');words=len(body.split())
        # Raw evidence is deliberately retained even if the provider ignores its word limit.
        atomic(Path(job)/'result.json',{'body':body,'sha256':sha,'source_urls':sorted(sources),'words':words,'over_word_limit':words>case['max_words'],'source_file':Path(result_file).name})
        s.update(result_sha256=sha,status='review_required',format_warning=words>case['max_words'],imported_at=stamp())
        return save(job,s)
def review(job,review_file):
    verdict=read(review_file)
    if not isinstance(verdict,dict) or verdict.get('verdict') not in ('accept','reject') or not isinstance(verdict.get('reason'),str) or not verdict['reason'].strip():raise ValueError('Review requires verdict and reason')
    if verdict['verdict']=='accept' and any(verdict.get(k) is not True for k in CHECKS):raise ValueError('Acceptance requires all explicit review checks')
    with locked(job):
        s=state(job)
        if s['status']!='review_required':raise ValueError('No result awaiting review')
        atomic(Path(job)/'review.json',verdict);s['status']='accepted' if verdict['verdict']=='accept' else 'rejected';return save(job,s)
def cancel(job):
    with locked(job):
        s=state(job)
        if s['status']=='canceled':return s
        if s['status'] in ('accepted','rejected'):raise ValueError('Review already final')
        s.update(status='canceled',remote_stop_required=bool(s['provider_url']))
        return save(job,s)
def inspect(job):
    s=state(job)
    s['expired']=now()>datetime.fromisoformat(s['deadline'])
    s['remote_cancellation_performed']=False
    s['resume_instruction']='Open saved provider_url; do not launch a duplicate. Restore access then import only as draft.' if s['provider_url'] else 'Use existing process, or explicitly select the app pilot.'
    return s
def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='cmd',required=True)
    p=sub.add_parser('prepare');p.add_argument('--case',required=True);p.add_argument('--out',required=True);p.add_argument('--mode',choices=MODES,default='existing')
    p=sub.add_parser('register');p.add_argument('--job',required=True);p.add_argument('--url',required=True);p.add_argument('--task-id')
    p=sub.add_parser('import');p.add_argument('--job',required=True);p.add_argument('--result',required=True)
    p=sub.add_parser('review');p.add_argument('--job',required=True);p.add_argument('--review-file',required=True)
    for name in ('status','cancel'):sub.add_parser(name).add_argument('--job',required=True)
    args=parser.parse_args()
    try:
        if args.cmd=='prepare':result=prepare(args.case,args.out,args.mode)
        elif args.cmd=='register':result=register(args.job,args.url,args.task_id)
        elif args.cmd=='import':result=import_result(args.job,args.result)
        elif args.cmd=='review':result=review(args.job,args.review_file)
        elif args.cmd=='cancel':result=cancel(args.job)
        else:result=inspect(args.job)
        print(json.dumps({'ok':True,'data':result},ensure_ascii=False,indent=2))
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError) as e:
        print(json.dumps({'ok':False,'error':str(e)},ensure_ascii=False));return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
