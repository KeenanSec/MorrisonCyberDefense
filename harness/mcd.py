#!/usr/bin/env python3
"""Local company workspace scaffolding. Python standard library only."""
import argparse
import csv
import json
import os
from pathlib import Path
import re
import shutil
import sys
from datetime import date

BASE = Path(__file__).resolve().parent
REGISTERS = json.loads((BASE / 'templates/registers.json').read_text())
TASK_FIELDS = ['id', 'title', 'owner', 'due', 'status', 'notes']


def table(path, fields):
    if not path.exists():
        with path.open('x', newline='') as f:
            csv.writer(f).writerow(fields)


def rows(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f))


def valid_date(value):
    try:
        date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError('Use a valid YYYY-MM-DD date')
    return value


def valid_slug(value):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value):
        raise argparse.ArgumentTypeError('Use lowercase letters, digits, and single hyphens')
    return value


def workspace(root):
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    (root / 'projects').mkdir(exist_ok=True)
    table(root / 'tasks.csv', TASK_FIELDS)
    for name in ('pipeline.csv', 'business-register.csv', 'metrics.csv'):
        table(root / name, REGISTERS[name])
    if not (root / 'decisions.md').exists():
        shutil.copyfile(BASE / 'templates/decisions.md', root / 'decisions.md')


def project(root, slug):
    path = root / 'projects' / slug
    if path.is_symlink() or not path.is_dir():
        raise ValueError(f'Project does not exist or is a symlink: {slug}')
    return path


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace', type=Path, default=BASE/'local', help='Local data location; default: harness/local (gitignored)')
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('init', help='Create local company registers without overwriting existing data')
    n = sub.add_parser('new', help='Create a project or client engagement from templates')
    n.add_argument('slug', type=valid_slug)
    n.add_argument('--name', required=True)
    n.add_argument('--owner', required=True)
    n.add_argument('--kind', choices=['internal', 'client'], default='internal')
    a = sub.add_parser('task', help='Add an owned task')
    a.add_argument('title')
    a.add_argument('--owner', required=True)
    a.add_argument('--due', required=True, type=valid_date)
    a.add_argument('--project', type=valid_slug)
    s = sub.add_parser('status', help='Update a task status')
    s.add_argument('id')
    s.add_argument('status', choices=['todo', 'doing', 'blocked', 'done'])
    s.add_argument('--project', type=valid_slug)
    s.add_argument('--note', default='')
    sub.add_parser('dashboard', help='Show project status and all open tasks')
    args = p.parse_args(argv)
    root = args.workspace.expanduser().resolve()
    try:
        if args.command == 'init':
            workspace(root)
            print(f'Workspace ready: {root}')
            return 0
        if not (root/'tasks.csv').is_file():
            raise ValueError('Run init first with the same --workspace location')
        if args.command == 'new':
            path = root/'projects'/args.slug
            path.mkdir(mode=0o700)  # Exclusive creation: never replace existing work.
            metadata = {'name':args.name, 'owner':args.owner, 'kind':args.kind, 'created':date.today().isoformat(), 'status':'planning'}
            (path/'project.json').write_text(json.dumps(metadata, indent=2)+'\n')
            names = ['decisions.md']
            if args.kind == 'client':
                names += ['scope.md','approvals.md','report.md','monthly-review.md','incident.md','closeout.md']
                for name in ('evidence.csv','findings.csv','changes.csv'):
                    table(path/name, REGISTERS[name])
            for name in names:
                shutil.copyfile(BASE/'templates'/name, path/name)
            table(path/'tasks.csv', TASK_FIELDS)
            (path/'README.md').write_text(f'# {args.name}\n\nOwner: {args.owner}\nKind: {args.kind}\n\n## Objective\n\nDescribe the intended result.\n\n## Completion criteria\n\nDefine how completion will be verified.\n\n## Milestones and references\n\nLink relevant procedures, documents, and decisions.\n\nTrack work in tasks.csv; update project.json status manually.\n')
            print(f'Created: {path}')
        elif args.command in ('task','status'):
            path = (project(root,args.project) if args.project else root)/'tasks.csv'
            data = rows(path)
            if args.command == 'task':
                identifier = f'T{max([int(r["id"][1:]) for r in data] or [0])+1:04d}'
                with path.open('a', newline='') as f:
                    csv.DictWriter(f, TASK_FIELDS).writerow(dict(id=identifier,title=args.title,owner=args.owner,due=args.due,status='todo',notes=''))
                print(f'Added {identifier}: {args.title}')
            else:
                match = next((r for r in data if r['id']==args.id), None)
                if match is None:
                    raise ValueError(f'Unknown task: {args.id}')
                match['status']=args.status
                if args.note:
                    match['notes']=args.note
                temp=path.with_suffix('.tmp')
                with temp.open('w', newline='') as f:
                    writer=csv.DictWriter(f,TASK_FIELDS);writer.writeheader();writer.writerows(data)
                os.replace(temp,path)
                print(f'{args.id}: {args.status}')
        elif args.command == 'dashboard':
            print(f'Workspace: {root}\nAs of: {date.today()}')
            scopes=[('Company',root)]
            for path in sorted((root/'projects').iterdir()):
                if path.is_symlink() or not path.is_dir():
                    continue
                meta=json.loads((path/'project.json').read_text())
                print(f'Project {path.name}: {meta["name"]} | {meta["owner"]} | {meta["status"]}')
                scopes.append((path.name,path))
            count=0
            for label,path in scopes:
                for row in rows(path/'tasks.csv'):
                    if row['status']=='done':
                        continue
                    count+=1
                    late=' OVERDUE' if row['due'] and row['due']<date.today().isoformat() else ''
                    print(f'{label}/{row["id"]} [{row["status"]}{late}] {row["title"]} | {row["owner"]} | due {row["due"]}')
            print(f'{count} open tasks')
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
