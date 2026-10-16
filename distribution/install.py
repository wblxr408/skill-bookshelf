"""Install selected complete skill directories into a client skills directory."""
from pathlib import Path
import argparse
import datetime
import json
import os
import re
import shutil
import tempfile

def install(source, destination, selected=None, replace=False):
    source=Path(source).resolve();destination=Path(destination).expanduser().resolve()
    manifest=json.loads((source/'manifest.json').read_text(encoding='utf-8'))
    skills=manifest['skills'];chosen=list(skills) if selected is None else list(selected)
    if not chosen:raise ValueError('Choose at least one skill')
    planned=[];seen=set()
    def visit(name):
        if name in seen:return
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*',name) or name not in skills:raise ValueError('Unknown skill: '+str(name))
        seen.add(name)
        for dependency in skills[name].get('dependencies',[]):visit(dependency)
        planned.append(name)
    for name in chosen:visit(name)
    # Reject all conflicts before touching any selected skill.
    conflicts=[]
    for name in planned:
        target=destination/name
        if target.resolve()!=target:raise ValueError('Refusing a linked target: '+str(target))
        if target.exists():
            if not replace:conflicts.append(name)
            elif not target.is_dir():raise ValueError('Skill target is not a directory: '+str(target))
        src=source/'skills'/name
        if src.resolve().parent!=(source/'skills').resolve() or not src.is_dir():raise ValueError('Invalid bundled skill: '+name)
    if conflicts:raise FileExistsError('Existing skills: '+', '.join(conflicts)+'. Use --replace to back them up and replace.')
    destination.mkdir(parents=True,exist_ok=True)
    backup=None;committed=[];moved=[]
    with tempfile.TemporaryDirectory(prefix='.bo-skills-stage-',dir=destination.parent) as staging:
        stage=Path(staging)
        for name in planned:shutil.copytree(source/'skills'/name,stage/name)
        try:
            for name in planned:
                target=destination/name
                if target.exists():
                    if backup is None:
                        stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
                        backup=destination/'.bo-backups'/stamp;backup.mkdir(parents=True)
                    target.rename(backup/name);moved.append(name)
                (stage/name).rename(target);committed.append(name)
        except Exception:
            for name in reversed(committed):
                target=destination/name
                if target.resolve().parent!=destination:raise RuntimeError('Unsafe rollback target')
                shutil.rmtree(target)
            for name in reversed(moved):(backup/name).rename(destination/name)
            raise
    return {'installed':planned,'destination':str(destination),'backup':str(backup) if backup else None}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Install complete BO fused skills. Existing skills are protected by default.')
    parser.add_argument('--source',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--dest',type=Path,required=True,help='Client skills directory, e.g. ~/.agents/skills or ~/.claude/skills')
    parser.add_argument('--only',nargs='+',help='Select skills; dependencies are included automatically')
    parser.add_argument('--replace',action='store_true',help='Back up existing selected skills before replacing them')
    args=parser.parse_args()
    try:print(json.dumps(install(args.source,args.dest,args.only,args.replace),ensure_ascii=False,indent=2))
    except (ValueError,FileExistsError,OSError) as error:parser.exit(2,str(error)+'\n')
