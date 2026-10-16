"""Build self-contained skill ZIPs from the versioned fused-skills tree."""
from pathlib import Path
import argparse
import json
import zipfile

ROOT=Path(__file__).resolve().parents[1]
def build(out):
 out=Path(out).resolve();out.mkdir(parents=True,exist_ok=True)
 manifest=json.loads((ROOT/'distribution/manifest.json').read_text(encoding='utf-8'))
 def closure(selected):
  names=set()
  def add(name):
   if name in names:return
   names.add(name)
   for dep in manifest['skills'][name]['dependencies']:add(dep)
  for name in selected:add(name)
  return sorted(names)
 results=[]
 for selection in [list(manifest['skills'])]+[[name] for name in manifest['skills']]:
  names=closure(selection);filename='bo-local-skills.zip' if len(selection)>1 else 'bo-skill-'+selection[0]+'.zip'
  payload={**manifest,'skills':{n:manifest['skills'][n] for n in names},'selected':selection}
  with zipfile.ZipFile(out/filename,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
   z.write(ROOT/'distribution/install.py','install.py')
   z.write(ROOT/'distribution/README.md','README.md')
   z.writestr('manifest.json',json.dumps(payload,ensure_ascii=False,indent=2))
   for name in names:
    source=ROOT/manifest['skills'][name].get('sourcePath','fused-skills/'+name)
    for p in sorted(source.rglob('*')):
     if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ['.pyc','.pyo']:z.write(p,Path('skills')/name/p.relative_to(source))
  results.append({'name':selection[0] if len(selection)==1 else 'all','file':filename,'bytes':(out/filename).stat().st_size,'includedSkills':names})
 (out/'index.json').write_text(json.dumps({'version':manifest['version'],'packages':results},ensure_ascii=False,indent=2),encoding='utf-8')
 return results
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);args=p.parse_args()
 for result in build(args.out):print(result['file'],round(result['bytes']/1024),'KiB',','.join(result['includedSkills']))
