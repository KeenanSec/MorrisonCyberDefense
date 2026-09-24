#!/usr/bin/env python3
"""Local company workspace scaffolding. Python standard library only."""
import argparse
import csv
from datetime import date
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile

if __package__:
    from .storage import locked, read_csv, safe_path, write_csv
    from .leads import merge_pipeline, validate as validate_leads
else:
    from storage import locked, read_csv, safe_path, write_csv
    from leads import merge_pipeline, validate as validate_leads

BASE = Path(__file__).resolve().parent
TASK_FIELDS = ['id', 'title', 'owner', 'due', 'status', 'notes']
STATUSES = ('todo', 'doing', 'blocked', 'done')


def nonempty(value):
    value = value.strip()
    if not value or any(ord(c) < 32 for c in value):
        raise argparse.ArgumentTypeError('Provide nonempty text without control characters')
    return value


def valid_date(value):
    try:
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
            raise ValueError()
        date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError('Use a valid YYYY-MM-DD date') from None
    return value


def valid_slug(value):
    if len(value) > 80 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value):
        raise argparse.ArgumentTypeError('Use 1–80 lowercase letters/digits separated by single hyphens')
    return value


def validate_ids(records, pattern, label):
    seen = set()
    for record in records:
        identifier = record['id']
        if not re.fullmatch(pattern, identifier) or identifier in seen:
            raise ValueError(f'{label}: invalid or duplicate ID {identifier!r}')
        seen.add(identifier)


def tasks(path):
    records = read_csv(path, TASK_FIELDS)
    validate_ids(records, r'T[0-9]{4,}', path)
    for record in records:
        try:
            nonempty(record['title'])
            nonempty(record['owner'])
            valid_date(record['due'])
        except argparse.ArgumentTypeError as exc:
            raise ValueError(f'{path}: {record["id"]}: {exc}') from None
        if record['status'] not in STATUSES:
            raise ValueError(f'{path}: invalid status for {record["id"]}')
    return records


def schemas():
    return json.loads((BASE / 'templates/registers.json').read_text(encoding='utf-8'))


def workspace(root, registers):
    # Preflight existing files before creating missing ones. Never "repair" by erasing data.
    directory = safe_path(root/'projects')
    if directory.exists() and not directory.is_dir():
        raise ValueError(f'Expected project directory: {directory}')
    tables = {'tasks.csv': TASK_FIELDS, **{n: registers[n] for n in
              ('pipeline.csv', 'business-register.csv', 'metrics.csv')}}
    for name, fields in tables.items():
        path = safe_path(root/name)
        if path.exists():
            records = tasks(path) if name == 'tasks.csv' else read_csv(path, fields)
            if name == 'pipeline.csv':
                validate_leads(records, path)
    decision = safe_path(root/'decisions.md')
    if decision.exists() and not decision.is_file():
        raise ValueError(f'Expected file: {decision}')
    directory.mkdir(exist_ok=True, mode=0o700)
    for name, fields in tables.items():
        if not (root/name).exists():
            write_csv(root/name, fields, [])
    if not decision.exists():
        shutil.copyfile(BASE/'templates/decisions.md', decision)


def project(root, slug):
    path = safe_path(root/'projects'/slug)
    if not path.is_dir():
        raise ValueError(f'Project does not exist: {slug}')
    return path


def create_project(root, args, registers):
    parent = safe_path(root/'projects')
    target = safe_path(parent/args.slug)
    if target.exists():
        raise ValueError(f'Project already exists: {args.slug}')
    # Publish only a fully populated project; remove staging if any step fails.
    with tempfile.TemporaryDirectory(dir=parent, prefix='.mcd-project-') as temporary:
        path = Path(temporary)/'project'
        path.mkdir(mode=0o700)
        meta = dict(name=args.name, owner=args.owner, kind=args.kind,
                    created=date.today().isoformat(), status='planning')
        (path/'project.json').write_text(json.dumps(meta, indent=2)+'\n', encoding='utf-8')
        names = ['decisions.md']
        if args.kind == 'client':
            names += ['scope.md', 'approvals.md', 'report.md', 'monthly-review.md', 'incident.md', 'closeout.md']
            for name in ('evidence.csv', 'findings.csv', 'changes.csv'):
                write_csv(path/name, registers[name], [])
        for name in names:
            shutil.copyfile(BASE/'templates'/name, path/name)
        write_csv(path/'tasks.csv', TASK_FIELDS, [])
        (path/'README.md').write_text(
            f'# {args.name}\n\nOwner: {args.owner}\nKind: {args.kind}\n\n'
            '## Objective\n\nDescribe the intended result.\n\n'
            '## Completion criteria\n\nDefine how completion will be verified.\n\n'
            '## Milestones and references\n\nLink procedures, documents, and decisions.\n\n'
            'Track work in tasks.csv; update project.json status manually.\n', encoding='utf-8')
        path.rename(target)
    print(f'Created: {target}')


def dashboard(root):
    lines = [f'Workspace: {root}', f'As of: {date.today()}']
    scopes = [('Company', root)]
    for candidate in sorted(safe_path(root/'projects').iterdir()):
        if candidate.name.startswith('.mcd-project-'):
            continue
        path = safe_path(candidate)
        if not path.is_dir():
            continue
        meta = json.loads(safe_path(path/'project.json').read_text(encoding='utf-8'))
        if not isinstance(meta, dict) or any(not isinstance(meta.get(k), str) or not meta[k].strip()
                                             for k in ('name', 'owner', 'status')):
            raise ValueError(f'{path}: invalid project metadata')
        lines.append(f'Project {path.name}: {meta["name"]} | {meta["owner"]} | {meta["status"]}')
        scopes.append((path.name, path))
    count = 0
    for label, path in scopes:
        for record in tasks(path/'tasks.csv'):
            if record['status'] == 'done':
                continue
            count += 1
            late = ' OVERDUE' if record['due'] < date.today().isoformat() else ''
            lines.append(f'{label}/{record["id"]} [{record["status"]}{late}] {record["title"]} | {record["owner"]} | due {record["due"]}')
    print('\n'.join(lines + [f'{count} open tasks']))


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace', type=Path, default=BASE/'local', help='Working data location (default: harness/local)')
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('init', help='Initialize without overwriting existing data')
    n = sub.add_parser('new', help='Create an internal project or client engagement')
    n.add_argument('slug', type=valid_slug)
    n.add_argument('--name', required=True, type=nonempty)
    n.add_argument('--owner', required=True, type=nonempty)
    n.add_argument('--kind', choices=['internal', 'client'], default='internal')
    a = sub.add_parser('task', help='Add an owned task')
    a.add_argument('title', type=nonempty)
    a.add_argument('--owner', required=True, type=nonempty)
    a.add_argument('--due', required=True, type=valid_date)
    a.add_argument('--project', type=valid_slug)
    s = sub.add_parser('status', help='Update a task status')
    s.add_argument('id')
    s.add_argument('status', choices=STATUSES)
    s.add_argument('--project', type=valid_slug)
    s.add_argument('--note', default=None)
    sub.add_parser('dashboard', help='Display open tasks')
    lead = sub.add_parser('import-leads', help='Append normalized prospect CSV; preserve existing records')
    lead.add_argument('file', type=Path)
    lead.add_argument('--owner', type=nonempty)
    lead.add_argument('--dry-run', action='store_true')
    return p


def execute(root, args, registers):
    if args.command == 'init':
        workspace(root, registers)
        print(f'Workspace ready: {root}')
        return
    if not safe_path(root/'tasks.csv').is_file() or not safe_path(root/'projects').is_dir():
        raise ValueError('Run init first with the same --workspace location')
    if args.command == 'new':
        create_project(root, args, registers)
    elif args.command in ('task', 'status'):
        path = (project(root, args.project) if args.project else root)/'tasks.csv'
        data = tasks(path)
        if args.command == 'task':
            identifier = f'T{max([int(r["id"][1:]) for r in data] or [0])+1:04d}'
            data.append(dict(id=identifier, title=args.title, owner=args.owner,
                             due=args.due, status='todo', notes=''))
            message = f'Added {identifier}: {args.title}'
        else:
            match = next((r for r in data if r['id'] == args.id), None)
            if match is None:
                raise ValueError(f'Unknown task: {args.id}')
            if args.note is not None:
                if '\x00' in args.note:
                    raise ValueError('Notes must not contain NUL bytes')
                match['notes'] = args.note
            match['status'] = args.status
            message = f'{args.id}: {args.status}'
        write_csv(path, TASK_FIELDS, data)
        print(message)
    elif args.command == 'dashboard':
        dashboard(root)
    elif args.command == 'import-leads':
        result = merge_pipeline(root/'pipeline.csv', safe_path(args.file), registers['pipeline.csv'],
                                args.owner, args.dry_run)
        print(json.dumps(result, sort_keys=True))


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        root = safe_path(args.workspace)
        registers = schemas()
        if args.command == 'init':
            root.mkdir(parents=True, exist_ok=True, mode=0o700)
        elif not root.is_dir():
            raise ValueError('Run init first with the same --workspace location')
        with locked(root):
            execute(root, args, registers)
        return 0
    except (OSError, ValueError, KeyError, TypeError, csv.Error) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
