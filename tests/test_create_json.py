import unittest
import jello.cli


class MyTests(unittest.TestCase):

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

    def test_int(self):
        """
        Test integer
        """
        self.data_in = [42]
        self.expected = '[\n  42\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_int_l(self):
        """
        Test integer -l
        """
        self.data_in = [42]
        self.expected = '42\n'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_int_r(self):
        """
        Test integer -r
        """
        self.data_in = [42]
        self.expected = '[\n  42\n]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_int_rl(self):
        """
        Test integer -rl
        """
        self.data_in = [42]
        self.expected = '42\n'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True, raw=True), self.expected)

    def test_float(self):
        """
        Test float
        """
        self.data_in = [3.14]
        self.expected = '[\n  3.14\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_float_l(self):
        """
        Test float -l
        """
        self.data_in = [3.14]
        self.expected = '3.14\n'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True), self.expected)

    def test_float_r(self):
        """
        Test float -r
        """
        self.data_in = [3.14]
        self.expected = '[\n  3.14\n]'
        self.assertEqual(jello.cli.create_json(self.data_in, raw=True), self.expected)

    def test_float_rl(self):
        """
        Test float -rl
        """
        self.data_in = [3.14]
        self.expected = '3.14\n'
        self.assertEqual(jello.cli.create_json(self.data_in, lines=True, raw=True), self.expected)

    def test_list_dict_single_key_value(self):
        """
        Test [{'key1': 'value1'}]
        """
        self.data_in = [{'key1': 'value1'}]
        self.expected = '[\n  {\n    "key1": "value1"\n  }\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_dict_single_key_value(self):
        """
        Test {'key1': 'value1'}
        """
        self.data_in = {'key1': 'value1'}
        self.expected = '{\n  "key1": "value1"\n}'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_list_dict_multiple_key_value(self):
        """
        Test [{'key1': 'value1'}, {'key2': 'value1'}]
        """
        self.data_in = [{'key1': 'value1'}, {'key2': 'value1'}]
        self.expected = '[\n  {\n    "key1": "value1"\n  },\n  {\n    "key2": "value1"\n  }\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)

    def test_list_dict_list_values(self):
        """
        Test [{'key1': ['value1', 0, True, 3.14]}, {'key1': ['value2', 5, False, 8.88]}]
        """
        self.data_in = [{'key1': ['value1', 0, True, 3.14]}, {'key1': ['value2', 5, False, 8.88]}]
        self.expected = '[\n  {\n    "key1": [\n      "value1",\n      0,\n      true,\n      3.14\n    ]\n  },\n  {\n    "key1": [\n      "value2",\n      5,\n      false,\n      8.88\n    ]\n  }\n]'
        self.assertEqual(jello.cli.create_json(self.data_in), self.expected)


if __name__ == '__main__':
    unittest.main()
