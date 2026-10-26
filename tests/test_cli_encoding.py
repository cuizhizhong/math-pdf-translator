import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CommandLineEncodingTests(unittest.TestCase):
    def test_non_chinese_windows_output_encoding(self):
        environment = dict(os.environ, PYTHONIOENCODING='cp1252')
        with tempfile.TemporaryDirectory() as directory:
            commands = [
                ('install.py', ['--dry-run', '--dest', str(Path(directory) / 'skills')], 0),
                ('validate_package.py', [], 0),
                ('check_environment.py', ['--skills-root', str(Path(directory) / 'missing')], 1),
                ('smoke_templates.py', ['--help'], 0),
            ]
            for script, arguments, expected in commands:
                with self.subTest(script=script):
                    result = subprocess.run([sys.executable, str(ROOT / 'scripts' / script), *arguments],
                                            env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
                    self.assertEqual(result.returncode, expected, result.stderr.decode('utf-8', errors='replace'))
                    output = result.stdout.decode('utf-8')
                    self.assertTrue(output)
                    self.assertNotIn(b'UnicodeEncodeError', result.stderr)
                    if script == 'check_environment.py':
                        self.assertFalse(json.loads(output)['ok'])


if __name__ == '__main__':
    unittest.main()
