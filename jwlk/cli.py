#!/usr/bin/env python3
"""jwlk - query JSON at the command line with python syntax"""

import sys
import textwrap
import json
import signal
from contextlib import redirect_stdout
import io
import ast
# import munch

__version__ = '0.1.3'


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
        jwlk:   query JSON at the command line with python syntax

        Usage:  <JSON Data> | jwlk [OPTIONS] QUERY

                -c    compact JSON output
                -s    slurp items into an array
                -v    version info
                -h    help

        Use '_' as the input data and assign the result to 'r'. Use python dict syntax.

        Example:
                <JSON Data> | jwlk 'r = _["foo"]'
    '''))


def print_error(message):
    """print error messages to STDERR and quit with error code"""
    print(message, file=sys.stderr)
    sys.exit(1)


def print_json(data, compact=False):
    # if isinstance(data, munch.Munch):
    #     data = munch.unmunchify(data)

    if isinstance(data, (list, dict)):
        if compact:
            print(json.dumps(data))
        else:
            print(json.dumps(data, indent=2))
    else:
        print(data)


def execute(data, slurp=False):
    result = None
    result_list = []
    try:
        if len(data.splitlines()) == 1:
            try:
                result = ast.literal_eval(data)
            except Exception:
                # if exception then it was not a list or dict
                result = data.lstrip("'").rstrip("'")
        else:
            for entry in data.splitlines():
                try:
                    result_list.append(ast.literal_eval(entry))
                except Exception:
                    # if exception then it was not a list or dict
                    result_list.append(entry.lstrip("'").rstrip("'"))

    except Exception as e:
        print(e)
        sys.exit(1)

    if result_list:
        if slurp:
            result = result_list
        else:
            if isinstance(result_list[0], (dict, list)):
                list_of_objs = []
                for obj in result_list:
                    list_of_objs.append(json.dumps(obj))
                result = '\n'.join(list_of_objs)
            else:
                result = '\n'.join(result_list)

    return result


def pyquery(data, query, slurp=False):
    _ = None
    result = None
    query = 'r = None\n' + query + '\nprint(r)'

    try:
        json_dict = json.loads(data)
    except Exception as e:
        print(f'jwlk:  Not JSON Data: {e}')
        sys.exit(1)

    _ = json_dict

    f = io.StringIO()
    with redirect_stdout(f):
        print(exec(compile(query, '<string>', 'exec')))
        output = f.getvalue()[0:-6]

    result = execute(output, slurp=slurp)

    return result


def main():
    # break on ctrl-c keyboard interrupt
    signal.signal(signal.SIGINT, ctrlc)

    stdin = get_stdin()

    query = '_'

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
    slurp = 's' in options
    version_info = 'v' in options
    helpme = 'h' in options

    if helpme:
        helptext()

    if version_info:
        print_error(f'jwlk:   version {__version__}\n')

    result = pyquery(stdin, query, slurp=slurp)

    print_json(result, compact=compact)


if __name__ == '__main__':
    main()
