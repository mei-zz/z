from pathlib import Path
import html,xml.etree.ElementTree as ET
O=Path(r'E:\我的资料库\Documents\Downloads\DCDLP-main\PAPER_PREP\R_HSPE_DSR_MANUSCRIPT_V2'); F=O/'figures'
boxes=[
('input',35,350,195,170,['Candidate pair (u,v)','Target-masked','training-visible graph'],'#EDF2F7','#64748B'),
('features',275,330,230,205,['Fixed structural','feature extraction','R context · GRAPH · PBD','and router state c_uv'],'#F1EBFF','#8B72C7'),
('rexpert',580,95,220,115,['R-HSPE expert','75 parameters','Δ_R'],'#FCE9E3','#D7785B'),
('gexpert',580,300,220,115,['GRAPH expert','75 parameters','Δ_G'],'#FCE9E3','#D7785B'),
('pexpert',580,505,220,115,['PBD expert','75 parameters','Δ_P'],'#FCE9E3','#D7785B'),
('state',275,685,230,145,['Symmetric state c_uv','R tokens/support','P3/P4 path counts','endpoint degree sum/gap'],'#F1EBFF','#8B72C7'),
('router',580,690,270,135,['Learned router','MLP 6→8→3 · 83 parameters','softmax: α_R, α_G, α_P'],'#FCE9E3','#D7785B'),
('mix',910,300,220,230,['Soft weighted residual','α_R Δ_R','+ α_G Δ_G','+ α_P Δ_P'],'#FFF4E5','#D89A36'),
('host',1190,130,180,130,['Existing NCNC','host score','(not routed)'],'#E5EFFB','#5A83B7'),
('sum',1265,385,72,72,['+'],'#F8FAFC','#64748B'),
('final',1410,355,160,130,['Final link','score'],'#E6F5E8','#4F9B5C')]
root=ET.Element('mxfile',{'host':'app.diagrams.net','modified':'2026-10-07T00:00:00.000Z','agent':'Codex','version':'24.7.17'});dg=ET.SubElement(root,'diagram',{'id':'dsr-figure-5','name':'Figure 5'});m=ET.SubElement(dg,'mxGraphModel',{'dx':'1600','dy':'900','grid':'1','gridSize':'10','guides':'1','tooltips':'1','connect':'1','arrows':'1','fold':'1','page':'1','pageScale':'1','pageWidth':'1600','pageHeight':'900','math':'1','shadow':'0'});cells=ET.SubElement(m,'root');ET.SubElement(cells,'mxCell',{'id':'0'});ET.SubElement(cells,'mxCell',{'id':'1','parent':'0'})
for ident,x,y,w,h,lines,fill,stroke in boxes:
 value='<div style="text-align:center">'+'<br>'.join(html.escape(z) for z in lines)+'</div>';style=f'rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};strokeWidth=2;fontSize=16;fontStyle=1;'
 c=ET.SubElement(cells,'mxCell',{'id':ident,'value':value,'style':style,'vertex':'1','parent':'1'});ET.SubElement(c,'mxGeometry',{'x':str(x),'y':str(y),'width':str(w),'height':str(h),'as':'geometry'})
edges=[('input','features'),('features','rexpert'),('features','gexpert'),('features','pexpert'),('features','state'),('state','router'),('rexpert','mix'),('gexpert','mix'),('pexpert','mix'),('router','mix'),('mix','sum'),('host','sum'),('sum','final')]
for i,(a,b) in enumerate(edges):
 e=ET.SubElement(cells,'mxCell',{'id':f'e{i}','value':'','style':'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;strokeColor=#64748B;strokeWidth=2;','edge':'1','parent':'1','source':a,'target':b});ET.SubElement(e,'mxGeometry',{'relative':'1','as':'geometry'})
ET.ElementTree(root).write(F/'figure5.drawio',encoding='utf-8',xml_declaration=True)
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900"><defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12z" fill="#64748B"/></marker><style>text{font-family:Arial,Helvetica,sans-serif;fill:#172033}.ttl{font-size:19px;font-weight:700}.body{font-size:17px}.small{font-size:14px}.edge{fill:none;stroke:#64748B;stroke-width:2.5;marker-end:url(#arrow)}</style></defs><rect width="1600" height="900" fill="#fff"/>'''
paths=[[(230,435),(255,435),(275,435)],[(505,370),(545,370),(545,152),(580,152)],[(505,430),(580,357)],[(505,475),(545,475),(545,562),(580,562)],[(390,535),(390,685)],[(505,755),(545,755),(545,660),(715,660),(715,690)],[(800,152),(860,152),(860,350),(910,350)],[(800,357),(910,415)],[(800,562),(860,562),(860,480),(910,480)],[(850,757),(875,757),(875,550),(970,550),(970,530)],[(1100,415),(1265,421)],[(1280,260),(1280,385)],[(1337,421),(1410,420)]]
for pts in paths: svg+='<polyline class="edge" points="'+' '.join(f'{x},{y}' for x,y in pts)+'"/>'
def box(x,y,w,h,fill,stroke,rx=15): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2.2"/>'
def txt(x,y,lines,cls='body',step=24):
 start=y-(len(lines)-1)*step/2;out=f'<text x="{x}" y="{start}" text-anchor="middle" class="{cls}">'
 for i,line in enumerate(lines): out+=f'<tspan x="{x}" dy="{0 if i==0 else step}">{html.escape(line)}</tspan>'
 return out+'</text>'
for ident,x,y,w,h,lines,fill,stroke in boxes:
 svg+=box(x,y,w,h,fill,stroke,36 if ident=='sum' else 15)
 cls='ttl' if ident in ('input','mix','host','final','sum') else ('small' if ident in ('router','state') else 'body')
 svg+=txt(x+w/2,y+h/2,lines,cls,22 if cls=='small' else 25)
svg+=box(910,560,220,58,'#FFFFFF','#CBD5E1',12)+txt(1020,589,['α_R + α_G + α_P = 1','Soft mixture · no discrete choice'],'small',20)
svg+='</svg>'; (F/'figure5.svg').write_text(svg,encoding='utf-8')
ET.parse(F/'figure5.drawio');ET.parse(F/'figure5.svg')
(F/'figure5_visual_spec.md').write_text('''# Figure 5 visual specification\n\nCandidate and target-masked training-visible graph feed fixed R-HSPE, projected GRAPH and PBD feature construction. Three learned 75-parameter residual experts feed a soft weighted residual sum. A separate six-value symmetric state drives an 83-parameter 6→8→3 softmax router; the weights sum to one. The weighted residual and unchanged NCNC host score meet at an explicit addition node to form the final link score. No discrete expert selection or causal attribution is implied. Lavender indicates feature/state construction, coral learned modules, slate blue the existing host, green the output.\n''',encoding='utf-8')
(F/'figure5_review_notes.md').write_text('''# Figure 5 review notes\n\nThe revised diagram shows separate paths from the fixed feature view to the residual experts and router state to the gate. All three alpha values feed a continuous weighted residual. The residual enters an explicit sum with the separate NCNC score, preserving the fact that the host is not routed. Editable source: `figure5.drawio`; SVG is the render source for PDF/PNG.\n''',encoding='utf-8')
print('Figure 5 updated, sources parse.')
