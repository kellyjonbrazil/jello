#!/usr/bin/env python3
"""jello - query JSON at the command line with python syntax"""

import os
import sys
import platform
import textwrap
import json
import signal
import ast
from pygments import highlight
from pygments.style import Style
from pygments.token import (Name, Number, String, Keyword)
from pygments.lexers import JsonLexer
from pygments.formatters import Terminal256Formatter

__version__ = '1.2.0'


class JelloStyle(Style):
    BLUE = '#2c5dcd'
    GRAY = '#4d4d4d'
    PURPLE = '#5918bb'
    GREEN = '#00cc00'

    styles = {
        Name.Tag: f'bold {BLUE}',     # key names
        Keyword: GRAY,                # true, false, null
        Number: PURPLE,               # int, float
        String: GREEN                 # string
    }


def ctrlc(signum, frame):
    """exit with error on SIGINT"""
    sys.exit(1)


def get_stdin():
    """return STDIN data"""
    if sys.stdin.isatty():
        return None
    else:
        return sys.stdin.read()


def stdout_is_tty():
    """returns True if stdout is a TTY. False if output is being piped to another program"""
    if sys.stdout.isatty():
        return True
    else:
        return False


def helptext():
    print_error(textwrap.dedent('''\
        jello:   query JSON at the command line with python syntax

        Usage:  <JSON Data> | jello [OPTIONS] [QUERY]

                -c   compact JSON output
                -i   initialize environment with .jelloconf.py in ~ (linux) or %appdata% (Windows)
                -l   output as lines suitable for assignment to a bash array
                -m   monochrome output
                -n   print selected null values
                -r   raw string output (no quotes)
                -s   print the JSON schema in grep-able format
                -v   version info
                -h   help

        Use '_' as the input data and use python dict and list syntax.

        Example:
                <JSON Data> | jello '_["foo"]'
                variable=($(cat data.json | jello -l '_["foo"]'))
    '''))


def print_schema(src, path='', mono=False):
    """prints a grep-able schema representation of the JSON"""
    CEND = '\33[0m'
    CBLUE = '\33[34m'
    CGREEN = '\33[32m'
    CVIOLET = '\33[35m'
    CGRAY = '\33[90m'
    if isinstance(src, list) and path == '':
        for i, item in enumerate(src):
            if not mono:
                i = f'{CBLUE}{i}{CEND}'
            print_schema(item, path=f'.{i}', mono=mono)

    elif isinstance(src, list):
        for i, item in enumerate(src):
            if not mono:
                src = f'{CBLUE}{src}{CEND}'
                i = f'{CBLUE}{i}{CEND}'
            print_schema(item, path=f'{path}.{src}.{i}', mono=mono)

    elif isinstance(src, dict):
        for k, v in src.items():
            if isinstance(v, list):
                for i, item in enumerate(v):
                    if not mono:
                        k = f'{CBLUE}{k}{CEND}'
                        i = f'{CBLUE}{i}{CEND}'
                    print_schema(item, path=f'{path}.{k}.{i}', mono=mono)

            elif isinstance(v, dict):
                if not mono:
                    k = f'{CBLUE}{k}{CEND}'
                print_schema(v, path=f'{path}.{k}', mono=mono)

            else:
                if not mono:
                    k = f'{CBLUE}{k}{CEND}'
                    val = json.dumps(v)
                    if val == 'true' or val == 'false' or val == 'null':
                        val = f'{CGRAY}{val}{CEND}'
                    elif val.replace('.', '', 1).isdigit():
                        val = f'{CVIOLET}{val}{CEND}'
                    else:
                        val = f'{CGREEN}{val}{CEND}'
                else:
                    val = json.dumps(v)
                print(f'{path}.{k} = {val}')

    else:
        if not mono:
            val = json.dumps(src)
            if val == 'true' or val == 'false' or val == 'null':
                val = f'{CGRAY}{val}{CEND}'
            elif val.replace('.', '', 1).isdigit():
                val = f'{CVIOLET}{val}{CEND}'
            else:
                val = f'{CGREEN}{val}{CEND}'
        else:
            val = json.dumps(src)
        print(f'{path} = {val}')


def print_error(message):
    """print error messages to STDERR and quit with error code"""
    print(message, file=sys.stderr)
    sys.exit(1)


def create_json(data, compact=None, nulls=None, raw=None, lines=None):
    if isinstance(data, dict):
        if compact or lines:
            return json.dumps(data)
        else:
            return json.dumps(data, indent=2)

    if isinstance(data, list):
        if not lines:
            if compact:
                return json.dumps(data)
            else:
                return json.dumps(data, indent=2)

        # check if this list includes lists
        list_includes_list = False
        for item in data:
            if isinstance(item, list):
                list_includes_list = True
                break

        if lines and list_includes_list:
            print_error('jello:  Cannot print list of lists as lines. Try normal JSON output.\n')

        # print lines for a flat list
        else:
            flat_list = ''
            for entry in data:
                if entry is None:
                    if nulls:
                        flat_list += 'null\n'
                    else:
                        flat_list += '\n'

                elif isinstance(entry, (dict, bool, int, float)):
                    flat_list += json.dumps(entry) + '\n'

                elif isinstance(entry, str):
                    # replace \n with \\n here so lines with newlines literally print the \n char
                    entry = entry.replace('\n', '\\n')
                    if raw:
                        flat_list += f'{entry}' + '\n'
                    else:
                        flat_list += f'"{entry}"' + '\n'

            return flat_list.rstrip()

    # naked single item return case
    elif data is None:
        if nulls:
            return 'null'
        else:
            return ''

    elif isinstance(data, (bool, int, float)):
        return json.dumps(data)

    elif isinstance(data, str):
        # replace \n with \\n here so lines with newlines literally print the \n char
        data = data.replace('\n', '\\n')
        if raw:
            return f'{data}'
        else:
            return f'"{data}"'


def pyquery(data, query, initialize=None, compact=None, nulls=None, raw=None, lines=None, mono=None, schema=None):
    _ = data
    jelloconf = ''

    if initialize:
        if platform.system() == 'Windows':
            conf_file = os.path.join(os.environ['APPDATA'], '.jelloconf.py')
        else:
            conf_file = os.path.join(os.environ["HOME"], '.jelloconf.py')

        try:
            with open(conf_file, 'r') as f:
                jelloconf = f.read()
        except FileNotFoundError:
            print_error(textwrap.dedent(f'''\
                jello:  Initialization file not found: {conf_file}
            '''))

    query = jelloconf + query
    output = None

    try:
        # extract jello options from .jelloconf.py (compact, raw, lines, nulls, mono)
        for expr in ast.parse(jelloconf).body:
            if isinstance(expr, ast.Assign):
                if expr.targets[0].id == 'compact':
                    compact = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
                if expr.targets[0].id == 'raw':
                    raw = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
                if expr.targets[0].id == 'lines':
                    lines = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
                if expr.targets[0].id == 'nulls':
                    nulls = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
                if expr.targets[0].id == 'mono':
                    mono = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
                if expr.targets[0].id == 'schema':
                    schema = eval(compile(ast.Expression(expr.value), '<string>', "eval"))

        # run the query
        block = ast.parse(query, mode='exec')
        last = ast.Expression(block.body.pop().value)    # assumes last node is an expression
        exec(compile(block, '<string>', mode='exec'))
        output = eval(compile(last, '<string>', mode='eval'))

        # need to return compact, nulls, raw, lines, mono, schema in case they were changed in .jelloconf.py
        return (output, compact, nulls, raw, lines, mono, schema)

    except KeyError as e:
        print_error(textwrap.dedent(f'''\
            jello:  Key does not exist: {e}
        '''))

    except IndexError as e:
        print_error(textwrap.dedent(f'''\
            jello:  {e}
        '''))

    except SyntaxError as e:
        print_error(textwrap.dedent(f'''\
            jello:  {e}
                    {e.text}
        '''))

    except TypeError as e:
        print_error(textwrap.dedent(f'''\
            jello:  TypeError: {e}
        '''))

    except AttributeError as e:
        print_error(textwrap.dedent(f'''\
            jello:  AttributeError: {e}
        '''))

    except NameError as e:
        print_error(textwrap.dedent(f'''\
            jello:  NameError: {e}
        '''))

    except Exception as e:
        print_error(textwrap.dedent(f'''\
            jello:  Query Exception: {e}
                    _: {_}
                    query: {query}
                    output: {output}
        '''))


def load_json(data):
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
                # can't parse the data. Throw an error and quit
                print_error(textwrap.dedent(f'''\
                    jello:  JSON Load Exception: {e}
                            Cannot parse line {i + 1} (Not JSON or JSON Lines data):
                            {str(jsonline)[:70]}
                    '''))

        json_dict = data_list

    return json_dict


def main(data=None, query='_', initialize=None, version_info=None, helpme=None, compact=None,
         nulls=None, raw=None, lines=None, mono=None, schema=None):
    # break on ctrl-c keyboard interrupt
    signal.signal(signal.SIGINT, ctrlc)

    commandline = False
    if data is None:
        commandline = True
        data = get_stdin()
    # for debugging
    # data = r'''["word", null, false, 1, 3.14, true, "multiple words", false, "words\nwith\nnewlines", 42]'''

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
            if commandline:
                query = arg

    compact = compact if not commandline else'c' in options
    initialize = initialize if not commandline else 'i' in options
    lines = lines if not commandline else 'l' in options
    mono = mono if not commandline else 'm' in options
    nulls = nulls if not commandline else 'n' in options
    raw = raw if not commandline else 'r' in options
    schema = schema if not commandline else 's' in options
    version_info = version_info if not commandline else 'v' in options
    helpme = helpme if not commandline else 'h' in options

    if helpme:
        helptext()

    if version_info:
        print_error(f'jello:   version {__version__}\n')

    if data is None:
        print_error('jello:  missing piped JSON or JSON Lines data\n')

    # lines() function is deprecated. Warn and quit if detected.
    if query and 'lines(' in query:
        print_error('jello:  Error: lines() function is deprecated. Please use the -l option instead.\n')

    list_dict_data = load_json(data)

    # pulling variables back from pyquery since the user may have defined intialization options
    # in their .jelloconf.py file
    response, compact, nulls, raw, lines, mono, schema = pyquery(list_dict_data, query, initialize=initialize,
                                                                 compact=compact, nulls=nulls, raw=raw, lines=lines,
                                                                 mono=mono, schema=schema)

    if schema:
        if not stdout_is_tty():
            mono = True
        print_schema(response, mono=mono)
        exit()
    else:
        output = create_json(response, compact=compact, nulls=nulls, raw=raw, lines=lines)

    try:
        if commandline:
            if not mono and not lines and stdout_is_tty():
                print(highlight(output, JsonLexer(), Terminal256Formatter(style=JelloStyle))[0:-1])
            else:
                print(output)
        else:
            return output

    except Exception as e:
        print_error(textwrap.dedent(f'''\
            jello:  Output Exception:  {e}
                    list_dict_data: {list_dict_data}
                    response: {response}
                    output: {output}
        '''))


if __name__ == '__main__':
    main()
