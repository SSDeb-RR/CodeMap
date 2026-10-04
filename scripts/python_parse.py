#!/usr/bin/env python3
import ast,hashlib,json,os,sys
from pathlib import Path
X={".git",".venv","venv","node_modules","__pycache__","build","dist",".tox",".mypy_cache",".pytest_cache"};MAX=1024*1024
def rel(p,r):return p.relative_to(r).as_posix()
def mod(p):
 b=p[:-3].split("/");b.pop() if b[-1]=="__init__" else None;return ".".join(b)
def pkg(p):m=mod(p);return m if p.endswith("/__init__.py") else m.rpartition(".")[0]
def resolve(n,mods):
 b=n.split(".") if n else []
 while b:
  k=".".join(b)
  if k in mods:return mods[k]
  b.pop()
def rname(src,level,module):
 if level==0:return module or ""
 b=pkg(src).split(".") if pkg(src) else []
 if level-1>len(b):return None
 o=b[:len(b)-(level-1)]+(module.split(".") if module else []);return ".".join(filter(None,o))
root=Path(sys.argv[1]).resolve();paths=[];excluded=[]
for cur,dirs,names in os.walk(root):
 base=Path(cur);gone=sorted(d for d in dirs if d in X or d.startswith("."));excluded += [{"path":rel(base/d,root),"reason":"generated, dependency, or hidden directory"} for d in gone];dirs[:]=sorted(d for d in dirs if d not in gone);paths += [base/n for n in sorted(names) if n.endswith(".py")]
mods={mod(rel(p,root)):rel(p,root) for p in paths if mod(rel(p,root))};roots={m.split(".")[0] for m in mods};stdlib=getattr(sys,"stdlib_module_names",set());files=[];skipped=[];edges=[];unresolved=[];ext={"package":0,"builtin":0,"outside-root":0};seen=internal=0
for p in paths:
 rp=rel(p,root)
 try:raw=p.read_bytes();text=raw.decode()
 except (OSError,UnicodeDecodeError) as e:skipped.append({"path":rp,"reason":"unreadable","detail":str(e)});continue
 if len(raw)>MAX:skipped.append({"path":rp,"reason":"too-large","detail":f"{len(raw)} bytes exceeds {MAX}"});continue
 try:tree=ast.parse(text,filename=rp)
 except SyntaxError as e:skipped.append({"path":rp,"reason":"syntax-error","detail":str(e)});continue
 exports=[n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))];files.append({"path":rp,"language":"python","module":str(Path(rp).parent).replace("\\","/") or ".","lines":len(text.splitlines()),"bytes":len(raw),"hash":hashlib.sha256(raw).hexdigest(),"fanIn":0,"fanOut":0,"reachedBy":"Python package initializer" if rp.endswith("__init__.py") else None,"role":None,"exports":sorted(set(exports))});req=[]
 for n in ast.walk(tree):
  if isinstance(n,ast.Import):req += [(a.name,n.lineno,None) for a in n.names]
  elif isinstance(n,ast.ImportFrom):req.append((rname(rp,n.level,n.module),n.lineno,[a.name for a in n.names if a.name!="*"]))
 for requested,line,members in req:
  seen+=1;requested=requested or "";names=([f"{requested}.{m}" for m in members] if members else [])+[requested];target=next((resolve(n,mods) for n in names if resolve(n,mods)),None)
  if target and target!=rp:internal+=1;edges.append({"source":rp,"target":target,"kind":"import","typeOnly":False,"specifier":requested or ".","line":line});continue
  top=requested.split(".")[0]
  if top in stdlib:ext["builtin"]+=1
  elif top and top not in roots:ext["package"]+=1
  else:unresolved.append({"from":rp,"language":"python","specifier":requested or ".","kind":"import","line":line,"reason":"file-not-found","detail":"no repository-local Python module matched this import"})
edges=sorted({(e["source"],e["target"],e["kind"]):e for e in edges}.values(),key=lambda e:(e["source"],e["target"]));inc={};out={}
for e in edges:out.setdefault(e["source"],set()).add(e["target"]);inc.setdefault(e["target"],set()).add(e["source"])
for f in files:f["fanIn"]=len(inc.get(f["path"],set()));f["fanOut"]=len(out.get(f["path"],set()))
json.dump({"files":sorted(files,key=lambda f:f["path"]),"edges":edges,"skipped":sorted(skipped,key=lambda f:f["path"]),"excludedDirectories":sorted(excluded,key=lambda d:d["path"]),"imports":{"seen":seen,"internal":internal,"external":sum(ext.values()),"excluded":0,"unresolved":len(unresolved),"externalKinds":ext,"unresolvedItems":sorted(unresolved,key=lambda u:(u["from"],u["line"]))}},sys.stdout,sort_keys=True)
