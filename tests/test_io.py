#!/usr/bin/env python3

import io
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import jello.cli
from jello.lib import opts, read_file


def redirected(encoding, data=b''):
    """A redirected or piped stream in the locale encoding, e.g. cp1252 on Windows."""
    return io.TextIOWrapper(io.BytesIO(data), encoding=encoding, newline='\n', write_through=True)


class MyTests(unittest.TestCase):

    def setUp(self):
        for name in ('initialize', 'version_info', 'helpme', 'compact', 'nulls', 'empty', 'raw',
                     'lines', 'force_color', 'mono', 'schema', 'types'):
            setattr(opts, name, None)

        fd, self.path = tempfile.mkstemp(suffix='.json')
        with os.fdopen(fd, 'wb') as f:
            f.write('{"city": "Москва"}'.encode('utf-8'))

        env = mock.patch.dict(os.environ)
        env.start()
        self.addCleanup(env.stop)
        os.environ.pop('PYTHONIOENCODING', None)

    def tearDown(self):
        os.remove(self.path)

    def test_read_file_utf8(self):
        """
        Test that -f and -q files are read as UTF-8, with or without a BOM
        """
        self.assertEqual('{"city": "Москва"}', read_file(self.path))

        with open(self.path, 'wb') as f:
            f.write(b'\xef\xbb\xbf' + '{"city": "Москва"}'.encode('utf-8'))
        self.assertEqual('{"city": "Москва"}', read_file(self.path))

    def test_stdin_utf8(self):
        """
        Test that STDIN is decoded as UTF-8, not in the locale encoding
        """
        with mock.patch.object(sys, 'stdin', redirected('cp1252', '{"city": "Москва"}'.encode('utf-8'))):
            self.assertEqual('{"city": "Москва"}', jello.cli.get_stdin())

    def test_redirected_stdout_utf8(self):
        """
        Test that output to a redirected STDOUT is UTF-8, so non-Latin text
        does not raise UnicodeEncodeError in the locale encoding
        """
        stdout = redirected('cp1252')
        with mock.patch.object(sys, 'stdout', stdout), \
             mock.patch.object(sys, 'argv', ['jello', '_.city']):
            jello.cli.main(data='{"city": "Москва"}')
        self.assertEqual('"Москва"\n', stdout.buffer.getvalue().decode('utf-8'))

    def test_redirected_stdout_keeps_pythonioencoding(self):
        os.environ['PYTHONIOENCODING'] = 'utf-16'
        stdout = redirected('utf-16')
        with mock.patch.object(sys, 'stdout', stdout), \
             mock.patch.object(sys, 'argv', ['jello', '_.city']):
            jello.cli.main(data='{"city": "abc"}')
        self.assertEqual('"abc"\n', stdout.buffer.getvalue().decode('utf-16'))

    def test_stdin_redirected_from_file(self):
        """
        Test that STDIN redirected from a file is read
        """
        with open(self.path, 'rb') as stdin:
            result = subprocess.run([sys.executable, '-m', 'jello', '_.city'], stdin=stdin,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        self.assertEqual('"Москва"', result.stdout.decode('utf-8').strip())

    def _enable_windows_colors(self, platform, isatty):
        stdout = mock.Mock()
        stdout.isatty.return_value = isatty
        with mock.patch('sys.platform', platform), mock.patch('sys.stdout', stdout), \
             mock.patch('subprocess.run') as run:
            jello.cli.enable_windows_colors()
        return run

    def test_enable_windows_colors_on_console(self):
        """
        Test that cmd.exe enables colors on a Windows console without getting
        jello's STDIN: when STDIN is a redirected file, cmd.exe moved its
        position to the end
        """
        run = self._enable_windows_colors('win32', isatty=True)
        run.assert_called_once_with('', shell=True, stdin=subprocess.DEVNULL)

    def test_enable_windows_colors_skipped(self):
        """
        Test that cmd.exe is not started when STDOUT is not a console or not on Windows
        """
        self._enable_windows_colors('win32', isatty=False).assert_not_called()
        self._enable_windows_colors('linux', isatty=True).assert_not_called()


if __name__ == '__main__':
    unittest.main()
