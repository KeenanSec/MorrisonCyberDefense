import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest

from harness import mcd

class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'work'
    def run_cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = mcd.main(['--workspace', str(self.root), *args])
        return result, output.getvalue()
    def test_lifecycle_and_no_overwrite(self):
        self.assertEqual(self.run_cli('init')[0], 0)
        self.assertEqual(self.run_cli('new','sample','--name','Sample','--owner','Principal','--kind','client')[0],0)
        report=self.root/'projects/sample/report.md'
        report.write_text('Work in progress')
        self.assertEqual(self.run_cli('new','sample','--name','Other','--owner','Other')[0],1)
        self.assertEqual(report.read_text(),'Work in progress')
        self.assertEqual(self.run_cli('task','Review evidence','--owner','Keenan','--due','2020-01-01','--project','sample')[0],0)
        self.assertIn('OVERDUE',self.run_cli('dashboard')[1])
        self.assertEqual(self.run_cli('status','T0001','done','--project','sample')[0],0)
        self.assertIn('0 open tasks',self.run_cli('dashboard')[1])
        self.assertEqual(self.run_cli('init')[0],0)
        self.assertEqual(report.read_text(),'Work in progress')
    def test_invalid_task_does_not_mutate(self):
        self.run_cli('init')
        before=(self.root/'tasks.csv').read_bytes()
        self.assertEqual(self.run_cli('status','T9999','done')[0],1)
        self.assertEqual((self.root/'tasks.csv').read_bytes(),before)
    def test_path_traversal_rejected(self):
        with self.assertRaises(Exception):
            mcd.valid_slug('../escape')
    def test_missing_workspace_not_created(self):
        self.assertEqual(self.run_cli('dashboard')[0],1)
        self.assertFalse(self.root.exists())

if __name__ == '__main__':
    unittest.main()
