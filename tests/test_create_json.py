#!/usr/bin/env python3

import unittest
import jello.cli


class MyTests(unittest.TestCase):
    def setUp(self):
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
        self.expected = 'true'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_true_r(self):
        """
        Test True -r
        """
        self.data_in = True
        self.expected = 'true'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_true_l(self):
        """
        Test True -l
        """
        self.data_in = True
        self.expected = 'true'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_true_rl(self):
        """
        Test True -rl
        """
        self.data_in = True
        self.expected = 'true'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, lines=True), self.expected)

    #
    # Naked False
    #

    def test_false(self):
        """
        Test False
        """
        self.data_in = False
        self.expected = 'false'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_false_r(self):
        """
        Test False -r
        """
        self.data_in = False
        self.expected = 'false'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_false_l(self):
        """
        Test False -l
        """
        self.data_in = False
        self.expected = 'false'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_false_rl(self):
        """
        Test False -rl
        """
        self.data_in = False
        self.expected = 'false'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, lines=True), self.expected)

    #
    # Naked null
    #

    def test_null(self):
        """
        Test None
        """
        self.data_in = None
        self.expected = ''
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_null_n(self):
        """
        Test None with -n
        """
        self.data_in = None
        self.expected = 'null'
        self.assertEqual(jello.cli.create_json(self.data_in, nulls=True), self.expected)

    def test_null_r(self):
        """
        Test None with -r
        """
        self.data_in = None
        self.expected = ''
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_null_rl(self):
        """
        Test None with -rl
        """
        self.data_in = None
        self.expected = ''
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, lines=True), self.expected)

    def test_null_rln(self):
        """
        Test None with -rln
        """
        self.data_in = None
        self.expected = 'null'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, lines=True, nulls=True), self.expected)

    #
    # naked int
    #

    def test_int(self):
        """
        Test int
        """
        self.data_in = 42
        self.expected = '42'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_int_r(self):
        """
        Test int -r
        """
        self.data_in = 42
        self.expected = '42'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_int_l(self):
        """
        Test int -l
        """
        self.data_in = 42
        self.expected = '42'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_int_rl(self):
        """
        Test int -rl
        """
        self.data_in = 42
        self.expected = '42'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, lines=True), self.expected)

    #
    # naked float
    #

    def test_float(self):
        """
        Test float
        """
        self.data_in = 3.14
        self.expected = '3.14'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_float_r(self):
        """
        Test float -r
        """
        self.data_in = 3.14
        self.expected = '3.14'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_float_l(self):
        """
        Test float -l
        """
        self.data_in = 3.14
        self.expected = '3.14'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_float_rl(self):
        """
        Test float -rl
        """
        self.data_in = 3.14
        self.expected = '3.14'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, lines=True), self.expected)

    #
    # naked string
    #

    def test_string(self):
        """
        Test "string with\nnewline char"
        """
        self.data_in = '"string with\nnewline char"'
        self.expected = '""string with\\nnewline char""'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_string_r(self):
        """
        Test "string with\nnewline char" -r
        """
        self.data_in = '"string with\nnewline char"'
        self.expected = '"string with\\nnewline char"'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_string_l(self):
        """
        Test "string with\nnewline char" -l
        """
        self.data_in = '"string with\nnewline char"'
        self.expected = '""string with\\nnewline char""'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_string_rl(self):
        """
        Test "string with\nnewline char" -rl
        """
        self.data_in = '"string with\nnewline char"'
        self.expected = '"string with\\nnewline char"'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, lines=True), self.expected)

    #
    # Naked Dict
    #

    def test_dict(self):
        """
        Test self.dict_sample
        """
        self.data_in = self.dict_sample
        self.expected = '{\n  "string": "string\\nwith newline\\ncharacters in it",\n  "true": true,\n  "false": false,\n  "null": null,\n  "int": 42,\n  "float": 3.14,\n  "array": [\n    "string\\nwith newline\\ncharacters in it",\n    true,\n    false,\n    null,\n    42,\n    3.14\n  ]\n}'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_dict_r(self):
        """
        Test self.dict_sample -r
        """
        self.data_in = self.dict_sample
        self.expected = '{\n  "string": "string\\nwith newline\\ncharacters in it",\n  "true": true,\n  "false": false,\n  "null": null,\n  "int": 42,\n  "float": 3.14,\n  "array": [\n    "string\\nwith newline\\ncharacters in it",\n    true,\n    false,\n    null,\n    42,\n    3.14\n  ]\n}'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_dict_l(self):
        """
        Test self.dict_sample -l
        """
        self.data_in = self.dict_sample
        self.expected = '{"string": "string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 42, "float": 3.14, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]}'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_dict_c(self):
        """
        Test self.dict_sample -c
        """
        self.data_in = self.dict_sample
        self.expected = '{"string": "string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 42, "float": 3.14, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]}'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_dict_rl(self):
        """
        Test self.dict_sample -rl
        """
        self.data_in = self.dict_sample
        self.expected = '{"string": "string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 42, "float": 3.14, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]}'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, lines=True), self.expected)

    def test_dict_cl(self):
        """
        Test self.dict_sample -cl
        """
        self.data_in = self.dict_sample
        self.expected = '{"string": "string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 42, "float": 3.14, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]}'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, lines=True), self.expected)

    def test_dict_cr(self):
        """
        Test self.dict_sample -cr
        """
        self.data_in = self.dict_sample
        self.expected = '{"string": "string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 42, "float": 3.14, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]}'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, raw=True), self.expected)

    def test_dict_crl(self):
        """
        Test self.dict_sample -crl
        """
        self.data_in = self.dict_sample
        self.expected = '{"string": "string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 42, "float": 3.14, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]}'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, raw=True, lines=True), self.expected)

    #
    # true in a list
    #

    def test_list_true(self):
        """
        Test [True]
        """
        self.data_in = [True]
        self.expected = '[\n  true\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_list_true_c(self):
        """
        Test [True] -c
        """
        self.data_in = [True]
        self.expected = '[true]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True), self.expected)

    def test_list_true_r(self):
        """
        Test [True] -r
        """
        self.data_in = [True]
        self.expected = '[\n  true\n]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_list_true_l(self):
        """
        Test [True] -l
        """
        self.data_in = [True]
        self.expected = 'true'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_list_true_cl(self):
        """
        Test [True] -cl
        """
        self.data_in = [True]
        self.expected = 'true'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, lines=True), self.expected)

    def test_list_true_rl(self):
        """
        Test [True] -rl
        """
        self.data_in = [True]
        self.expected = 'true'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, lines=True), self.expected)

    def test_list_true_cr(self):
        """
        Test [True] -cr
        """
        self.data_in = [True]
        self.expected = '[true]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, raw=True), self.expected)

    def test_list_true_crl(self):
        """
        Test [True] -crl
        """
        self.data_in = [True]
        self.expected = 'true'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, lines=True), self.expected)

    #
    # false in a list
    #

    def test_list_false(self):
        """
        Test [False]
        """
        self.data_in = [False]
        self.expected = '[\n  false\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_list_false_c(self):
        """
        Test [False] -c
        """
        self.data_in = [False]
        self.expected = '[false]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True), self.expected)

    def test_list_false_r(self):
        """
        Test [False] -r
        """
        self.data_in = [False]
        self.expected = '[\n  false\n]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_list_false_l(self):
        """
        Test [False] -l
        """
        self.data_in = [False]
        self.expected = 'false'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_list_false_cl(self):
        """
        Test [False] -cl
        """
        self.data_in = [False]
        self.expected = 'false'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, lines=True), self.expected)

    def test_list_false_rl(self):
        """
        Test [False] -rl
        """
        self.data_in = [False]
        self.expected = 'false'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, lines=True), self.expected)

    def test_list_false_cr(self):
        """
        Test [False] -cr
        """
        self.data_in = [False]
        self.expected = '[false]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, raw=True), self.expected)

    def test_list_false_crl(self):
        """
        Test [False] -crl
        """
        self.data_in = [False]
        self.expected = 'false'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, lines=True), self.expected)

    #
    # null in a list
    #

    def test_list_null(self):
        """
        Test [None]
        """
        self.data_in = [None]
        self.expected = '[\n  null\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_list_null_c(self):
        """
        Test [None] -c
        """
        self.data_in = [None]
        self.expected = '[null]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True), self.expected)

    def test_list_null_r(self):
        """
        Test [None] -r
        """
        self.data_in = [None]
        self.expected = '[\n  null\n]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_list_null_l(self):
        """
        Test [None] -l
        """
        self.data_in = [None]
        self.expected = ''
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_list_null_cl(self):
        """
        Test [None] -cl
        """
        self.data_in = [None]
        self.expected = ''
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, lines=True), self.expected)

    def test_list_null_rl(self):
        """
        Test [None] -rl
        """
        self.data_in = [None]
        self.expected = ''
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, lines=True), self.expected)

    def test_list_null_cr(self):
        """
        Test [None] -cr
        """
        self.data_in = [None]
        self.expected = '[null]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, raw=True), self.expected)

    def test_list_null_crl(self):
        """
        Test [False] -crl
        """
        self.data_in = [None]
        self.expected = ''
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, lines=True), self.expected)

    def test_list_null_n(self):
        """
        Test [None] -n
        """
        self.data_in = [None]
        self.expected = '[\n  null\n]'
        self.assertEqual(jello.cli.create_json(self.data_in, nulls=True), self.expected)

    def test_list_null_nc(self):
        """
        Test [None] -nc
        """
        self.data_in = [None]
        self.expected = '[null]'
        self.assertEqual(jello.cli.create_json(self.data_in, nulls=True, compact=True), self.expected)

    def test_list_null_nl(self):
        """
        Test [None] -nl
        """
        self.data_in = [None]
        self.expected = 'null'
        self.assertEqual(jello.cli.create_json(self.data_in, nulls=True, lines=True), self.expected)

    def test_list_null_nr(self):
        """
        Test [None] -nr
        """
        self.data_in = [None]
        self.expected = '[\n  null\n]'
        self.assertEqual(jello.cli.create_json(self.data_in, nulls=True, raw=True), self.expected)

    def test_list_null_ncr(self):
        """
        Test [None] -ncr
        """
        self.data_in = [None]
        self.expected = '[null]'
        self.assertEqual(jello.cli.create_json(self.data_in, nulls=True, compact=True, raw=True), self.expected)

    def test_list_null_ncl(self):
        """
        Test [None] -ncl
        """
        self.data_in = [None]
        self.expected = 'null'
        self.assertEqual(jello.cli.create_json(self.data_in, nulls=True, compact=True, lines=True), self.expected)

    def test_list_null_nlr(self):
        """
        Test [None] -nlr
        """
        self.data_in = [None]
        self.expected = 'null'
        self.assertEqual(jello.cli.create_json(self.data_in, nulls=True, lines=True, raw=True), self.expected)

    def test_list_null_nlrc(self):
        """
        Test [None] -nlrc
        """
        self.data_in = [None]
        self.expected = 'null'
        self.assertEqual(jello.cli.create_json(self.data_in, nulls=True, lines=True, raw=True, compact=True), self.expected)

    #
    # Int in a list
    #

    def test_list_int(self):
        """
        Test [integer]
        """
        self.data_in = [42]
        self.expected = '[\n  42\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_list_int_c(self):
        """
        Test [integer] -c
        """
        self.data_in = [42]
        self.expected = '[42]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True), self.expected)

    def test_list_int_l(self):
        """
        Test [integer] -l
        """
        self.data_in = [42]
        self.expected = '42'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_list_int_r(self):
        """
        Test [integer] -r
        """
        self.data_in = [42]
        self.expected = '[\n  42\n]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_list_int_rl(self):
        """
        Test [integer] -rl
        """
        self.data_in = [42]
        self.expected = '42'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True, raw=True), self.expected)

    def test_list_int_cl(self):
        """
        Test [integer] -cl
        """
        self.data_in = [42]
        self.expected = '42'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, lines=True), self.expected)

    def test_list_int_crl(self):
        """
        Test [integer] -crl
        """
        self.data_in = [42]
        self.expected = '42'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, raw=True, lines=True), self.expected)

    #
    # Float in a list
    #

    def test_list_float(self):
        """
        Test [float]
        """
        self.data_in = [3.14]
        self.expected = '[\n  3.14\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_list_float_c(self):
        """
        Test [float] -c
        """
        self.data_in = [3.14]
        self.expected = '[3.14]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True), self.expected)

    def test_list_float_l(self):
        """
        Test [float] -l
        """
        self.data_in = [3.14]
        self.expected = '3.14'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_list_float_r(self):
        """
        Test [float] -r
        """
        self.data_in = [3.14]
        self.expected = '[\n  3.14\n]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_list_float_rl(self):
        """
        Test [float] -rl
        """
        self.data_in = [3.14]
        self.expected = '3.14'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True, raw=True), self.expected)

    def test_list_float_rc(self):
        """
        Test [float] -rc
        """
        self.data_in = [3.14]
        self.expected = '[3.14]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, compact=True), self.expected)

    def test_list_float_rcl(self):
        """
        Test [float] -rcl
        """
        self.data_in = [3.14]
        self.expected = '3.14'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, compact=True, lines=True), self.expected)

    #
    # String in a list
    #

    def test_list_str(self):
        """
        Test ['string with spaces\nand newline\ncharacters']
        """
        self.data_in = ['string with spaces\nand newline\ncharacters']
        self.expected = '[\n  "string with spaces\\nand newline\\ncharacters"\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_list_str_l(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -l
        """
        self.data_in = ['string with spaces\nand newline\ncharacters']
        self.expected = '"string with spaces\\nand newline\\ncharacters"'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_list_str_r(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -r
        """
        self.data_in = ['string with spaces\nand newline\ncharacters']
        self.expected = '[\n  "string with spaces\\nand newline\\ncharacters"\n]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_list_str_c(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -c
        """
        self.data_in = ['string with spaces\nand newline\ncharacters']
        self.expected = '["string with spaces\\nand newline\\ncharacters"]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True), self.expected)

    def test_list_str_rl(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -rl
        """
        self.data_in = ['string with spaces\nand newline\ncharacters']
        self.expected = 'string with spaces\\nand newline\\ncharacters'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True, raw=True), self.expected)

    def test_list_str_rc(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -rc
        """
        self.data_in = ['string with spaces\nand newline\ncharacters']
        self.expected = '["string with spaces\\nand newline\\ncharacters"]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, compact=True), self.expected)

    def test_list_str_cl(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -cl
        """
        self.data_in = ['string with spaces\nand newline\ncharacters']
        self.expected = '"string with spaces\\nand newline\\ncharacters"'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, lines=True), self.expected)

    def test_list_str_crl(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -crl
        """
        self.data_in = ['string with spaces\nand newline\ncharacters']
        self.expected = 'string with spaces\\nand newline\\ncharacters'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, raw=True, lines=True), self.expected)

    #
    # List with different types of elements
    #

    def test_list_sample(self):
        """
        Test self.list_sample
        """
        self.data_in = self.list_sample
        self.expected = '[\n  "string\\nwith newline\\ncharacters in it",\n  true,\n  false,\n  null,\n  42,\n  3.14\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_list_sample_l(self):
        """
        Test self.list_sample -l
        """
        self.data_in = self.list_sample
        self.expected = '"string\\nwith newline\\ncharacters in it"\ntrue\nfalse\n\n42\n3.14'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_list_sample_r(self):
        """
        Test self.list_sample -r
        """
        self.data_in = self.list_sample
        self.expected = '[\n  "string\\nwith newline\\ncharacters in it",\n  true,\n  false,\n  null,\n  42,\n  3.14\n]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_list_sample_c(self):
        """
        Test self.list_sample -c
        """
        self.data_in = self.list_sample
        self.expected = '["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True), self.expected)

    def test_list_sample_rl(self):
        """
        Test self.list_sample -rl
        """
        self.data_in = self.list_sample
        self.expected = 'string\\nwith newline\\ncharacters in it\ntrue\nfalse\n\n42\n3.14'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, lines=True), self.expected)

    def test_list_sample_rc(self):
        """
        Test self.list_sample -rc
        """
        self.data_in = self.list_sample
        self.expected = '["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, compact=True), self.expected)

    def test_list_sample_cl(self):
        """
        Test self.list_sample -cl
        """
        self.data_in = self.list_sample
        self.expected = '"string\\nwith newline\\ncharacters in it"\ntrue\nfalse\n\n42\n3.14'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, lines=True), self.expected)

    def test_list_sample_crl(self):
        """
        Test self.list_sample -crl
        """
        self.data_in = self.list_sample
        self.expected = 'string\\nwith newline\\ncharacters in it\ntrue\nfalse\n\n42\n3.14'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, raw=True, lines=True), self.expected)

    #
    # Dicts in a list
    #

    def test_list_dict(self):
        """
        Test self.list_of_dicts_sample
        """
        self.data_in = self.list_of_dicts_sample
        self.expected = '[\n  {\n    "string": "string\\nwith newline\\ncharacters in it",\n    "true": true,\n    "false": false,\n    "null": null,\n    "int": 42,\n    "float": 3.14,\n    "array": [\n      "string\\nwith newline\\ncharacters in it",\n      true,\n      false,\n      null,\n      42,\n      3.14\n    ]\n  },\n  {\n    "string": "another string\\nwith newline\\ncharacters in it",\n    "true": true,\n    "false": false,\n    "null": null,\n    "int": 10001,\n    "float": -400.45,\n    "array": [\n      "string\\nwith newline\\ncharacters in it",\n      true,\n      false,\n      null,\n      -6000034,\n      999999.854321\n    ]\n  }\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_list_dict_c(self):
        """
        Test self.list_of_dicts_sample -c
        """
        self.data_in = self.list_of_dicts_sample
        self.expected = '[{"string": "string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 42, "float": 3.14, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]}, {"string": "another string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 10001, "float": -400.45, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, -6000034, 999999.854321]}]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True), self.expected)

    def test_list_dict_r(self):
        """
        Test self.list_of_dicts_sample -r
        """
        self.data_in = self.list_of_dicts_sample
        self.expected = '[\n  {\n    "string": "string\\nwith newline\\ncharacters in it",\n    "true": true,\n    "false": false,\n    "null": null,\n    "int": 42,\n    "float": 3.14,\n    "array": [\n      "string\\nwith newline\\ncharacters in it",\n      true,\n      false,\n      null,\n      42,\n      3.14\n    ]\n  },\n  {\n    "string": "another string\\nwith newline\\ncharacters in it",\n    "true": true,\n    "false": false,\n    "null": null,\n    "int": 10001,\n    "float": -400.45,\n    "array": [\n      "string\\nwith newline\\ncharacters in it",\n      true,\n      false,\n      null,\n      -6000034,\n      999999.854321\n    ]\n  }\n]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_list_dict_l(self):
        """
        Test self.list_of_dicts_sample -l
        """
        self.data_in = self.list_of_dicts_sample
        self.expected = '{"string": "string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 42, "float": 3.14, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]}\n{"string": "another string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 10001, "float": -400.45, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, -6000034, 999999.854321]}'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_list_dict_cr(self):
        """
        Test self.list_of_dicts_sample -cr
        """
        self.data_in = self.list_of_dicts_sample
        self.expected = '[{"string": "string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 42, "float": 3.14, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]}, {"string": "another string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 10001, "float": -400.45, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, -6000034, 999999.854321]}]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, raw=True), self.expected)

    def test_list_dict_cl(self):
        """
        Test self.list_of_dicts_sample -cl
        """
        self.data_in = self.list_of_dicts_sample
        self.expected = '{"string": "string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 42, "float": 3.14, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]}\n{"string": "another string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 10001, "float": -400.45, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, -6000034, 999999.854321]}'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, lines=True), self.expected)

    def test_list_dict_rl(self):
        """
        Test self.list_of_dicts_sample -rl
        """
        self.data_in = self.list_of_dicts_sample
        self.expected = '{"string": "string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 42, "float": 3.14, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]}\n{"string": "another string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 10001, "float": -400.45, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, -6000034, 999999.854321]}'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True, lines=True), self.expected)

    def test_list_dict_crl(self):
        """
        Test self.list_of_dicts_sample -crl
        """
        self.data_in = self.list_of_dicts_sample
        self.expected = '{"string": "string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 42, "float": 3.14, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14]}\n{"string": "another string\\nwith newline\\ncharacters in it", "true": true, "false": false, "null": null, "int": 10001, "float": -400.45, "array": ["string\\nwith newline\\ncharacters in it", true, false, null, -6000034, 999999.854321]}'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, raw=True, lines=True), self.expected)

    #
    # lists in list
    #

    def test_list_list(self):
        """
        Test self.list_of_lists_sample
        """
        self.data_in = self.list_of_lists_sample
        self.expected = '[\n  [\n    "string\\nwith newline\\ncharacters in it",\n    true,\n    false,\n    null,\n    42,\n    3.14\n  ],\n  [\n    "another string\\nwith newline\\ncharacters in it",\n    true,\n    false,\n    null,\n    42001,\n    -3.14\n  ]\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_list_list_c(self):
        """
        Test self.list_of_lists_sample -c
        """
        self.data_in = self.list_of_lists_sample
        self.expected = '[["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14], ["another string\\nwith newline\\ncharacters in it", true, false, null, 42001, -3.14]]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True), self.expected)

    def test_list_list_r(self):
        """
        Test self.list_of_lists_sample -r
        """
        self.data_in = self.list_of_lists_sample
        self.expected = '[\n  [\n    "string\\nwith newline\\ncharacters in it",\n    true,\n    false,\n    null,\n    42,\n    3.14\n  ],\n  [\n    "another string\\nwith newline\\ncharacters in it",\n    true,\n    false,\n    null,\n    42001,\n    -3.14\n  ]\n]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_list_list_l(self):
        """
        Test self.list_of_lists_sample -l
        """
        self.data_in = self.list_of_lists_sample
        self.assertRaises(SystemExit, jello.cli.create_json, self.data_in, lines=True)

    def test_list_list_cr(self):
        """
        Test self.list_of_lists_sample -cr
        """
        self.data_in = self.list_of_lists_sample
        self.expected = '[["string\\nwith newline\\ncharacters in it", true, false, null, 42, 3.14], ["another string\\nwith newline\\ncharacters in it", true, false, null, 42001, -3.14]]'
        self.assertEqual(jello.cli.create_json(self.data_in, compact=True, raw=True), self.expected)

    def test_list_list_cl(self):
        """
        Test self.list_of_lists_sample -cl
        """
        self.data_in = self.list_of_lists_sample
        self.assertRaises(SystemExit, jello.cli.create_json, self.data_in, compact=True, lines=True)

    def test_list_list_rl(self):
        """
        Test self.list_of_lists_sample -rl
        """
        self.data_in = self.list_of_lists_sample
        self.assertRaises(SystemExit, jello.cli.create_json, self.data_in, raw=True, lines=True)

    def test_list_list_crl(self):
        """
        Test self.list_of_lists_sample -crl
        """
        self.data_in = self.list_of_lists_sample
        self.assertRaises(SystemExit, jello.cli.create_json, self.data_in, compact=True, raw=True, lines=True)


if __name__ == '__main__':
    unittest.main()
