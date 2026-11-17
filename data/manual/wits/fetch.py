import subprocess, sys, os, re
out=sys.argv[1]
reps={"USA":"840","EUN":"918","CHN":"156","GBR":"826","JPN":"392","RUS":"643","KOR":"410","VNM":"704","CAN":"124","CHE":"756","ARE":"784","AUS":"036","TUR":"792","MEX":"484","SAU":"682","PAN":"591","SGP":"702"}
for iso,code in reps.items():
    for dt in ["reported","aveestimated"]:
        for y in range(2025,2012,-1):
            f=f"{out}/{iso}_{dt}_{y}.xml"
            url=f"https://wits.worldbank.org/API/V1/SDMX/V21/datasource/TRN/reporter/{code}/partner/170/product/all/year/{y}/datatype/{dt}"
            r=subprocess.run(["curl","-s","-m","120","-o",f,"-w","%{http_code}",url],stdout=subprocess.PIPE,universal_newlines=True)
            if r.stdout=="200" and os.path.getsize(f)>2000:
                print(iso,dt,y,"OK",flush=True); break
            os.remove(f) if os.path.exists(f) else None
        else:
            print(iso,dt,"NONE",flush=True)
