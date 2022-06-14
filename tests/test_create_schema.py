#!/usr/bin/env python3

import unittest
import os
from jello.lib import opts, Schema


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
        opts.types = None
        opts.keyname_color = None
        opts.keyword_color = None
        opts.number_color = None
        opts.string_color = None

        # initialize schema_lists
        self.schema = Schema()

        # initialize JELLO_COLORS env variable
        os.environ['JELLO_COLORS'] = 'default,default,default,default'

        # set the colors
        self.schema.set_colors()

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

        self.dict_space_keys_nest_sample = {
            'string with spaces': 'string\nwith newline\ncharacters in it',
            'foo': {
                "another with spaces": {
                    "nested": {
                        "nested space": True
                    }
                }
            },
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

        self.deep_nest_sample = [[[[{"foo":[[[[1,2,3]]]]}]]]]

    # ------------ Tests ------------

    #
    # Naked True
    #

    def test_true(self):
        """
        Test True
        """
        data_in = True
        expected = '\x1b[34;01m_\x1b[39;00m = \x1b[90mtrue\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_true_m(self):
        """
        Test True -m
        """
        data_in = True
        expected = '_ = true;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # Naked False
    #

    def test_false(self):
        """
        Test False
        """
        data_in = False
        expected = '\x1b[34;01m_\x1b[39;00m = \x1b[90mfalse\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_false_m(self):
        """
        Test False -m
        """
        data_in = False
        expected = '_ = false;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # Naked null
    #

    def test_null(self):
        """
        Test None
        """
        data_in = None
        expected = '\x1b[34;01m_\x1b[39;00m = \x1b[90mnull\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_null_m(self):
        """
        Test None -m
        """
        data_in = None
        expected = '_ = null;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # naked int
    #

    def test_int(self):
        """
        Test int
        """
        data_in = 42
        expected = '\x1b[34;01m_\x1b[39;00m = \x1b[35m42\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_int_m(self):
        """
        Test int -m
        """
        data_in = 42
        expected = '_ = 42;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # naked float
    #

    def test_float(self):
        """
        Test float
        """
        data_in = 3.14
        expected = '\x1b[34;01m_\x1b[39;00m = \x1b[35m3.14\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_float_m(self):
        """
        Test float -m
        """
        data_in = 3.14
        expected = '_ = 3.14;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # naked string
    #

    def test_string(self):
        """
        Test string
        """
        data_in = '"string with\\nnewline char"'
        expected = '\x1b[34;01m_\x1b[39;00m = \x1b[32m"\\"string with\\\\nnewline char\\""\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_string_m(self):
        """
        Test string -m
        """
        data_in = '"string with\\nnewline char"'
        expected = '_ = "\\"string with\\\\nnewline char\\"";'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # Naked Dict
    #

    def test_dict(self):
        """
        Test self.dict_sample
        """
        data_in = self.dict_sample
        expected = '\x1b[34;01m_\x1b[39;00m = {};\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01mstring\x1b[39;00m = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[90mtrue\x1b[39m = \x1b[90mtrue\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[90mfalse\x1b[39m = \x1b[90mfalse\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[90mnull\x1b[39m = \x1b[90mnull\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[90mint\x1b[39m = \x1b[35m42\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[90mfloat\x1b[39m = \x1b[35m3.14\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m0\x1b[39m] = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m1\x1b[39m] = \x1b[90mtrue\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m2\x1b[39m] = \x1b[90mfalse\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m3\x1b[39m] = \x1b[90mnull\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m4\x1b[39m] = \x1b[35m42\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m5\x1b[39m] = \x1b[35m3.14\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_dict_t(self):
        """
        Test self.dict_sample -t
        """
        opts.types = True
        data_in = self.dict_sample
        expected = '\x1b[34;01m_\x1b[39;00m = {};                                                             //  (object)\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01mstring\x1b[39;00m = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[39m;                //  (string)\n\x1b[34;01m_\x1b[39;00m.\x1b[90mtrue\x1b[39m = \x1b[90mtrue\x1b[39m;                                                      // (boolean)\n\x1b[34;01m_\x1b[39;00m.\x1b[90mfalse\x1b[39m = \x1b[90mfalse\x1b[39m;                                                    // (boolean)\n\x1b[34;01m_\x1b[39;00m.\x1b[90mnull\x1b[39m = \x1b[90mnull\x1b[39m;                                                      //    (null)\n\x1b[34;01m_\x1b[39;00m.\x1b[90mint\x1b[39m = \x1b[35m42\x1b[39m;                                                         //  (number)\n\x1b[34;01m_\x1b[39;00m.\x1b[90mfloat\x1b[39m = \x1b[35m3.14\x1b[39m;                                                     //  (number)\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m = [];                                                       //   (array)\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m0\x1b[39m] = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[39m;              //  (string)\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m1\x1b[39m] = \x1b[90mtrue\x1b[39m;                                                  // (boolean)\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m2\x1b[39m] = \x1b[90mfalse\x1b[39m;                                                 // (boolean)\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m3\x1b[39m] = \x1b[90mnull\x1b[39m;                                                  //    (null)\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m4\x1b[39m] = \x1b[35m42\x1b[39m;                                                    //  (number)\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m5\x1b[39m] = \x1b[35m3.14\x1b[39m;                                                  //  (number)'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_dict_m(self):
        """
        Test self.dict_sample -m
        """
        data_in = self.dict_sample
        expected = '_ = {};\n_.string = "string\\nwith newline\\ncharacters in it";\n_.true = true;\n_.false = false;\n_.null = null;\n_.int = 42;\n_.float = 3.14;\n_.array = [];\n_.array[0] = "string\\nwith newline\\ncharacters in it";\n_.array[1] = true;\n_.array[2] = false;\n_.array[3] = null;\n_.array[4] = 42;\n_.array[5] = 3.14;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    def test_dict_mt(self):
        """
        Test self.dict_sample -mt
        """
        opts.types = True
        data_in = self.dict_sample
        expected = '_ = {};                                                             //  (object)\n_.string = "string\\nwith newline\\ncharacters in it";                //  (string)\n_.true = true;                                                      // (boolean)\n_.false = false;                                                    // (boolean)\n_.null = null;                                                      //    (null)\n_.int = 42;                                                         //  (number)\n_.float = 3.14;                                                     //  (number)\n_.array = [];                                                       //   (array)\n_.array[0] = "string\\nwith newline\\ncharacters in it";              //  (string)\n_.array[1] = true;                                                  // (boolean)\n_.array[2] = false;                                                 // (boolean)\n_.array[3] = null;                                                  //    (null)\n_.array[4] = 42;                                                    //  (number)\n_.array[5] = 3.14;                                                  //  (number)'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # true in a list
    #

    def test_list_true(self):
        """
        Test [True]
        """
        data_in = [True]
        expected = '\x1b[34;01m_\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m] = \x1b[90mtrue\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_list_true_m(self):
        """
        Test [True] -m
        """
        data_in = [True]
        expected = '_ = [];\n_[0] = true;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # false in a list
    #

    def test_list_false(self):
        """
        Test [False]
        """
        data_in = [False]
        expected = '\x1b[34;01m_\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m] = \x1b[90mfalse\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_list_false_m(self):
        """
        Test [False] -m
        """
        data_in = [False]
        expected = '_ = [];\n_[0] = false;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # null in a list
    #

    def test_list_null(self):
        """
        Test [None]
        """
        data_in = [None]
        expected = '\x1b[34;01m_\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m] = \x1b[90mnull\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_list_null_m(self):
        """
        Test [None] -m
        """
        data_in = [None]
        expected = '_ = [];\n_[0] = null;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # Int in a list
    #

    def test_list_int(self):
        """
        Test [42]
        """
        data_in = [42]
        expected = '\x1b[34;01m_\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m] = \x1b[35m42\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_list_int_m(self):
        """
        Test [42] -m
        """
        data_in = [42]
        expected = '_ = [];\n_[0] = 42;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # Float in a list
    #

    def test_list_float(self):
        """
        Test [3.14]
        """
        data_in = [3.14]
        expected = '\x1b[34;01m_\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m] = \x1b[35m3.14\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_list_float_m(self):
        """
        Test [3.14] -m
        """
        data_in = [3.14]
        expected = '_ = [];\n_[0] = 3.14;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # String in a list
    #

    def test_list_str(self):
        """
        Test ['string with spaces\nand newline\ncharacters']
        """
        data_in = ['string with spaces\nand newline\ncharacters']
        expected = '\x1b[34;01m_\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m] = \x1b[32m"string with spaces\\nand newline\\ncharacters"\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_list_str_m(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -m
        """
        data_in = ['string with spaces\nand newline\ncharacters']
        expected = '_ = [];\n_[0] = "string with spaces\\nand newline\\ncharacters";'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # List with different types of elements
    #

    def test_list_sample(self):
        """
        Test self.list_sample
        """
        data_in = self.list_sample
        expected = '\x1b[34;01m_\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m] = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m] = \x1b[90mtrue\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m2\x1b[39m] = \x1b[90mfalse\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m3\x1b[39m] = \x1b[90mnull\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m4\x1b[39m] = \x1b[35m42\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m5\x1b[39m] = \x1b[35m3.14\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_list_sample_m(self):
        """
        Test self.list_sample -m
        """
        data_in = self.list_sample
        expected = '_ = [];\n_[0] = "string\\nwith newline\\ncharacters in it";\n_[1] = true;\n_[2] = false;\n_[3] = null;\n_[4] = 42;\n_[5] = 3.14;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # Dicts in a list
    #

    def test_list_dict(self):
        """
        Test self.list_of_dicts_sample
        """
        data_in = self.list_of_dicts_sample
        expected = '\x1b[34;01m_\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m] = {};\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m].\x1b[34;01mstring\x1b[39;00m = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m].\x1b[90mtrue\x1b[39m = \x1b[90mtrue\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m].\x1b[90mfalse\x1b[39m = \x1b[90mfalse\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m].\x1b[90mnull\x1b[39m = \x1b[90mnull\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m].\x1b[90mint\x1b[39m = \x1b[35m42\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m].\x1b[90mfloat\x1b[39m = \x1b[35m3.14\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m].\x1b[34;01marray\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m].\x1b[34;01marray\x1b[39;00m[\x1b[35m0\x1b[39m] = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m].\x1b[34;01marray\x1b[39;00m[\x1b[35m1\x1b[39m] = \x1b[90mtrue\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m].\x1b[34;01marray\x1b[39;00m[\x1b[35m2\x1b[39m] = \x1b[90mfalse\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m].\x1b[34;01marray\x1b[39;00m[\x1b[35m3\x1b[39m] = \x1b[90mnull\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m].\x1b[34;01marray\x1b[39;00m[\x1b[35m4\x1b[39m] = \x1b[35m42\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m].\x1b[34;01marray\x1b[39;00m[\x1b[35m5\x1b[39m] = \x1b[35m3.14\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m] = {};\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m].\x1b[34;01mstring\x1b[39;00m = \x1b[32m"another string\\nwith newline\\ncharacters in it"\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m].\x1b[90mtrue\x1b[39m = \x1b[90mtrue\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m].\x1b[90mfalse\x1b[39m = \x1b[90mfalse\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m].\x1b[90mnull\x1b[39m = \x1b[90mnull\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m].\x1b[90mint\x1b[39m = \x1b[35m10001\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m].\x1b[90mfloat\x1b[39m = -\x1b[35m400.45\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m].\x1b[34;01marray\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m].\x1b[34;01marray\x1b[39;00m[\x1b[35m0\x1b[39m] = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m].\x1b[34;01marray\x1b[39;00m[\x1b[35m1\x1b[39m] = \x1b[90mtrue\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m].\x1b[34;01marray\x1b[39;00m[\x1b[35m2\x1b[39m] = \x1b[90mfalse\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m].\x1b[34;01marray\x1b[39;00m[\x1b[35m3\x1b[39m] = \x1b[90mnull\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m].\x1b[34;01marray\x1b[39;00m[\x1b[35m4\x1b[39m] = -\x1b[35m6000034\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m].\x1b[34;01marray\x1b[39;00m[\x1b[35m5\x1b[39m] = \x1b[35m999999.854321\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_list_dict_m(self):
        """
        Test self.list_of_dicts_sample -m
        """
        data_in = self.list_of_dicts_sample
        expected = '_ = [];\n_[0] = {};\n_[0].string = "string\\nwith newline\\ncharacters in it";\n_[0].true = true;\n_[0].false = false;\n_[0].null = null;\n_[0].int = 42;\n_[0].float = 3.14;\n_[0].array = [];\n_[0].array[0] = "string\\nwith newline\\ncharacters in it";\n_[0].array[1] = true;\n_[0].array[2] = false;\n_[0].array[3] = null;\n_[0].array[4] = 42;\n_[0].array[5] = 3.14;\n_[1] = {};\n_[1].string = "another string\\nwith newline\\ncharacters in it";\n_[1].true = true;\n_[1].false = false;\n_[1].null = null;\n_[1].int = 10001;\n_[1].float = -400.45;\n_[1].array = [];\n_[1].array[0] = "string\\nwith newline\\ncharacters in it";\n_[1].array[1] = true;\n_[1].array[2] = false;\n_[1].array[3] = null;\n_[1].array[4] = -6000034;\n_[1].array[5] = 999999.854321;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # lists in list
    #

    def test_list_list(self):
        """
        Test self.list_of_lists_sample
        """
        data_in = self.list_of_lists_sample
        expected = '\x1b[34;01m_\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m] = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m] = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m1\x1b[39m] = \x1b[90mtrue\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m2\x1b[39m] = \x1b[90mfalse\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m3\x1b[39m] = \x1b[90mnull\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m4\x1b[39m] = \x1b[35m42\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m5\x1b[39m] = \x1b[35m3.14\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m] = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m][\x1b[35m0\x1b[39m] = \x1b[32m"another string\\nwith newline\\ncharacters in it"\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m][\x1b[35m1\x1b[39m] = \x1b[90mtrue\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m][\x1b[35m2\x1b[39m] = \x1b[90mfalse\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m][\x1b[35m3\x1b[39m] = \x1b[90mnull\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m][\x1b[35m4\x1b[39m] = \x1b[35m42001\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m1\x1b[39m][\x1b[35m5\x1b[39m] = -\x1b[35m3.14\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_list_list_m(self):
        """
        Test self.list_of_lists_sample -m
        """
        data_in = self.list_of_lists_sample
        expected = '_ = [];\n_[0] = [];\n_[0][0] = "string\\nwith newline\\ncharacters in it";\n_[0][1] = true;\n_[0][2] = false;\n_[0][3] = null;\n_[0][4] = 42;\n_[0][5] = 3.14;\n_[1] = [];\n_[1][0] = "another string\\nwith newline\\ncharacters in it";\n_[1][1] = true;\n_[1][2] = false;\n_[1][3] = null;\n_[1][4] = 42001;\n_[1][5] = -3.14;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    #
    # deep nest
    #

    def test_dict_space_keys_nest(self):
        """
        Test self.dict_space_keys_nest_sample
        """
        data_in = self.dict_space_keys_nest_sample
        expected = '\x1b[34;01m_\x1b[39;00m = {};\n\x1b[34;01m_\x1b[39;00m[\x1b[32m"string with spaces"\x1b[39m] = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01mfoo\x1b[39;00m = {};\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01mfoo\x1b[39;00m[\x1b[32m"another with spaces"\x1b[39m] = {};\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01mfoo\x1b[39;00m[\x1b[32m"another with spaces"\x1b[39m].\x1b[34;01mnested\x1b[39;00m = {};\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01mfoo\x1b[39;00m[\x1b[32m"another with spaces"\x1b[39m].\x1b[34;01mnested\x1b[39;00m[\x1b[32m"nested space"\x1b[39m] = \x1b[90mtrue\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[90mtrue\x1b[39m = \x1b[90mtrue\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[90mfalse\x1b[39m = \x1b[90mfalse\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[90mnull\x1b[39m = \x1b[90mnull\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[90mint\x1b[39m = \x1b[35m42\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[90mfloat\x1b[39m = \x1b[35m3.14\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m0\x1b[39m] = \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m1\x1b[39m] = \x1b[90mtrue\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m2\x1b[39m] = \x1b[90mfalse\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m3\x1b[39m] = \x1b[90mnull\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m4\x1b[39m] = \x1b[35m42\x1b[39m;\n\x1b[34;01m_\x1b[39;00m.\x1b[34;01marray\x1b[39;00m[\x1b[35m5\x1b[39m] = \x1b[35m3.14\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_dict_space_keys_nest_m(self):
        """
        Test self.dict_space_keys_nest_sample -m
        """
        data_in = self.dict_space_keys_nest_sample
        expected = '_ = {};\n_["string with spaces"] = "string\\nwith newline\\ncharacters in it";\n_.foo = {};\n_.foo["another with spaces"] = {};\n_.foo["another with spaces"].nested = {};\n_.foo["another with spaces"].nested["nested space"] = true;\n_.true = true;\n_.false = false;\n_.null = null;\n_.int = 42;\n_.float = 3.14;\n_.array = [];\n_.array[0] = "string\\nwith newline\\ncharacters in it";\n_.array[1] = true;\n_.array[2] = false;\n_.array[3] = null;\n_.array[4] = 42;\n_.array[5] = 3.14;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

    def test_deep_nest(self):
        """
        Test self.deep_nest_sample
        """
        data_in = self.deep_nest_sample
        expected = '\x1b[34;01m_\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m] = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m] = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m] = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m] = {};\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m].\x1b[34;01mfoo\x1b[39;00m = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m].\x1b[34;01mfoo\x1b[39;00m[\x1b[35m0\x1b[39m] = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m].\x1b[34;01mfoo\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m] = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m].\x1b[34;01mfoo\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m] = [];\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m].\x1b[34;01mfoo\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m] = \x1b[35m1\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m].\x1b[34;01mfoo\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m1\x1b[39m] = \x1b[35m2\x1b[39m;\n\x1b[34;01m_\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m].\x1b[34;01mfoo\x1b[39;00m[\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m0\x1b[39m][\x1b[35m2\x1b[39m] = \x1b[35m3\x1b[39m;'
        output = self.schema.create_schema(data_in)
        self.assertEqual(self.schema.color_output(output), expected)

    def test_deep_nest_m(self):
        """
        Test self.deep_nest_sample -m
        """
        data_in = self.deep_nest_sample
        expected = '_ = [];\n_[0] = [];\n_[0][0] = [];\n_[0][0][0] = [];\n_[0][0][0][0] = {};\n_[0][0][0][0].foo = [];\n_[0][0][0][0].foo[0] = [];\n_[0][0][0][0].foo[0][0] = [];\n_[0][0][0][0].foo[0][0][0] = [];\n_[0][0][0][0].foo[0][0][0][0] = 1;\n_[0][0][0][0].foo[0][0][0][1] = 2;\n_[0][0][0][0].foo[0][0][0][2] = 3;'
        self.assertEqual(self.schema.create_schema(data_in), expected)

if __name__ == '__main__':
    unittest.main()
