import contextlib
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from harness import mcd, storage

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO/'market-intelligence/scraper'))
from houston_biz.pipeline import PIPELINE_FIELDS, export_pipeline

HEADERS = ['Business / DBA Name', 'Legal Entity Name', 'Street Address', 'City', 'State', 'ZIP Code', 'NAICS Code']


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root/'input.csv'
        self.output = self.root/'leads.csv'
        self.workspace = self.root/'workspace'
        self.call('init')

    def call(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = mcd.main(['--workspace', str(self.workspace), *map(str, args)])
        return code, output.getvalue()

    def fixture(self, rows):
        with self.source.open('w', newline='', encoding='utf-8-sig') as stream:
            writer = csv.writer(stream)
            writer.writerow(HEADERS)
            writer.writerows(rows)

    def row(self, name='Test Contractor', address='1 Main St', city='Houston', state='TX', zipcode='77001', naics='238220'):
        return [name, 'Legal Name', address, city, state, zipcode, naics]

    def export(self, **kwargs):
        return export_pipeline([self.source], self.output, **kwargs)

    def test_filters_deduplication_and_stable_ids(self):
        self.fixture([self.row(), self.row(name=' test   contractor ', city='HOUSTON', zipcode='77001-1234'),
                      self.row(address='2 Main St'), self.row(name='Clinic', naics='621111'),
                      self.row(name='Home health', naics='621610'), self.row(city='Dallas'),
                      self.row(state='CA'), self.row(zipcode='bad'), self.row(name=''),
                      self.row(name='Commercial Builder', naics='236220')])
        stats = self.export()
        self.assertEqual(stats, dict(read=10, filtered=3, invalid=2, duplicates=1, exported=4))
        data = storage.read_csv(self.output, PIPELINE_FIELDS)
        self.assertTrue(all(r['verified_at']=='' and r['stage']=='research' for r in data))
        first_ids = {r['id'] for r in data}
        other = self.root/'second.csv'
        export_pipeline([self.source], other)
        self.assertEqual(first_ids, {r['id'] for r in storage.read_csv(other, PIPELINE_FIELDS)})
        self.assertEqual(PIPELINE_FIELDS, mcd.schemas()['pipeline.csv'])

    def test_explicit_city_and_vertical_filter(self):
        self.fixture([self.row(city='Katy'), self.row(name='Katy Clinic', city='Katy', naics='621210'), self.row()])
        self.assertEqual(self.export(vertical='clinics', cities=['Katy'])['exported'], 1)

    def test_no_overwrite_or_partial_output(self):
        self.fixture([self.row()])
        self.output.write_text('existing work')
        with self.assertRaises(ValueError):
            self.export()
        self.assertEqual(self.output.read_text(), 'existing work')
        self.output.unlink()
        self.source.write_text('wrong,header\n')
        with self.assertRaises(ValueError):
            self.export()
        self.assertFalse(self.output.exists())

    def test_malformed_row_rejected(self):
        self.fixture([self.row(), ['short']])
        with self.assertRaises(ValueError):
            self.export()
        self.assertFalse(self.output.exists())

    def test_formula_escaping(self):
        self.fixture([self.row(name='=SUM(1,2)')])
        self.export()
        self.assertTrue(storage.read_csv(self.output, PIPELINE_FIELDS)[0]['organization'].startswith("'="))

    def test_import_preview_repeat_and_preserve_edits(self):
        self.fixture([self.row()])
        self.export()
        pipeline = self.workspace/'pipeline.csv'
        before = pipeline.read_bytes()
        code, result = self.call('import-leads', self.output, '--dry-run')
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(result)['added'], 1)
        self.assertEqual(pipeline.read_bytes(), before)
        self.assertEqual(self.call('import-leads', self.output, '--owner', 'Keenan')[0], 0)
        data = storage.read_csv(pipeline, PIPELINE_FIELDS)
        data[0].update(notes='Spoke to owner; do not overwrite', stage='do-not-contact', do_not_contact='true')
        storage.write_csv(pipeline, PIPELINE_FIELDS, data)
        before = pipeline.read_bytes()
        self.assertEqual(json.loads(self.call('import-leads', self.output)[1])['duplicates'], 1)
        self.assertEqual(pipeline.read_bytes(), before)
        self.fixture([self.row(address='99 Other St')])
        self.output.unlink()
        self.export()
        self.assertEqual(json.loads(self.call('import-leads', self.output)[1])['suppressed'], 1)
        self.assertEqual(pipeline.read_bytes(), before)

    def test_corrupt_import_does_not_change_pipeline(self):
        self.fixture([self.row()])
        self.export()
        records = storage.read_csv(self.output, PIPELINE_FIELDS)
        records[0]['due'] = 'not-a-date'
        storage.write_csv(self.output, PIPELINE_FIELDS, records)
        pipeline = self.workspace/'pipeline.csv'
        before = pipeline.read_bytes()
        self.assertEqual(self.call('import-leads', self.output)[0], 1)
        self.assertEqual(pipeline.read_bytes(), before)

    def test_duplicate_incoming_ids_rejected(self):
        self.fixture([self.row()])
        self.export()
        data = storage.read_csv(self.output, PIPELINE_FIELDS)
        storage.write_csv(self.output, PIPELINE_FIELDS, data*2)
        self.assertEqual(self.call('import-leads', self.output)[0], 1)

    def test_actual_cli_offline_roundtrip(self):
        self.fixture([self.row()])
        result = subprocess.run([sys.executable, '-m', 'houston_biz', 'pipeline-leads',
                                 '--input', str(self.source), '--output', str(self.output)],
                                cwd=REPO/'market-intelligence/scraper', capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run([sys.executable, str(REPO/'harness/mcd.py'), '--workspace',
                                 str(self.workspace), 'import-leads', str(self.output)],
                                cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['added'], 1)


if __name__ == '__main__':
    unittest.main()
