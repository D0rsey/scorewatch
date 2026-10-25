"""Refresh ScoreWatch from a user-downloaded GotSport XLSX export. Python standard library only."""
import sys,zipfile,xml.etree.ElementTree as ET,json,re,datetime,pathlib
root=pathlib.Path(__file__).resolve().parent
if len(sys.argv)!=2:raise SystemExit('Usage: python update_from_export.py /path/to/export.xlsx')
z=zipfile.ZipFile(sys.argv[1]);ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'};ss=[]
if 'xl/sharedStrings.xml' in z.namelist():ss=[''.join(t.text or '' for t in x.findall('.//m:t',ns)) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
rows=[]
for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//m:sheetData/m:row',ns):
 d={}
 for c in row.findall('m:c',ns):
  v=c.find('m:v',ns);inline=c.find('m:is',ns);val=v.text if v is not None else ''.join(t.text or '' for t in inline.findall('.//m:t',ns)) if inline is not None else ''
  if c.get('t')=='s':val=ss[int(val)]
  d[re.match('[A-Z]+',c.get('r')).group()]=val
 rows.append(d)
if [rows[0].get(k) for k in 'ABCDEFGHI']!=['Match #','Date','Time','Home Team','Results','Away Team','Location','Division','Status']:raise SystemExit('Unexpected GotSport export columns; refusing to overwrite data')
games=[]
for r in rows[1:]:
 date=datetime.datetime.strptime(' '.join(r['B'].split()),'%A, %B %d, %Y').date().isoformat();score=re.fullmatch(r'\s*(\d+)\s*-\s*(\d+)\s*',r['E']);games.append(dict(id=r['A'],date=date,time=r['C'],home=r['D'],away=r['F'],homeScore=int(score[1]) if score else None,awayScore=int(score[2]) if score else None,location=r['G'],division=r['H'],sourceStatus=r['I']))
old=json.loads((root/'data.json').read_text());before={g['id']:g for g in old['games']};changes=[]
for g in games:
 prev=before.get(g['id'])
 if not prev:changes.append({'type':'new_match','match':g['id']});continue
 for k in ('date','time','home','away','location','homeScore','awayScore','sourceStatus'):
  if prev.get(k)!=g.get(k):changes.append({'type':'score_change' if 'Score' in k else 'schedule_or_status_change','match':g['id'],'field':k,'before':prev.get(k),'after':g.get(k)})
for mid in before:
 if mid not in {g['id'] for g in games}:changes.append({'type':'missing_from_export','match':mid})
old['games']=games;(root/'data.json').write_text(json.dumps(old,indent=2));(root/'data.js').write_text('window.SCOREWATCH_DATA = '+json.dumps(old,ensure_ascii=False)+';');(root/'changes.json').write_text(json.dumps(changes,indent=2));print(f'Imported {len(games)} games; {len(changes)} changes. See changes.json')
