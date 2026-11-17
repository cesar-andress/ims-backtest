import re, glob, os, sys, collections
d=sys.argv[1]
rx=re.compile(r'<Series [^>]*PRODUCTCODE="(64\d{4})"[^>]*>\s*<Obs ([^/]*)/>')
for f in sorted(glob.glob(d+"/*.xml")):
    txt=open(f,encoding="utf-8").read()
    vals=[];types=collections.Counter();na=0;lines=0;mx=0
    for code,attrs in rx.findall(txt):
        a=dict(re.findall(r'(\w+)="([^"]*)"',attrs))
        types[a.get("TARIFFTYPE")]+=1
        lines+=int(a.get("TOTALNOOFLINES",0)); na+=int(a.get("NBR_NA_LINES",0))
        if a.get("OBS_VALUE") not in (None,""):
            v=float(a["OBS_VALUE"]); vals.append(v); mx=max(mx,float(a.get("MAX_RATE",v) or v))
    nom=re.search(r'NOMENCODE="(\w+)"',txt)
    avg=sum(vals)/len(vals) if vals else None
    print(f"{os.path.basename(f):28s} hs6={len(vals):3d} avg={avg if avg is None else round(avg,2)!s:6} max={mx:5.1f} types={dict(types)} lines={lines} NA_lines={na} nom={nom.group(1) if nom else '-'}")
