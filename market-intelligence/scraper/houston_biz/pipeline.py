"""Normalize local permit CSVs into candidate leads for the harness.

No contact enrichment or network access. Industry filters are targeting heuristics.
"""
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import unicodedata

PIPELINE_FIELDS = ['id', 'organization', 'contact_reference', 'source', 'verified_at',
                   'stage', 'owner', 'next_action', 'due', 'do_not_contact', 'notes']
ALIASES = {
    'name': ('Business / DBA Name', 'Business Name (DBA)', 'outlet_name'),
    'legal': ('Legal Entity Name', 'Legal Taxpayer Name', 'taxpayer_name'),
    'address': ('Street Address', 'outlet_address'),
    'city': ('City', 'outlet_city'),
    'state': ('State', 'outlet_state'),
    'zip': ('ZIP Code', 'outlet_zip'),
    'naics': ('NAICS Code', 'outlet_naics_code'),
}


def clean(value):
    return ' '.join(unicodedata.normalize('NFKC', value or '').split())


def key(value):
    return clean(value).casefold()


def spreadsheet_text(value):
    value = clean(value)
    return "'"+value if value.startswith(('=', '+', '-', '@')) else value


def normalize(inputs, vertical, cities):
    allowed = {key(c) for c in cities}
    if not allowed or '' in allowed:
        raise ValueError('Supply at least one nonempty city')
    stats = dict(read=0, filtered=0, invalid=0, duplicates=0, exported=0)
    candidates = {}
    for source in inputs:
        source = Path(source)
        with source.open(newline='', encoding='utf-8-sig') as stream:
            reader = csv.DictReader(stream, strict=True)
            headers = reader.fieldnames or []
            if len(headers) != len(set(headers)):
                raise ValueError(f'{source}: duplicate CSV headers')
            columns = {field: next((name for name in names if name in headers), None)
                       for field, names in ALIASES.items()}
            if any(columns[field] is None for field in ('name', 'address', 'city', 'state', 'zip', 'naics')):
                raise ValueError(f'{source}: unsupported header; need business name, address, city, state, ZIP and NAICS')
            for raw in reader:
                stats['read'] += 1
                if None in raw or any(value is None for value in raw.values()):
                    raise ValueError(f'{source}: wrong column count near line {reader.line_num}')
                if any('\x00' in value for value in raw.values()):
                    raise ValueError(f'{source}: NUL byte near line {reader.line_num}')
                row = {field: clean(raw.get(column, '')) for field, column in columns.items()}
                naics = row['naics']
                if not re.fullmatch(r'[0-9]{6}', naics) or not re.fullmatch(r'[0-9]{5}(?:-[0-9]{4})?', row['zip']):
                    stats['invalid'] += 1
                    continue
                if not row['name'] or not row['address'] or not row['city']:
                    stats['invalid'] += 1
                    continue
                contractor = naics.startswith('238') or naics == '236220'
                clinic = naics.startswith(('6211', '6212', '6213', '6214'))
                selected = contractor if vertical == 'contractors' else clinic if vertical == 'clinics' else contractor or clinic
                if row['state'].upper() != 'TX' or key(row['city']) not in allowed or not selected:
                    stats['filtered'] += 1
                    continue
                # Location-level deduplication: preserve distinct branches/suites.
                identity = [key(row[field]) for field in ('name', 'address', 'city')]+['tx', row['zip'][:5]]
                digest = hashlib.sha256(json.dumps(identity, ensure_ascii=False).encode('utf-8')).hexdigest()[:24]
                identifier = 'L'+digest
                if identifier in candidates:
                    stats['duplicates'] += 1
                    continue
                record = dict.fromkeys(PIPELINE_FIELDS, '')
                record.update(id=identifier, organization=spreadsheet_text(row['name']),
                    contact_reference=spreadsheet_text(f"Location: {row['address']}, {row['city']}, TX {row['zip'][:5]}"),
                    source='local-permit-csv:'+str(source.resolve()), stage='research',
                    next_action='Verify operating status, official business contact, fit, and outreach eligibility',
                    do_not_contact='false', notes=json.dumps(dict(legal_name=row['legal'], naics=naics,
                        candidate_type='contractor' if contractor else 'clinic',
                        qualification='Unverified registry candidate; no phone or email supplied'), ensure_ascii=False))
                candidates[identifier] = record
    records = sorted(candidates.values(), key=lambda row: (key(row['organization']), row['id']))
    stats['exported'] = len(records)
    return records, stats


def export_pipeline(inputs, output, vertical='both', cities=('Houston',)):
    if vertical not in ('contractors', 'clinics', 'both'):
        raise ValueError('Unknown vertical')
    output = Path(output)
    if output.exists() or output.is_symlink():
        raise ValueError(f'Output already exists; use a new filename: {output}')
    records, stats = normalize(inputs, vertical, cities)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', newline='', encoding='utf-8',
                                         dir=output.parent, prefix='.pipeline-', delete=False) as stream:
            temporary = Path(stream.name)
            writer = csv.DictWriter(stream, PIPELINE_FIELDS)
            writer.writeheader()
            writer.writerows(records)
            stream.flush()
            os.fsync(stream.fileno())
        # Atomic publication without overwriting an output created concurrently.
        os.link(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return stats
