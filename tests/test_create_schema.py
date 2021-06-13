#!/usr/bin/env python3

import unittest
import os
from jello.lib import opts, JelloTheme, Schema


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

        # initialize schema_list
        self.schema = Schema()

        # initialize JELLO_COLORS env variable
        os.environ['JELLO_COLORS'] = 'default,default,default,default,default,default'

        # set the colors
        self.jello_theme = JelloTheme()
        self.jello_theme.set_colors()

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

    #
    # Naked True
    #

    def test_true(self):
        """
        Test True
        """
        self.data_in = True
        self.expected = '. = \x1b[90mtrue\x1b[0m;'
        self.schema.create_schema(self.data_in)
        self.assertEqual('\n'.join(self.schema.schema_list), self.expected)

    def test_true_m(self):
        """
        Test True -m
        """
        self.data_in = True
        self.expected = '. = true;'
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual('\n'.join(self.schema.schema_list), self.expected)

    #
    # Naked False
    #

    def test_false(self):
        """
        Test False
        """
        self.data_in = False
        self.expected = '. = \x1b[90mfalse\x1b[0m;'
        self.schema.create_schema(self.data_in)
        self.assertEqual('\n'.join(self.schema.schema_list), self.expected)

    def test_false_m(self):
        """
        Test False -m
        """
        self.data_in = False
        self.expected = '. = false;'
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual('\n'.join(self.schema.schema_list), self.expected)

    #
    # Naked null
    #

    def test_null(self):
        """
        Test None
        """
        self.data_in = None
        self.expected = '. = \x1b[90mnull\x1b[0m;'
        self.schema.create_schema(self.data_in)
        self.assertEqual('\n'.join(self.schema.schema_list), self.expected)

    def test_null_m(self):
        """
        Test None -m
        """
        self.data_in = None
        self.expected = '. = null;'
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual('\n'.join(self.schema.schema_list), self.expected)

    #
    # naked int
    #

    def test_int(self):
        """
        Test int
        """
        self.data_in = 42
        self.expected = '. = \x1b[35m42\x1b[0m;'
        self.schema.create_schema(self.data_in)
        self.assertEqual('\n'.join(self.schema.schema_list), self.expected)

    def test_int_m(self):
        """
        Test int -m
        """
        self.data_in = 42
        self.expected = '. = 42;'
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual('\n'.join(self.schema.schema_list), self.expected)

    #
    # naked float
    #

    def test_float(self):
        """
        Test float
        """
        self.data_in = 3.14
        self.expected = '. = \x1b[35m3.14\x1b[0m;'
        self.schema.create_schema(self.data_in)
        self.assertEqual('\n'.join(self.schema.schema_list), self.expected)

    def test_float_m(self):
        """
        Test float -m
        """
        self.data_in = 3.14
        self.expected = '. = 3.14;'
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual('\n'.join(self.schema.schema_list), self.expected)

    #
    # naked string
    #

    def test_string(self):
        """
        Test string
        """
        self.data_in = '"string with\\nnewline char"'
        self.expected = '. = \x1b[32m"\\"string with\\\\nnewline char\\""\x1b[0m;'
        self.schema.create_schema(self.data_in)
        self.assertEqual('\n'.join(self.schema.schema_list), self.expected)

    def test_string_m(self):
        """
        Test string -m
        """
        self.data_in = '"string with\\nnewline char"'
        self.expected = '. = "\\"string with\\\\nnewline char\\"";'
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual('\n'.join(self.schema.schema_list), self.expected)

    #
    # Naked Dict
    #

    def test_dict(self):
        """
        Test self.dict_sample
        """
        self.data_in = self.dict_sample
        self.expected = ['.\x1b[1m\x1b[34mstring\x1b[0m = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[0m;', '.\x1b[1m\x1b[34mtrue\x1b[0m = \x1b[90mtrue\x1b[0m;', '.\x1b[1m\x1b[34mfalse\x1b[0m = \x1b[90mfalse\x1b[0m;', '.\x1b[1m\x1b[34mnull\x1b[0m = \x1b[90mnull\x1b[0m;', '.\x1b[1m\x1b[34mint\x1b[0m = \x1b[35m42\x1b[0m;', '.\x1b[1m\x1b[34mfloat\x1b[0m = \x1b[35m3.14\x1b[0m;', '.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[0m;', '.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mtrue\x1b[0m;', '.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m2\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mfalse\x1b[0m;', '.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m3\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mnull\x1b[0m;', '.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m4\x1b[0m\x1b[35m]\x1b[0m = \x1b[35m42\x1b[0m;', '.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m5\x1b[0m\x1b[35m]\x1b[0m = \x1b[35m3.14\x1b[0m;']
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    def test_dict_m(self):
        """
        Test self.dict_sample -m
        """
        self.data_in = self.dict_sample
        self.expected = ['.string = "string\\nwith newline\\ncharacters in it";', '.true = true;', '.false = false;', '.null = null;', '.int = 42;', '.float = 3.14;', '.array[0] = "string\\nwith newline\\ncharacters in it";', '.array[1] = true;', '.array[2] = false;', '.array[3] = null;', '.array[4] = 42;', '.array[5] = 3.14;']
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    #
    # true in a list
    #

    def test_list_true(self):
        """
        Test [True]
        """
        self.data_in = [True]
        self.expected = ['.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mtrue\x1b[0m;']
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    def test_list_true_m(self):
        """
        Test [True] -m
        """
        self.data_in = [True]
        self.expected = ['.[0] = true;']
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    #
    # false in a list
    #

    def test_list_false(self):
        """
        Test [False]
        """
        self.data_in = [False]
        self.expected = ['.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mfalse\x1b[0m;']
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    def test_list_false_m(self):
        """
        Test [False] -m
        """
        self.data_in = [False]
        self.expected = ['.[0] = false;']
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    #
    # null in a list
    #

    def test_list_null(self):
        """
        Test [None]
        """
        self.data_in = [None]
        self.expected = ['.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mnull\x1b[0m;']
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    def test_list_null_m(self):
        """
        Test [None] -m
        """
        self.data_in = [None]
        self.expected = ['.[0] = null;']
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    #
    # Int in a list
    #

    def test_list_int(self):
        """
        Test [42]
        """
        self.data_in = [42]
        self.expected = ['.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m = \x1b[35m42\x1b[0m;']
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    def test_list_int_m(self):
        """
        Test [42] -m
        """
        self.data_in = [42]
        self.expected = ['.[0] = 42;']
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    #
    # Float in a list
    #

    def test_list_float(self):
        """
        Test [3.14]
        """
        self.data_in = [3.14]
        self.expected = ['.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m = \x1b[35m3.14\x1b[0m;']
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    def test_list_float_m(self):
        """
        Test [3.14] -m
        """
        self.data_in = [3.14]
        self.expected = ['.[0] = 3.14;']
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    #
    # String in a list
    #

    def test_list_str(self):
        """
        Test ['string with spaces\nand newline\ncharacters']
        """
        self.data_in = ['string with spaces\nand newline\ncharacters']
        self.expected = ['.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m = \x1b[32m"string with spaces\\nand newline\\ncharacters"\x1b[0m;']
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    def test_list_str_m(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -m
        """
        self.data_in = ['string with spaces\nand newline\ncharacters']
        self.expected = ['.[0] = "string with spaces\\nand newline\\ncharacters";']
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    #
    # List with different types of elements
    #

    def test_list_sample(self):
        """
        Test self.list_sample
        """
        self.data_in = self.list_sample
        self.expected = ['.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mtrue\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m2\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mfalse\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m3\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mnull\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m4\x1b[0m\x1b[35m]\x1b[0m = \x1b[35m42\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m5\x1b[0m\x1b[35m]\x1b[0m = \x1b[35m3.14\x1b[0m;']
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    def test_list_sample_m(self):
        """
        Test self.list_sample -m
        """
        self.data_in = self.list_sample
        self.expected = ['.[0] = "string\\nwith newline\\ncharacters in it";', '.[1] = true;', '.[2] = false;', '.[3] = null;', '.[4] = 42;', '.[5] = 3.14;']
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    #
    # Dicts in a list
    #

    def test_list_dict(self):
        """
        Test self.list_of_dicts_sample
        """
        self.data_in = self.list_of_dicts_sample
        self.expected = ['.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34mstring\x1b[0m = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34mtrue\x1b[0m = \x1b[90mtrue\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34mfalse\x1b[0m = \x1b[90mfalse\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34mnull\x1b[0m = \x1b[90mnull\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34mint\x1b[0m = \x1b[35m42\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34mfloat\x1b[0m = \x1b[35m3.14\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mtrue\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m2\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mfalse\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m3\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mnull\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m4\x1b[0m\x1b[35m]\x1b[0m = \x1b[35m42\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m5\x1b[0m\x1b[35m]\x1b[0m = \x1b[35m3.14\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34mstring\x1b[0m = \x1b[32m"another string\\nwith newline\\ncharacters in it"\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34mtrue\x1b[0m = \x1b[90mtrue\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34mfalse\x1b[0m = \x1b[90mfalse\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34mnull\x1b[0m = \x1b[90mnull\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34mint\x1b[0m = \x1b[35m10001\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34mfloat\x1b[0m = \x1b[32m-400.45\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mtrue\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m2\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mfalse\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m3\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mnull\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m4\x1b[0m\x1b[35m]\x1b[0m = \x1b[32m-6000034\x1b[0m;', '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34marray\x1b[0m\x1b[35m[\x1b[0m\x1b[31m5\x1b[0m\x1b[35m]\x1b[0m = \x1b[35m999999.854321\x1b[0m;']
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    def test_list_dict_m(self):
        """
        Test self.list_of_dicts_sample -m
        """
        self.data_in = self.list_of_dicts_sample
        self.expected = ['.[0].string = "string\\nwith newline\\ncharacters in it";', '.[0].true = true;', '.[0].false = false;', '.[0].null = null;', '.[0].int = 42;', '.[0].float = 3.14;', '.[0].array[0] = "string\\nwith newline\\ncharacters in it";', '.[0].array[1] = true;', '.[0].array[2] = false;', '.[0].array[3] = null;', '.[0].array[4] = 42;', '.[0].array[5] = 3.14;', '.[1].string = "another string\\nwith newline\\ncharacters in it";', '.[1].true = true;', '.[1].false = false;', '.[1].null = null;', '.[1].int = 10001;', '.[1].float = -400.45;', '.[1].array[0] = "string\\nwith newline\\ncharacters in it";', '.[1].array[1] = true;', '.[1].array[2] = false;', '.[1].array[3] = null;', '.[1].array[4] = -6000034;', '.[1].array[5] = 999999.854321;']
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    #
    # lists in list
    #

    def test_list_list(self):
        """
        Test self.list_of_lists_sample
        """
        self.data_in = self.list_of_lists_sample
        self.expected = ['.\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34m[\'string\\nwith newline\\ncharacters in it\', True, False, None, 42, 3.14]\x1b[0m\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[0m;', ".\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34m['string\\nwith newline\\ncharacters in it', True, False, None, 42, 3.14]\x1b[0m\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mtrue\x1b[0m;", ".\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34m['string\\nwith newline\\ncharacters in it', True, False, None, 42, 3.14]\x1b[0m\x1b[35m[\x1b[0m\x1b[31m2\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mfalse\x1b[0m;", ".\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34m['string\\nwith newline\\ncharacters in it', True, False, None, 42, 3.14]\x1b[0m\x1b[35m[\x1b[0m\x1b[31m3\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mnull\x1b[0m;", ".\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34m['string\\nwith newline\\ncharacters in it', True, False, None, 42, 3.14]\x1b[0m\x1b[35m[\x1b[0m\x1b[31m4\x1b[0m\x1b[35m]\x1b[0m = \x1b[35m42\x1b[0m;", ".\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34m['string\\nwith newline\\ncharacters in it', True, False, None, 42, 3.14]\x1b[0m\x1b[35m[\x1b[0m\x1b[31m5\x1b[0m\x1b[35m]\x1b[0m = \x1b[35m3.14\x1b[0m;", '.\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34m[\'another string\\nwith newline\\ncharacters in it\', True, False, None, 42001, -3.14]\x1b[0m\x1b[35m[\x1b[0m\x1b[31m0\x1b[0m\x1b[35m]\x1b[0m = \x1b[32m"another string\\nwith newline\\ncharacters in it"\x1b[0m;', ".\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34m['another string\\nwith newline\\ncharacters in it', True, False, None, 42001, -3.14]\x1b[0m\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mtrue\x1b[0m;", ".\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34m['another string\\nwith newline\\ncharacters in it', True, False, None, 42001, -3.14]\x1b[0m\x1b[35m[\x1b[0m\x1b[31m2\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mfalse\x1b[0m;", ".\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34m['another string\\nwith newline\\ncharacters in it', True, False, None, 42001, -3.14]\x1b[0m\x1b[35m[\x1b[0m\x1b[31m3\x1b[0m\x1b[35m]\x1b[0m = \x1b[90mnull\x1b[0m;", ".\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34m['another string\\nwith newline\\ncharacters in it', True, False, None, 42001, -3.14]\x1b[0m\x1b[35m[\x1b[0m\x1b[31m4\x1b[0m\x1b[35m]\x1b[0m = \x1b[35m42001\x1b[0m;", ".\x1b[35m[\x1b[0m\x1b[31m1\x1b[0m\x1b[35m]\x1b[0m.\x1b[1m\x1b[34m['another string\\nwith newline\\ncharacters in it', True, False, None, 42001, -3.14]\x1b[0m\x1b[35m[\x1b[0m\x1b[31m5\x1b[0m\x1b[35m]\x1b[0m = \x1b[32m-3.14\x1b[0m;"]
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)

    def test_list_list_m(self):
        """
        Test self.list_of_lists_sample -m
        """
        self.data_in = self.list_of_lists_sample
        self.expected = ['.[0].[\'string\\nwith newline\\ncharacters in it\', True, False, None, 42, 3.14][0] = "string\\nwith newline\\ncharacters in it";', ".[0].['string\\nwith newline\\ncharacters in it', True, False, None, 42, 3.14][1] = true;", ".[0].['string\\nwith newline\\ncharacters in it', True, False, None, 42, 3.14][2] = false;", ".[0].['string\\nwith newline\\ncharacters in it', True, False, None, 42, 3.14][3] = null;", ".[0].['string\\nwith newline\\ncharacters in it', True, False, None, 42, 3.14][4] = 42;", ".[0].['string\\nwith newline\\ncharacters in it', True, False, None, 42, 3.14][5] = 3.14;", '.[1].[\'another string\\nwith newline\\ncharacters in it\', True, False, None, 42001, -3.14][0] = "another string\\nwith newline\\ncharacters in it";', ".[1].['another string\\nwith newline\\ncharacters in it', True, False, None, 42001, -3.14][1] = true;", ".[1].['another string\\nwith newline\\ncharacters in it', True, False, None, 42001, -3.14][2] = false;", ".[1].['another string\\nwith newline\\ncharacters in it', True, False, None, 42001, -3.14][3] = null;", ".[1].['another string\\nwith newline\\ncharacters in it', True, False, None, 42001, -3.14][4] = 42001;", ".[1].['another string\\nwith newline\\ncharacters in it', True, False, None, 42001, -3.14][5] = -3.14;"]
        opts.mono = True
        self.schema.create_schema(self.data_in)
        self.assertEqual(self.schema.schema_list, self.expected)


if __name__ == '__main__':
    unittest.main()
