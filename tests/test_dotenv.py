import os
import tempfile
import unittest

from src.dotenv import load_env
import src.dotenv


class TestDotEnv(unittest.TestCase):

    def test_file_not_found(self):
        with self.assertLogs(src.dotenv.__name__, level='DEBUG'):
            load_env('.file_not_found')

    def test_loading_ok(self):
        with tempfile.NamedTemporaryFile('w', delete=True) as tmp:
            tmp.write('''VAR_00=1234
            VAR_01=ABCD''')
            tmp.flush()
            load_env(tmp.name)
            self.assertEqual('1234', os.environ.get('VAR_00'))
            self.assertEqual('ABCD', os.environ.get('VAR_01'))
