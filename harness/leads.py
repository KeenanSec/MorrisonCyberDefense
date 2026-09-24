"""Append-only prospect ingestion with exact schema validation and opt-out preservation."""
from datetime import date
import re
import unicodedata

if __package__:
    from .storage import read_csv, write_csv
else:
    from storage import read_csv, write_csv

STAGES = {'research', 'qualified', 'discovery', 'proposal', 'won', 'lost', 'do-not-contact'}


def normalized(value):
    return ' '.join(unicodedata.normalize('NFKC', value).split()).casefold()


def validate(records, source):
    seen = set()
    for record in records:
        identifier = record['id']
        if not identifier.strip() or identifier in seen or not record['organization'].strip():
            raise ValueError(f'{source}: missing organization or invalid/duplicate ID {identifier!r}')
        seen.add(identifier)
        if record['stage'] not in STAGES:
            raise ValueError(f'{source}: invalid stage for {identifier}')
        if record['do_not_contact'].casefold() not in ('', 'true', 'false'):
            raise ValueError(f'{source}: do_not_contact must be blank, true, or false')
        for field in ('due', 'verified_at'):
            value = record[field]
            if value:
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                    raise ValueError(f'{source}: {field} must use YYYY-MM-DD')
                date.fromisoformat(value)


def merge_pipeline(destination, source, fields, owner=None, dry_run=False):
    existing = read_csv(destination, fields)
    incoming = read_csv(source, fields)
    validate(existing, destination)
    validate(incoming, source)
    identifiers = {r['id'] for r in existing}
    locations = {(normalized(r['organization']), normalized(r['contact_reference'])) for r in existing}
    # An existing organization opt-out protects every imported location of that name.
    suppressed = {normalized(r['organization']) for r in existing
                  if r['do_not_contact'].casefold() == 'true' or r['stage'] == 'do-not-contact'}
    added, duplicate, blocked = [], 0, 0
    for record in incoming:
        organization = normalized(record['organization'])
        location = (organization, normalized(record['contact_reference']))
        if record['id'] in identifiers or location in locations:
            duplicate += 1
            continue
        if organization in suppressed:
            blocked += 1
            continue
        record = dict(record)
        if owner is not None:
            record['owner'] = owner
        added.append(record)
        identifiers.add(record['id'])
        locations.add(location)
    if added and not dry_run:
        write_csv(destination, fields, existing + added)
    return dict(added=len(added), duplicates=duplicate, suppressed=blocked, dry_run=dry_run)
