#!/usr/bin/env python3

import unittest
import jello.cli
from jello.cli import opts


class MyTests(unittest.TestCase):
    def setUp(self):
        # initialize options
        opts.initialize = None
        opts.version_info = None
        opts.helpme = None
        opts.compact = None
        opts.nulls = None
        opts.raw = None
        opts.lines = None
        opts.mono = None
        opts.schema = None
        opts.keyname_color = None
        opts.keyword_color = None
        opts.number_color = None
        opts.string_color = None
        opts.arrayid_color = None
        opts.arraybracket_color = None

        # create samples
        self.dict_sample = {
            'string': 'string\nwith newline\ncharacters in it',
            'true': True,
            'false': False,
            'null': None,
            'int': 42,
            'float': 3.14,
            'array': [
                'string\nwith newline\ncharacters in it',
                True,
                False,
                None,
                42,
                3.14
            ]
        }

        self.list_sample = [
            'string\nwith newline\ncharacters in it',
            True,
            False,
            None,
            42,
            3.14
        ]

        self.list_of_dicts_sample = [
            {
                'string': 'string\nwith newline\ncharacters in it',
                'true': True,
                'false': False,
                'null': None,
                'int': 42,
                'float': 3.14,
                'array': [
                    'string\nwith newline\ncharacters in it',
                    True,
                    False,
                    None,
                    42,
                    3.14
                ]
            },
            {
                'string': 'another string\nwith newline\ncharacters in it',
                'true': True,
                'false': False,
                'null': None,
                'int': 10001,
                'float': -400.45,
                'array': [
                    'string\nwith newline\ncharacters in it',
                    True,
                    False,
                    None,
                    -6000034,
                    999999.854321
                ]
            }
        ]

        self.list_of_lists_sample = [
            [
                'string\nwith newline\ncharacters in it',
                True,
                False,
                None,
                42,
                3.14
            ],
            [
                'another string\nwith newline\ncharacters in it',
                True,
                False,
                None,
                42001,
                -3.14
            ]
        ]

    # ------------ Tests ------------

    def test_KeyError(self):
        """
        Test _.foo.nonexistent_key (KeyError)
        """
        self.data_in = {"foo": "bar"}
        self.query = '_.nonexistent_key'
        self.assertRaises(KeyError, jello.cli.pyquery, self.data_in, self.query)

    def test_IndexError(self):
        """
        Test _.foo[99] (IndexError)
        """
        self.data_in = [1,2,3]
        self.query = '_[9]'
        self.assertRaises(IndexError, jello.cli.pyquery, self.data_in, self.query)

    def test_SyntaxError(self):
        """
        Test % (SyntaxError)
        """
        self.data_in = [1,2,3]
        self.query = '%'
        self.assertRaises(SyntaxError, jello.cli.pyquery, self.data_in, self.query)

    def test_TypeError(self):
        """
        Test _[5] on None (TypeError)
        """
        self.data_in = None
        self.query = '_[5]'
        self.assertRaises(TypeError, jello.cli.pyquery, self.data_in, self.query)

    def test_AttributeError(self):
        """
        Test _.items() on list (AttributeError)
        """
        self.data_in = [1,2,3]
        self.query = '_.items()'
        self.assertRaises(AttributeError, jello.cli.pyquery, self.data_in, self.query)

    def test_NameError(self):
        """
        Test variable (NameError)
        """
        self.data_in = {"foo": "bar"}
        self.query = 'variable'
        self.assertRaises(NameError, jello.cli.pyquery, self.data_in, self.query)

    def test_ValueError(self):
        """
        Test _.get (ValueError)
        """
        self.data_in = {"foo": "bar"}
        self.query = '_.get'
        self.assertRaises(ValueError, jello.cli.pyquery, self.data_in, self.query)


if __name__ == '__main__':
    unittest.main()
