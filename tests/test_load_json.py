#!/usr/bin/env python3

import unittest
from jello.lib import load_json


class MyTests(unittest.TestCase):
    pretty_json =  '''\
{
    "foo": 1,
    "bar": 2,
    "baz": 3
}'''

    compact_json = '''{"foo": 1,"bar": 2,"baz": 3}'''

    json_lines = '''\
{"foo": 1,"bar": 2,"baz": 3}
{"foo": 4,"bar": 5,"baz": 6}
{"foo": 7,"bar": 8,"baz": 9}'''

    json_lines_extra_spaces = '''\
     
{"foo": 1,"bar": 2,"baz": 3}

{"foo": 4,"bar": 5,"baz": 6}
          
{"foo": 7,"bar": 8,"baz": 9}
     
    '''

    def test_load_pretty_json(self):
        """
        Test with pretty JSON
        """
        expected = {'foo': 1, 'bar': 2, 'baz': 3}
        self.assertEqual(load_json(self.pretty_json), expected)

    def test_load_compact_json(self):
        """
        Test with compact JSON
        """
        expected = {'foo': 1, 'bar': 2, 'baz': 3}
        self.assertEqual(load_json(self.compact_json), expected)

    def test_load_json_lines(self):
        """
        Test with JSON Lines
        """
        expected = [{'foo': 1, 'bar': 2, 'baz': 3}, {'foo': 4, 'bar': 5, 'baz': 6}, {'foo': 7, 'bar': 8, 'baz': 9}]
        self.assertEqual(load_json(self.json_lines), expected)

    def test_load_json_lines_with_extra_whitespace(self):
        """
        Test with JSON Lines with extra blank lines and whitespace
        """
        expected = [{'foo': 1, 'bar': 2, 'baz': 3}, {'foo': 4, 'bar': 5, 'baz': 6}, {'foo': 7, 'bar': 8, 'baz': 9}]
        self.assertEqual(load_json(self.json_lines_extra_spaces), expected)


if __name__ == '__main__':
    unittest.main()
