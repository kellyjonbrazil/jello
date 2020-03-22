#!/usr/bin/env python3
"""jpyq - query JSON at the command line with python syntax"""

import sys
import textwrap
import json
import signal
from contextlib import redirect_stdout
import io
import ast


__version__ = '0.1.0'


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
        jpyq:   query JSON at the command line with python syntax

        Usage:  <JSON Data> | jpyq [OPTIONS] QUERY

                -p    pretty print
                -v    version info
                -h    help
    '''))


def print_error(message):
    """print error messages to STDERR and quit with error code"""
    print(message, file=sys.stderr)
    sys.exit(1)


def print_json(data, pretty=False):
    if isinstance(data, (list, dict)):
        if pretty:
            print(json.dumps(data, indent=2))
        else:
            print(json.dumps(data))
    else:
        print(data)


def pyquery(data, query):
    _ = None
    result = None

    try:
        _ = json.loads(data)
    except Exception as e:
        print(f'jpyq:  Not JSON Data: {e}')

    # get single statement results
    f = io.StringIO()
    with redirect_stdout(f):
        eval(compile(query, '<string>', 'single'))

    output = f.getvalue()[0:-1]

    result_list = []
    try:
        if len(output.splitlines()) == 1:
            try:
                result = ast.literal_eval(output)
            except Exception:
                # if exception then it was not a list or dict
                result = output.lstrip("'").rstrip("'")
        else:
            for entry in output.splitlines():
                try:
                    result_list.append(ast.literal_eval(entry))
                except Exception:
                    # if exception then it was not a list or dict
                    result_list.append(entry.lstrip("'").rstrip("'"))

    except Exception as e:
        print(e)

    if result_list:
        result = result_list

    # f = io.StringIO()
    # with redirect_stdout(f):
        # code_block = (compile(query, '<string>', 'exec'))
        # print(exec(code_block))
        # if r: print(r)

    # Above prints result to stdout and returns None. Need to capture stdout and ignore None
    # then turn the stdout string result into a dictionary:
    # dict_string = f.getvalue()[0:-6]

    # result_list = []
    # try:
    #     result = ast.literal_eval(dict_string)
        # if type(result) is not list:
        #     result_list.append(result)
        #     result = result_list

    # except Exception as e:
    #     # if json.loads fails, assume the data is formatted as json lines and parse
    #     result_list = []
    #     for dict_line in dict_string.splitlines():
    #         try:
    #             result = ast.literal_eval(dict_line)
    #             result_list.append(result)
    #         except Exception as e:
    #             # can't parse the data. Throw a nice message and quit
    #             return (textwrap.dedent(f'''\
    #                 jpyq:  Exception - {e}
    #                 {dict_line}'''))
    #     result = result_list

    # '\n'.join(f.getvalue().splitlines()[0:-1]).lstrip('"').rstrip('"')
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

    pretty = 'p' in options
    # version_info = 'v' in options
    # helpme = 'h' in options

    result = pyquery(stdin, query)

    print_json(result, pretty=pretty)


if __name__ == '__main__':
    main()
