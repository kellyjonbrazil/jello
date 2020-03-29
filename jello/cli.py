#!/usr/bin/env python3
"""jello - query JSON at the command line with python syntax"""

import os
import sys
import textwrap
import json
import signal
from contextlib import redirect_stdout
import io
import ast

__version__ = '0.3.1'


def ctrlc(signum, frame):
    """exit with error on SIGINT"""
    sys.exit(1)


def get_stdin():
    """return STDIN data"""
    if sys.stdin.isatty():
        return None

    return sys.stdin.read()


def helptext():
    print_error(textwrap.dedent('''\
        jello:   query JSON at the command line with python syntax

        Usage:  <JSON Data> | jello [OPTIONS] QUERY

                -c    compact JSON output
                -l    output as lines suitable for assignment to a bash array
                -n    print selected null values
                -r    raw string output (no quotes)
                -v    version info
                -h    help

        Use '_' as the input data and assign the result to 'r'. Use python dict syntax.

        Example:
                <JSON Data> | jello 'r = _["foo"]'
                variable=($(cat data.json | jello -l 'r = _["foo"]))
    '''))


def print_error(message):
    """print error messages to STDERR and quit with error code"""
    print(message, file=sys.stderr)
    sys.exit(1)


def create_json(data, compact=False, nulls=None, lines=None, raw=None):
    # check if this list includes lists
    check_type = data
    list_includes_list = False
    if isinstance(check_type, list):
        for item in check_type:
            if isinstance(item, list):
                list_includes_list = True

    if isinstance(data, (list, dict)):
        if not lines and not list_includes_list:
            new_list = []
            for line in data:
                if isinstance(line, str):
                    new_list.append(line.replace('\u2063', '\n'))
                else:
                    new_list.append(line)

            if compact:
                return json.dumps(new_list)

            else:
                return json.dumps(new_list, indent=2)

        if not lines:
            if compact:
                return json.dumps(data)
            else:
                return json.dumps(data, indent=2)

        elif lines and isinstance(data, dict):
            return json.dumps(data)

        elif lines and list_includes_list:
            print('jello:  Cannot print list of lists as lines. Try normal JSON output.\n', file=sys.stderr)
            sys.exit(1)

        # only print lines for a flat list
        else:
            flat_list = ''
            for line in data:
                if line is None:
                    if nulls:
                        flat_list += 'null\n'
                    else:
                        flat_list += '\n'

                elif line is True:
                    flat_list += 'true\n'

                elif line is False:
                    flat_list += 'false\n'

                elif isinstance(line, str):
                    string_data = line.replace('\u2063', r'\n')
                    if raw:
                        flat_list += f'{string_data}\n'
                    else:
                        flat_list += f'"{string_data}"\n'

                else:
                    # don't pretty print JSON Lines
                    flat_list += json.dumps(line) + '\n'

            return flat_list

    elif data is None:
        if nulls:
            return 'null'
        else:
            return ''

    elif data is True:
        return 'true'

    elif data is False:
        return 'false'

    elif isinstance(data, str):
        string_data = data.replace('\u2063', r'\n')
        if raw:
            return string_data
        else:
            return f'"{string_data}"'


def normalize(data, nulls=None, raw=None):
    result_list = []
    try:
        for entry in data.splitlines():
            # first check if the result is a single list with no dicts or other lists inside
            try:
                check_type = ast.literal_eval(entry)

                list_includes_obj = False
                if isinstance(check_type, list):
                    for item in check_type:
                        if isinstance(item, (list, dict)):
                            list_includes_obj = True

                if list_includes_obj:
                    # this is a higher-level list of dicts. We can safely replace
                    # \u2063 with newlines here.
                    result_list.append(ast.literal_eval(entry.replace(r'\u2063', r'\n')))
                else:
                    # this is the last node. Don't replace \u2063 with newline yet...
                    # do this in print_json()
                    result_list.append(ast.literal_eval(entry))

            except (ValueError, SyntaxError):
                # if ValueError or SyntaxError exception then it was not a
                # list, dict, bool, None, int, or float - must be a string
                # we will replace \u2063 with newlines in print_json()
                result_list.append(str(entry))

    except Exception as e:
        print(textwrap.dedent(f'''\
            jello:  Normalize Exception: {e}
                    data: {data}
                    result_list: {result_list}
            '''), file=sys.stderr)
        sys.exit(1)

    return result_list[0]


def pyquery(data, query):
    _ = data
    query = 'r = None\n' + query + '\nprint(r)'
    output = None

    f = io.StringIO()
    try:
        with redirect_stdout(f):
            print(exec(compile(query, '<string>', 'exec')))
            output = f.getvalue()[0:-6]

    except KeyError as e:
        print(textwrap.dedent(f'''\
            jello:  Key does not exist: {e}
        '''), file=sys.stderr)
        sys.exit(1)

    except IndexError as e:
        print(textwrap.dedent(f'''\
            jello:  {e}
        '''), file=sys.stderr)
        sys.exit(1)

    except SyntaxError as e:
        print(textwrap.dedent(f'''\
            jello:  {e}
                    {e.text}
        '''), file=sys.stderr)
        sys.exit(1)

    except TypeError as e:
        if output is None:
            output = ''
        else:
            print(textwrap.dedent(f'''\
                jello:  TypeError: {e}
            '''), file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(textwrap.dedent(f'''\
            jello:  Query Exception: {e}
                    _: {_}
                    query: {query}
                    output: {output}
        '''), file=sys.stderr)
        sys.exit(1)

    return output


def load_json(data):
    # replace newline characters in the input text with unicode separator \u2063
    data = data.strip().replace(r'\n', '\u2063')

    # load the JSON or JSON Lines data
    try:
        json_dict = json.loads(data)

    except Exception:
        # if json.loads fails, assume the data is json lines and parse
        data = data.splitlines()
        data_list = []
        for i, jsonline in enumerate(data):
            try:
                entry = json.loads(jsonline)
                data_list.append(entry)
            except Exception as e:
                # can't parse the data. Throw a nice message and quit
                print(textwrap.dedent(f'''\
                    jello:  JSON Load Exception: {e}
                            Cannot parse line {i + 1} (Not JSON or JSON Lines data):
                            {str(jsonline)[:70]}
                    '''), file=sys.stderr)
                sys.exit(1)

        json_dict = data_list

    return json_dict


def main():
    # break on ctrl-c keyboard interrupt
    signal.signal(signal.SIGINT, ctrlc)
    stdin = get_stdin()
    # for debugging
    # stdin = r'''["word", null, false, 1, 3.14, true, "multiple words", false, "words\nwith\nnewlines", 42]'''

    query = 'r = _'

    options = []
    long_options = {}
    for arg in sys.argv[1:]:
        if arg.startswith('-') and not arg.startswith('--'):
            options.extend(arg[1:])

        elif arg.startswith('--'):
            try:
                k, v = arg[2:].split('=')
                long_options[k] = int(v)
            except Exception:
                helptext()

        else:
            query = arg

    compact = 'c' in options
    lines = 'l' in options
    nulls = 'n' in options
    raw = 'r' in options
    version_info = 'v' in options
    helpme = 'h' in options

    if helpme:
        helptext()

    if version_info:
        print_error(f'jello:   version {__version__}\n')

    if stdin is None:
        print_error('jello:  missing piped JSON or JSON Lines data\n')

    list_dict_data = load_json(stdin)
    raw_response = pyquery(list_dict_data, query)
    normalized_response = normalize(raw_response, raw=raw, nulls=nulls)
    output = create_json(normalized_response, compact=compact, nulls=nulls, raw=raw, lines=lines)
    print(output.rstrip())


if __name__ == '__main__':
    main()
