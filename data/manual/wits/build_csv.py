import re, csv, sys
raw, outdir = sys.argv[1], sys.argv[2]
BASE="https://wits.worldbank.org/API/V1/SDMX/V21/datasource/TRN/reporter/{code}/partner/{par}/product/all/year/{y}/datatype/{dt}"
EU=["AUT","BEL","CZE","DEU","DNK","ESP","FRA","ITA","NLD","POL","PRT","ROU","SVK","SWE"]
# reporter_iso: (file, wits_code, partner, year, datatype, tariff_type, note)
sel={
 "USA":("USA_reported_2021","840","170",2021,"reported","PREF","US-Colombia TPA."),
 "EUN":("EUN_reported_2021","918","170",2021,"reported","PREF","EU-Colombia/Peru/Ecuador Trade Agreement; EU reported as a single customs territory (WITS reporter 918)."),
 "GBR":("GBR_reported_2021","826","170",2021,"reported","PREF","UK-Andean Trade Agreement."),
 "KOR":("KOR_reported_2021","410","170",2021,"reported","PREF","Korea-Colombia FTA."),
 "CAN":("CAN_reported_2021","124","170",2021,"reported","PREF","Canada-Colombia FTA."),
 "CHE":("CHE_reported_2021","756","170",2021,"reported","PREF","EFTA-Colombia FTA."),
 "MEX":("MEX_reported_2018","484","170",2018,"reported","PREF_PARTIAL","MANUAL CHECK: latest WITS line data (2018) shows preference on only ~30% of national lines, MFN on the rest; WITS AVE-estimated 2017 file reports 0.0. Verify current Colombia-Mexico schedule (Pacific Alliance Additional Protocol) before using."),
 "PAN":("PAN_mfn000_2023","591","000",2023,"reported","MFN","No Colombia-Panama FTA in force. MANUAL CHECK: WITS 2013 shows partial preference for COL (simple avg 7.79) under an older partial-scope agreement; no later preferential data."),
 "CHN":("CHN_mfn000_2023","156","000",2023,"reported","MFN","No preferential agreement with Colombia."),
 "JPN":("JPN_ave000_2023","392","000",2023,"aveestimated","MFN_AVE","No EPA in force. Ad-valorem equivalents used because 25 of 99 lines are specific/compound duties (reported ad-valorem-only average would be 16.32). Japanese GSP not considered. Leather footwear is under tariff-rate quota."),
 "RUS":("RUS_ave000_2021","643","000",2021,"aveestimated","MFN_AVE","EAEU common tariff; 71 of 79 lines specific/compound, so ad-valorem equivalents used (ad-valorem-only average would be a misleading 0.0). Latest year available in WITS."),
 "VNM":("VNM_mfn000_2023","704","000",2023,"reported","MFN","No preferential agreement with Colombia."),
 "ARE":("ARE_mfn000_2023","784","000",2023,"reported","MFN","GCC common external tariff; no agreement with Colombia."),
 "AUS":("AUS_mfn000_2023","036","000",2023,"reported","MFN","No preferential agreement with Colombia."),
 "TUR":("TUR_mfn000_2023","792","000",2023,"reported","MFN","Colombia-Turkey FTA signed but not in force. Turkey applies high duties (incl. additional duties) on footwear from non-FTA origins."),
 "SAU":("SAU_mfn000_2023","682","000",2023,"reported","MFN","No agreement with Colombia."),
 "SGP":("SGP_mfn000_2023","702","000",2023,"reported","MFN","Singapore applies zero duties on footwear."),
}
rx=re.compile(r'<Series [^>]*PRODUCTCODE="(64\d{4})"[^>]*>\s*<Obs ([^/]*)/>')
summary={}; detail=[]
for rep,(f,code,par,y,dt,tt,note) in sel.items():
    txt=open(f"{raw}/{f}.xml",encoding="utf-8").read()
    vals=[]
    for hs6,attrs in rx.findall(txt):
        a=dict(re.findall(r'(\w+)="([^"]*)"',attrs))
        v=float(a["OBS_VALUE"]); vals.append(v)
        detail.append([rep,hs6,y,dt,a.get("TARIFFTYPE"),round(v,4),a.get("MIN_RATE"),a.get("MAX_RATE"),a.get("TOTALNOOFLINES"),a.get("NBR_PREF_LINES"),a.get("NBR_MFN_LINES"),a.get("NBR_NA_LINES"),a.get("NOMENCODE")])
    url=BASE.format(code=code,par=par,y=y,dt=dt)
    summary[rep]=(round(sum(vals)/len(vals),2),tt,y,code,"COL" if par=="170" else "WORLD(MFN)",dt,len(vals),note,url)
rows=[]
for iso in ["ARE","AUS","AUT","BEL","CAN","CHE","CHN","CZE","DEU","DNK","ESP","FRA","GBR","ITA","JPN","KOR","MEX","NLD","PAN","POL","PRT","ROU","RUS","SAU","SGP","SVK","SWE","TUR","USA","VNM"]:
    rep="EUN" if iso in EU else iso
    avg,tt,y,code,par,dt,n,note,url=summary[rep]
    rows.append([iso,f"{avg:.2f}",f"WITS-TRAINS API, accessed 2026-11-17: {url}",tt,y,rep,par,dt,n,note])
with open(f"{outdir}/legacy_preferential_tariffs.csv","w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["iso3","tariff_pct","source","tariff_type","year","wits_reporter","partner","datatype","n_hs6","notes"]); w.writerows(rows)
with open(f"{outdir}/wits/legacy_hs64_hs6_detail.csv","w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["reporter","hs6","year","datatype","tariff_type","simple_avg_pct","min_rate","max_rate","n_lines","n_pref_lines","n_mfn_lines","n_na_lines","hs_nomenclature"]); w.writerows(detail)
for r in rows: print(r[0],r[1],r[3],r[4])
