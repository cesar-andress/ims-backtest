import subprocess, sys, os
out=sys.argv[1]
reps={"CHN":"156","JPN":"392","RUS":"643","VNM":"704","ARE":"784","AUS":"036","TUR":"792","SAU":"682","SGP":"702","PAN":"591"}
for iso,code in reps.items():
    for y in range(2025,2012,-1):
        f=f"{out}/{iso}_mfn000_{y}.xml"
        url=f"https://wits.worldbank.org/API/V1/SDMX/V21/datasource/TRN/reporter/{code}/partner/000/product/all/year/{y}/datatype/reported"
        r=subprocess.run(["curl","-s","-m","120","-o",f,"-w","%{http_code}",url],stdout=subprocess.PIPE,universal_newlines=True)
        if r.stdout=="200" and os.path.getsize(f)>2000: print(iso,y,"OK",flush=True); break
        if os.path.exists(f): os.remove(f)
    else: print(iso,"NONE",flush=True)
