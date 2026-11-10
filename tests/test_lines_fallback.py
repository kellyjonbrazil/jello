#!/usr/bin/env python3

import unittest
from jello.lib import Json, opts


class TestLinesFallback(unittest.TestCase):
    def setUp(self):
        opts.compact = False
        opts.lines = True
        opts.nulls = False
        opts.raw = False
        opts.mono = True

    def test_lines_tuple_entry_serialized(self):
        output = Json().create_json([(1, 2)])
        self.assertIn("1", output)
        self.assertIn("2", output)
        self.assertTrue(output.strip())

    def test_lines_set_entry_not_dropped(self):
        output = Json().create_json([{1}])
        self.assertTrue(output.strip())
        self.assertIn("1", output)


if __name__ == "__main__":
    unittest.main()
