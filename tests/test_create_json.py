#!/usr/bin/env python3

import unittest
from collections import OrderedDict
import pygments
from jello.lib import opts, Json


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

        # initialize Json class
        self.json_out = Json()

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
        data_in = True
        expected = 'true'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_true_r(self):
        """
        Test True -r
        """
        data_in = True
        expected = 'true'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_true_l(self):
        """
        Test True -l
        """
        data_in = True
        expected = 'true'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_true_rl(self):
        """
        Test True -rl
        """
        data_in = True
        expected = 'true'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # Naked False
    #

    def test_false(self):
        """
        Test False
        """
        data_in = False
        expected = 'false'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_false_r(self):
        """
        Test False -r
        """
        data_in = False
        expected = 'false'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_false_l(self):
        """
        Test False -l
        """
        data_in = False
        expected = 'false'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_false_rl(self):
        """
        Test False -rl
        """
        data_in = False
        expected = 'false'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # Naked null
    #

    def test_null(self):
        """
        Test None
        """
        data_in = None
        expected = ''
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_null_n(self):
        """
        Test None with -n
        """
        data_in = None
        expected = 'null'
        opts.nulls = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_null_r(self):
        """
        Test None with -r
        """
        data_in = None
        expected = ''
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_null_rl(self):
        """
        Test None with -rl
        """
        data_in = None
        expected = ''
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_null_rln(self):
        """
        Test None with -rln
        """
        data_in = None
        expected = 'null'
        opts.raw = True
        opts.lines = True
        opts.nulls = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # naked int
    #

    def test_int(self):
        """
        Test int
        """
        data_in = 42
        expected = '42'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_int_r(self):
        """
        Test int -r
        """
        data_in = 42
        expected = '42'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_int_l(self):
        """
        Test int -l
        """
        data_in = 42
        expected = '42'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_int_rl(self):
        """
        Test int -rl
        """
        data_in = 42
        expected = '42'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # naked float
    #

    def test_float(self):
        """
        Test float
        """
        data_in = 3.14
        expected = '3.14'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_float_r(self):
        """
        Test float -r
        """
        data_in = 3.14
        expected = '3.14'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_float_l(self):
        """
        Test float -l
        """
        data_in = 3.14
        expected = '3.14'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_float_rl(self):
        """
        Test float -rl
        """
        data_in = 3.14
        expected = '3.14'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # naked string
    #

    def test_string(self):
        """
        Test "string with\nnewline char"
        """
        data_in = '"string with\nnewline char"'
        expected = '""string with\\nnewline char""'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_string_r(self):
        """
        Test "string with\nnewline char" -r
        """
        data_in = '"string with\nnewline char"'
        expected = '"string with\\nnewline char"'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_string_l(self):
        """
        Test "string with\nnewline char" -l
        """
        data_in = '"string with\nnewline char"'
        expected = '""string with\\nnewline char""'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_string_rl(self):
        """
        Test "string with\nnewline char" -rl
        """
        data_in = '"string with\nnewline char"'
        expected = '"string with\\nnewline char"'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # Naked Dict
    #

    def test_dict(self):
        """
        Test self.dict_sample
        """
        data_in = self.dict_sample
        expected = '{\n  "string": "string\\nwith newline\\ncharacters in it",\n  "true": true,\n  "false": false,\n  "null": null,\n  "int": 42,\n  "float": 3.14,\n  "array": [\n    "string\\nwith newline\\ncharacters in it",\n    true,\n    false,\n    null,\n    42,\n    3.14\n  ]\n}'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_dict_r(self):
        """
        Test self.dict_sample -r
        """
        data_in = self.dict_sample
        expected = '{\n  "string": "string\\nwith newline\\ncharacters in it",\n  "true": true,\n  "false": false,\n  "null": null,\n  "int": 42,\n  "float": 3.14,\n  "array": [\n    "string\\nwith newline\\ncharacters in it",\n    true,\n    false,\n    null,\n    42,\n    3.14\n  ]\n}'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_dict_l(self):
        """
        Test self.dict_sample -l
        """
        data_in = self.dict_sample
        expected = '{"string":"string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":42,"float":3.14,"array":["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]}'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_dict_c(self):
        """
        Test self.dict_sample -c
        """
        data_in = self.dict_sample
        expected = '{"string":"string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":42,"float":3.14,"array":["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]}'
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_dict_rl(self):
        """
        Test self.dict_sample -rl
        """
        data_in = self.dict_sample
        expected = '{"string":"string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":42,"float":3.14,"array":["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]}'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_dict_cl(self):
        """
        Test self.dict_sample -cl
        """
        data_in = self.dict_sample
        expected = '{"string":"string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":42,"float":3.14,"array":["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]}'
        opts.compact = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_dict_cr(self):
        """
        Test self.dict_sample -cr
        """
        data_in = self.dict_sample
        expected = '{"string":"string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":42,"float":3.14,"array":["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]}'
        opts.compact = True
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_dict_crl(self):
        """
        Test self.dict_sample -crl
        """
        data_in = self.dict_sample
        expected = '{"string":"string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":42,"float":3.14,"array":["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]}'
        opts.compact = True
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    # only run this test if using pygments 2.9.0
    @unittest.skipIf(pygments.__version__ != '2.9.0', "Skip if Pygments 2.9.0 is not installed")
    def test_dict_html(self):
        """
        Test self.dict_sample html output
        """
        data_in = self.dict_sample
        expected = '<div class="highlight" style="background: #ffffff"><pre style="line-height: 125%;"><span></span>{\n  <span style="color: #00007f; font-weight: bold">&quot;string&quot;</span>: <span style="color: #007f00">&quot;string\\nwith newline\\ncharacters in it&quot;</span>,\n  <span style="color: #00007f; font-weight: bold">&quot;true&quot;</span>: <span style="color: #555555">true</span>,\n  <span style="color: #00007f; font-weight: bold">&quot;false&quot;</span>: <span style="color: #555555">false</span>,\n  <span style="color: #00007f; font-weight: bold">&quot;null&quot;</span>: <span style="color: #555555">null</span>,\n  <span style="color: #00007f; font-weight: bold">&quot;int&quot;</span>: <span style="color: #7f007f">42</span>,\n  <span style="color: #00007f; font-weight: bold">&quot;float&quot;</span>: <span style="color: #7f007f">3.14</span>,\n  <span style="color: #00007f; font-weight: bold">&quot;array&quot;</span>: [\n    <span style="color: #007f00">&quot;string\\nwith newline\\ncharacters in it&quot;</span>,\n    <span style="color: #555555">true</span>,\n    <span style="color: #555555">false</span>,\n    <span style="color: #555555">null</span>,\n    <span style="color: #7f007f">42</span>,\n    <span style="color: #7f007f">3.14</span>\n  ]\n}\n</pre></div>\n'
        output = self.json_out.create_json(data_in)
        self.assertEqual(self.json_out.html_output(output), expected)

    def test_dict_color(self):
        """
        Test self.dict_sample color output
        """
        data_in = self.dict_sample
        expected = '{\n  \x1b[34;01m"string"\x1b[39;00m: \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[39m,\n  \x1b[34;01m"true"\x1b[39;00m: \x1b[90mtrue\x1b[39m,\n  \x1b[34;01m"false"\x1b[39;00m: \x1b[90mfalse\x1b[39m,\n  \x1b[34;01m"null"\x1b[39;00m: \x1b[90mnull\x1b[39m,\n  \x1b[34;01m"int"\x1b[39;00m: \x1b[35m42\x1b[39m,\n  \x1b[34;01m"float"\x1b[39;00m: \x1b[35m3.14\x1b[39m,\n  \x1b[34;01m"array"\x1b[39;00m: [\n    \x1b[32m"string\\nwith newline\\ncharacters in it"\x1b[39m,\n    \x1b[90mtrue\x1b[39m,\n    \x1b[90mfalse\x1b[39m,\n    \x1b[90mnull\x1b[39m,\n    \x1b[35m42\x1b[39m,\n    \x1b[35m3.14\x1b[39m\n  ]\n}'
        output = self.json_out.create_json(data_in)
        self.assertEqual(self.json_out.color_output(output), expected)

    #
    # true in a list
    #

    def test_list_true(self):
        """
        Test [True]
        """
        data_in = [True]
        expected = '[\n  true\n]'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_true_c(self):
        """
        Test [True] -c
        """
        data_in = [True]
        expected = '[true]'
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_true_r(self):
        """
        Test [True] -r
        """
        data_in = [True]
        expected = '[\n  true\n]'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_true_l(self):
        """
        Test [True] -l
        """
        data_in = [True]
        expected = 'true'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_true_cl(self):
        """
        Test [True] -cl
        """
        data_in = [True]
        expected = 'true'
        opts.compact = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_true_rl(self):
        """
        Test [True] -rl
        """
        data_in = [True]
        expected = 'true'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_true_cr(self):
        """
        Test [True] -cr
        """
        data_in = [True]
        expected = '[true]'
        opts.compact = True
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_true_crl(self):
        """
        Test [True] -crl
        """
        data_in = [True]
        expected = 'true'
        opts.compact = True
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # false in a list
    #

    def test_list_false(self):
        """
        Test [False]
        """
        data_in = [False]
        expected = '[\n  false\n]'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_false_c(self):
        """
        Test [False] -c
        """
        data_in = [False]
        expected = '[false]'
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_false_r(self):
        """
        Test [False] -r
        """
        data_in = [False]
        expected = '[\n  false\n]'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_false_l(self):
        """
        Test [False] -l
        """
        data_in = [False]
        expected = 'false'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_false_cl(self):
        """
        Test [False] -cl
        """
        data_in = [False]
        expected = 'false'
        opts.compact = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_false_rl(self):
        """
        Test [False] -rl
        """
        data_in = [False]
        expected = 'false'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_false_cr(self):
        """
        Test [False] -cr
        """
        data_in = [False]
        expected = '[false]'
        opts.compact = True
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_false_crl(self):
        """
        Test [False] -crl
        """
        data_in = [False]
        expected = 'false'
        opts.compact = True
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # null in a list
    #

    def test_list_null(self):
        """
        Test [None]
        """
        data_in = [None]
        expected = '[\n  null\n]'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_c(self):
        """
        Test [None] -c
        """
        data_in = [None]
        expected = '[null]'
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_r(self):
        """
        Test [None] -r
        """
        data_in = [None]
        expected = '[\n  null\n]'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_l(self):
        """
        Test [None] -l
        """
        data_in = [None]
        expected = ''
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_cl(self):
        """
        Test [None] -cl
        """
        data_in = [None]
        expected = ''
        opts.compact = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_rl(self):
        """
        Test [None] -rl
        """
        data_in = [None]
        expected = ''
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_cr(self):
        """
        Test [None] -cr
        """
        data_in = [None]
        expected = '[null]'
        opts.compact = True
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_crl(self):
        """
        Test [False] -crl
        """
        data_in = [None]
        expected = ''
        opts.compact = True
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_n(self):
        """
        Test [None] -n
        """
        data_in = [None]
        expected = '[\n  null\n]'
        opts.nulls = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_nc(self):
        """
        Test [None] -nc
        """
        data_in = [None]
        expected = '[null]'
        opts.nulls = True
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_nl(self):
        """
        Test [None] -nl
        """
        data_in = [None]
        expected = 'null'
        opts.nulls = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_nr(self):
        """
        Test [None] -nr
        """
        data_in = [None]
        expected = '[\n  null\n]'
        opts.nulls = True
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_ncr(self):
        """
        Test [None] -ncr
        """
        data_in = [None]
        expected = '[null]'
        opts.nulls = True
        opts.compact = True
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_ncl(self):
        """
        Test [None] -ncl
        """
        data_in = [None]
        expected = 'null'
        opts.nulls = True
        opts.compact = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_nlr(self):
        """
        Test [None] -nlr
        """
        data_in = [None]
        expected = 'null'
        opts.nulls = True
        opts.lines = True
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_null_nlrc(self):
        """
        Test [None] -nlrc
        """
        data_in = [None]
        expected = 'null'
        opts.nulls = True
        opts.lines = True
        opts.raw = True
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # Int in a list
    #

    def test_list_int(self):
        """
        Test [integer]
        """
        data_in = [42]
        expected = '[\n  42\n]'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_int_c(self):
        """
        Test [integer] -c
        """
        data_in = [42]
        expected = '[42]'
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_int_l(self):
        """
        Test [integer] -l
        """
        data_in = [42]
        expected = '42'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_int_r(self):
        """
        Test [integer] -r
        """
        data_in = [42]
        expected = '[\n  42\n]'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_int_rl(self):
        """
        Test [integer] -rl
        """
        data_in = [42]
        expected = '42'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_int_cl(self):
        """
        Test [integer] -cl
        """
        data_in = [42]
        expected = '42'
        opts.compact = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_int_crl(self):
        """
        Test [integer] -crl
        """
        data_in = [42]
        expected = '42'
        opts.compact = True
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # Float in a list
    #

    def test_list_float(self):
        """
        Test [float]
        """
        data_in = [3.14]
        expected = '[\n  3.14\n]'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_float_c(self):
        """
        Test [float] -c
        """
        data_in = [3.14]
        expected = '[3.14]'
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_float_l(self):
        """
        Test [float] -l
        """
        data_in = [3.14]
        expected = '3.14'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_float_r(self):
        """
        Test [float] -r
        """
        data_in = [3.14]
        expected = '[\n  3.14\n]'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_float_rl(self):
        """
        Test [float] -rl
        """
        data_in = [3.14]
        expected = '3.14'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_float_rc(self):
        """
        Test [float] -rc
        """
        data_in = [3.14]
        expected = '[3.14]'
        opts.raw = True
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_float_rcl(self):
        """
        Test [float] -rcl
        """
        data_in = [3.14]
        expected = '3.14'
        opts.raw = True
        opts.compact = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # String in a list
    #

    def test_list_str(self):
        """
        Test ['string with spaces\nand newline\ncharacters']
        """
        data_in = ['string with spaces\nand newline\ncharacters']
        expected = '[\n  "string with spaces\\nand newline\\ncharacters"\n]'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_str_l(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -l
        """
        data_in = ['string with spaces\nand newline\ncharacters']
        expected = '"string with spaces\\nand newline\\ncharacters"'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_str_r(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -r
        """
        data_in = ['string with spaces\nand newline\ncharacters']
        expected = '[\n  "string with spaces\\nand newline\\ncharacters"\n]'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_str_c(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -c
        """
        data_in = ['string with spaces\nand newline\ncharacters']
        expected = '["string with spaces\\nand newline\\ncharacters"]'
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_str_rl(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -rl
        """
        data_in = ['string with spaces\nand newline\ncharacters']
        expected = 'string with spaces\\nand newline\\ncharacters'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_str_rc(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -rc
        """
        data_in = ['string with spaces\nand newline\ncharacters']
        expected = '["string with spaces\\nand newline\\ncharacters"]'
        opts.raw = True
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_str_cl(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -cl
        """
        data_in = ['string with spaces\nand newline\ncharacters']
        expected = '"string with spaces\\nand newline\\ncharacters"'
        opts.compact = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_str_crl(self):
        """
        Test ['string with spaces\nand newline\ncharacters'] -crl
        """
        data_in = ['string with spaces\nand newline\ncharacters']
        expected = 'string with spaces\\nand newline\\ncharacters'
        opts.compact = True
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # List with different types of elements
    #

    def test_list_sample(self):
        """
        Test self.list_sample
        """
        data_in = self.list_sample
        expected = '[\n  "string\\nwith newline\\ncharacters in it",\n  true,\n  false,\n  null,\n  42,\n  3.14\n]'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_sample_l(self):
        """
        Test self.list_sample -l
        """
        data_in = self.list_sample
        expected = '"string\\nwith newline\\ncharacters in it"\ntrue\nfalse\n\n42\n3.14'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_sample_r(self):
        """
        Test self.list_sample -r
        """
        data_in = self.list_sample
        expected = '[\n  "string\\nwith newline\\ncharacters in it",\n  true,\n  false,\n  null,\n  42,\n  3.14\n]'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_sample_c(self):
        """
        Test self.list_sample -c
        """
        data_in = self.list_sample
        expected = '["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]'
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_sample_rl(self):
        """
        Test self.list_sample -rl
        """
        data_in = self.list_sample
        expected = 'string\\nwith newline\\ncharacters in it\ntrue\nfalse\n\n42\n3.14'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_sample_rc(self):
        """
        Test self.list_sample -rc
        """
        data_in = self.list_sample
        expected = '["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]'
        opts.raw = True
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_sample_cl(self):
        """
        Test self.list_sample -cl
        """
        data_in = self.list_sample
        expected = '"string\\nwith newline\\ncharacters in it"\ntrue\nfalse\n\n42\n3.14'
        opts.compact = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_sample_crl(self):
        """
        Test self.list_sample -crl
        """
        data_in = self.list_sample
        expected = 'string\\nwith newline\\ncharacters in it\ntrue\nfalse\n\n42\n3.14'
        opts.compact = True
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # Dicts in a list
    #

    def test_list_dict(self):
        """
        Test self.list_of_dicts_sample
        """
        data_in = self.list_of_dicts_sample
        expected = '[\n  {\n    "string": "string\\nwith newline\\ncharacters in it",\n    "true": true,\n    "false": false,\n    "null": null,\n    "int": 42,\n    "float": 3.14,\n    "array": [\n      "string\\nwith newline\\ncharacters in it",\n      true,\n      false,\n      null,\n      42,\n      3.14\n    ]\n  },\n  {\n    "string": "another string\\nwith newline\\ncharacters in it",\n    "true": true,\n    "false": false,\n    "null": null,\n    "int": 10001,\n    "float": -400.45,\n    "array": [\n      "string\\nwith newline\\ncharacters in it",\n      true,\n      false,\n      null,\n      -6000034,\n      999999.854321\n    ]\n  }\n]'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_dict_c(self):
        """
        Test self.list_of_dicts_sample -c
        """
        data_in = self.list_of_dicts_sample
        expected = '[{"string":"string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":42,"float":3.14,"array":["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]},{"string":"another string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":10001,"float":-400.45,"array":["string\\nwith newline\\ncharacters in it",true,false,null,-6000034,999999.854321]}]'
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_dict_r(self):
        """
        Test self.list_of_dicts_sample -r
        """
        data_in = self.list_of_dicts_sample
        expected = '[\n  {\n    "string": "string\\nwith newline\\ncharacters in it",\n    "true": true,\n    "false": false,\n    "null": null,\n    "int": 42,\n    "float": 3.14,\n    "array": [\n      "string\\nwith newline\\ncharacters in it",\n      true,\n      false,\n      null,\n      42,\n      3.14\n    ]\n  },\n  {\n    "string": "another string\\nwith newline\\ncharacters in it",\n    "true": true,\n    "false": false,\n    "null": null,\n    "int": 10001,\n    "float": -400.45,\n    "array": [\n      "string\\nwith newline\\ncharacters in it",\n      true,\n      false,\n      null,\n      -6000034,\n      999999.854321\n    ]\n  }\n]'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_dict_l(self):
        """
        Test self.list_of_dicts_sample -l
        """
        data_in = self.list_of_dicts_sample
        expected = '{"string":"string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":42,"float":3.14,"array":["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]}\n{"string":"another string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":10001,"float":-400.45,"array":["string\\nwith newline\\ncharacters in it",true,false,null,-6000034,999999.854321]}'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_dict_cr(self):
        """
        Test self.list_of_dicts_sample -cr
        """
        data_in = self.list_of_dicts_sample
        expected = '[{"string":"string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":42,"float":3.14,"array":["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]},{"string":"another string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":10001,"float":-400.45,"array":["string\\nwith newline\\ncharacters in it",true,false,null,-6000034,999999.854321]}]'
        opts.compact = True
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_dict_cl(self):
        """
        Test self.list_of_dicts_sample -cl
        """
        data_in = self.list_of_dicts_sample
        expected = '{"string":"string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":42,"float":3.14,"array":["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]}\n{"string":"another string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":10001,"float":-400.45,"array":["string\\nwith newline\\ncharacters in it",true,false,null,-6000034,999999.854321]}'
        opts.compact = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_dict_rl(self):
        """
        Test self.list_of_dicts_sample -rl
        """
        data_in = self.list_of_dicts_sample
        expected = '{"string":"string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":42,"float":3.14,"array":["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]}\n{"string":"another string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":10001,"float":-400.45,"array":["string\\nwith newline\\ncharacters in it",true,false,null,-6000034,999999.854321]}'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_dict_crl(self):
        """
        Test self.list_of_dicts_sample -crl
        """
        data_in = self.list_of_dicts_sample
        expected = '{"string":"string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":42,"float":3.14,"array":["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]}\n{"string":"another string\\nwith newline\\ncharacters in it","true":true,"false":false,"null":null,"int":10001,"float":-400.45,"array":["string\\nwith newline\\ncharacters in it",true,false,null,-6000034,999999.854321]}'
        opts.compact = True
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    #
    # lists in list
    #

    def test_list_list(self):
        """
        Test self.list_of_lists_sample
        """
        data_in = self.list_of_lists_sample
        expected = '[\n  [\n    "string\\nwith newline\\ncharacters in it",\n    true,\n    false,\n    null,\n    42,\n    3.14\n  ],\n  [\n    "another string\\nwith newline\\ncharacters in it",\n    true,\n    false,\n    null,\n    42001,\n    -3.14\n  ]\n]'
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_list_c(self):
        """
        Test self.list_of_lists_sample -c
        """
        data_in = self.list_of_lists_sample
        expected = '[["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14],["another string\\nwith newline\\ncharacters in it",true,false,null,42001,-3.14]]'
        opts.compact = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_list_r(self):
        """
        Test self.list_of_lists_sample -r
        """
        data_in = self.list_of_lists_sample
        expected = '[\n  [\n    "string\\nwith newline\\ncharacters in it",\n    true,\n    false,\n    null,\n    42,\n    3.14\n  ],\n  [\n    "another string\\nwith newline\\ncharacters in it",\n    true,\n    false,\n    null,\n    42001,\n    -3.14\n  ]\n]'
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_list_l(self):
        """
        Test self.list_of_lists_sample -l
        """
        data_in = self.list_of_lists_sample
        expected = '["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]\n["another string\\nwith newline\\ncharacters in it",true,false,null,42001,-3.14]'
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_list_cr(self):
        """
        Test self.list_of_lists_sample -cr
        """
        data_in = self.list_of_lists_sample
        expected = '[["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14],["another string\\nwith newline\\ncharacters in it",true,false,null,42001,-3.14]]'
        opts.compact = True
        opts.raw = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_list_cl(self):
        """
        Test self.list_of_lists_sample -cl
        """
        data_in = self.list_of_lists_sample
        expected = '["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]\n["another string\\nwith newline\\ncharacters in it",true,false,null,42001,-3.14]'
        opts.compact = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_list_rl(self):
        """
        Test self.list_of_lists_sample -rl
        """
        data_in = self.list_of_lists_sample
        expected = '["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]\n["another string\\nwith newline\\ncharacters in it",true,false,null,42001,-3.14]'
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_list_list_crl(self):
        """
        Test self.list_of_lists_sample -crl
        """
        data_in = self.list_of_lists_sample
        expected = '["string\\nwith newline\\ncharacters in it",true,false,null,42,3.14]\n["another string\\nwith newline\\ncharacters in it",true,false,null,42001,-3.14]'
        opts.compact = True
        opts.raw = True
        opts.lines = True
        self.assertEqual(self.json_out.create_json(data_in), expected)

    def test_non_serializable(self):
        """
        Test _.items()
        """
        data_in = OrderedDict(foo='bar').items()
        self.assertRaises(TypeError, self.json_out.create_json, data_in)

    def test_non_serializable_l(self):
        """
        Test _.items() -l
        """
        data_in = OrderedDict(foo='bar').items()
        opts.lines = True
        self.assertRaises(TypeError, self.json_out.create_json, data_in)


if __name__ == '__main__':
    unittest.main()
