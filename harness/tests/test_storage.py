import argparse
import contextlib
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from harness import mcd, storage


class RobustnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'workspace with spaces'
        self.assertEqual(self.call('init')[0], 0)

    def call(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = mcd.main(['--workspace', str(self.root), *args])
        return result, output.getvalue()

    def add(self):
        return self.call('task', 'Review, résumé', '--owner', 'Keenan', '--due', '2026-12-01')

    def test_csv_roundtrip_with_unicode_commas_and_multiline_notes(self):
        self.assertEqual(self.add()[0], 0)
        note = 'Line one, "quoted"\nLine two'
        self.assertEqual(self.call('status', 'T0001', 'blocked', '--note', note)[0], 0)
        records = mcd.tasks(self.root/'tasks.csv')
        self.assertEqual(records[0]['title'], 'Review, résumé')
        self.assertEqual(records[0]['notes'], note)
        self.assertEqual(self.call('status', 'T0001', 'doing', '--note', '')[0], 0)
        self.assertEqual(mcd.tasks(self.root/'tasks.csv')[0]['notes'], '')

    def test_malformed_csv_never_overwritten(self):
        path = self.root/'tasks.csv'
        header = ','.join(mcd.TASK_FIELDS)+'\n'
        cases = ['', 'id,title\n', header+'T0001,short\n',
                 header+'T0001,Test,Owner,2026-01-01,todo,,extra\n',
                 header+'T0001,"unterminated',
                 header+'bad,Test,Owner,2026-01-01,todo,\n',
                 header+'T0001,Test,Owner,2026-02-30,todo,\n',
                 header+'T0001,Test,Owner,2026-01-01,unknown,\n',
                 header+('T0001,Test,Owner,2026-01-01,todo,\n'*2)]
        for contents in cases:
            with self.subTest(contents=contents):
                path.write_text(contents)
                before = path.read_bytes()
                self.assertEqual(self.add()[0], 1)
                self.assertEqual(path.read_bytes(), before)

    def test_bom_and_missing_final_newline(self):
        path = self.root/'tasks.csv'
        path.write_text('\ufeff'+','.join(mcd.TASK_FIELDS)+'\nT0001,Old,Owner,2026-01-01,todo,', encoding='utf-8')
        self.assertEqual(self.add()[0], 0)
        self.assertEqual([r['id'] for r in mcd.tasks(path)], ['T0001', 'T0002'])

    def test_invalid_cli_values(self):
        for fn, value in [(mcd.nonempty, '  '), (mcd.nonempty, 'a\nb'),
                          (mcd.valid_date, '20260101'), (mcd.valid_date, '2026-02-30'),
                          (mcd.valid_slug, '../escape'), (mcd.valid_slug, 'a'*81)]:
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                fn(value)

    def test_symlinked_task_file_not_modified(self):
        target = Path(self.temp.name)/'outside.csv'
        path = self.root/'tasks.csv'
        path.rename(target)
        path.symlink_to(target)
        before = target.read_bytes()
        self.assertEqual(self.add()[0], 1)
        self.assertEqual(target.read_bytes(), before)

    def test_symlinked_parent_and_project_directory_rejected(self):
        alias = Path(self.temp.name)/'alias'
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            storage.safe_path(alias/'child')
        (self.root/'projects').rmdir()
        (self.root/'projects').symlink_to(Path(self.temp.name), target_is_directory=True)
        self.assertEqual(self.call('new', 'escape', '--name', 'Test', '--owner', 'Owner')[0], 1)
        self.assertFalse((Path(self.temp.name)/'escape').exists())

    def test_busy_workspace(self):
        before = (self.root/'tasks.csv').read_bytes()
        with storage.locked(self.root):
            code, output = self.add()
        self.assertEqual(code, 1)
        self.assertIn('busy', output)
        self.assertEqual((self.root/'tasks.csv').read_bytes(), before)

    def test_failed_write_preserves_original_and_cleans_temporary(self):
        before = (self.root/'tasks.csv').read_bytes()
        with patch('harness.storage.os.replace', side_effect=OSError('disk failure')):
            self.assertEqual(self.add()[0], 1)
        self.assertEqual((self.root/'tasks.csv').read_bytes(), before)
        self.assertEqual(list(self.root.glob('.mcd-*')), [])

    def test_project_creation_failure_leaves_no_partial_project(self):
        with patch('harness.mcd.shutil.copyfile', side_effect=OSError('copy failed')):
            self.assertEqual(self.call('new', 'sample', '--name', 'Test', '--owner', 'Owner')[0], 1)
        self.assertEqual(list((self.root/'projects').iterdir()), [])

    def test_init_preflights_existing_registers(self):
        pipeline = self.root/'pipeline.csv'
        pipeline.write_text('wrong,header\n')
        (self.root/'metrics.csv').unlink()
        self.assertEqual(self.call('init')[0], 1)
        self.assertFalse((self.root/'metrics.csv').exists())
        self.assertEqual(pipeline.read_text(), 'wrong,header\n')

    def test_invalid_project_metadata_returns_error_without_traceback(self):
        self.call('new', 'sample', '--name', 'Test', '--owner', 'Owner')
        for value in [[], {'name': None}, 'string']:
            (self.root/'projects/sample/project.json').write_text(json.dumps(value))
            code, output = self.call('dashboard')
            self.assertEqual(code, 1)
            self.assertNotIn('Traceback', output)

    def test_invalid_encoding_is_reported(self):
        (self.root/'tasks.csv').write_bytes(b'\xff\xff')
        code, output = self.add()
        self.assertEqual(code, 1)
        self.assertIn('Error:', output)


if __name__ == '__main__':
    unittest.main()
