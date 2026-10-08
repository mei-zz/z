import concurrent.futures, json, pathlib, urllib.request, urllib.parse, time
dest=pathlib.Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main\HYPERGRAPH_RESEARCH\HSPE_V17_2\novelty_evidence')
dest.mkdir(parents=True,exist_ok=True)
dois=['10.3390/e27101046','10.1016/j.patcog.2024.110292','10.1007/s10115-024-02255-8','10.3390/electronics12234842','10.1007/s40747-025-02118-x','10.1038/s41598-026-45116-w','10.1007/s00530-024-01324-w','10.1145/3690624.3709274']
def fetch(doi):
 url='https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='')
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Focused academic bibliography verification/1.0'})
  with urllib.request.urlopen(req,timeout=20) as r:data=json.loads(r.read().decode())['message']
  return {'doi':doi,'state':'VERIFIED','url':url,'title':data.get('title'),'authors':data.get('author'),'published':data.get('published'),'container':data.get('container-title'),'link':data.get('link')}
 except Exception as e:return {'doi':doi,'state':'SOURCE_UNAVAILABLE','error':str(e),'url':url}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(fetch,dois))
(dest/'crossref_metadata.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf8')
for r in results:print(r['doi'],r['state'],str(r.get('title','')))
