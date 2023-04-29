"""jello - query JSON at the command line with python syntax"""

import os
import sys
import signal
import shutil
import textwrap
from textwrap import TextWrapper
import jello
from jello.lib import opts, load_json, read_file, pyquery, Schema, Json


def ctrlc(signum, frame):
    """exit with error on SIGINT"""
    sys.exit(1)


def get_stdin():
    """return STDIN data"""
    if sys.stdin.isatty():
        return None
    else:
        return sys.stdin.read()


def print_help():
    print(textwrap.dedent('''\
        jello:  query JSON at the command line with python syntax

        Usage:  cat data.json | jello [OPTIONS] [QUERY | -q <query_file>]
                jello [OPTIONS] [QUERY | -q <query_file>] [-f <input_files>]

                -c   compact JSON output
                -C   force color output even when using pipes (overrides -m)
                -e   empty data (don't process data from STDIN or file)
                -f   load input data from JSON file or JSON Lines files
                -i   initialize environment with .jelloconf.py
                     located at ~ (linux) or %appdata% (Windows)
                -l   output as lines suitable for assignment to a bash array
                -m   monochrome output
                -n   print selected null values
                -q   load query from a file
                -r   raw string output (no quotes)
                -s   print the JSON schema in grep-able format
                -t   print type annotations in schema view
                -v   version info
                -h   help

        Use '_' as the input data and use python dict and list bracket syntax
        or dot notation to filter the results and/or rebuild the output.

        Examples:
                cat data.json | jello _.foo
                jello _.foo -f data.json
                jello '_["foo"]' -f data.json
                variable=($(cat data.json | jello -l _.foo))
    '''))
    sys.exit()


def print_error(message):
    """print error messages to STDERR and quit with error code"""
    print(message, file=sys.stderr)
    sys.exit(1)


def print_exception(e=None, data='', query='', response='', ex_type='Runtime'):
    exception_message = ''
    term_width = shutil.get_terminal_size().columns or 80
    split_length = int(term_width)
    if split_length < 10:
        split_length = 10

    wrapper = TextWrapper(width=term_width,
                                initial_indent='',
                                subsequent_indent=' ' * 12)
    exception_message = wrapper.fill(f'jello:  {ex_type} Exception:  {e.__class__.__name__}') + '\n'

    wrapper = TextWrapper(width=term_width,
                          initial_indent=' ' * 8,
                          subsequent_indent=' ' * 12)
    exception_message += wrapper.fill(f'{e}') + '\n'

    e_text = ''
    if hasattr(e, 'text'):
        e_text = str(e.text).replace('\n', '')

    detail = {
        f'{e.__class__.__name__}': e_text,
        'query': str(query).replace('\n', '\\n'),
        'data': str(data).replace('\n', '\\n'),
        'response': str(response).replace('\n', '\\n')
    }

    for item in detail:
        if len(detail[item]) > (split_length * 2) + 10:
            detail[item] = f'{item}:  {detail[item][:split_length]} ... {detail[item][-split_length:]}'
        elif detail[item]:
            detail[item] = f'{item}:  {detail[item]}'

        if detail[item]:
            detail[item] = wrapper.fill(detail[item])
            exception_message += f'{detail[item]}' + '\n'

    print(exception_message, file=sys.stderr)
    sys.exit(1)


def main(data=None, query='_'):
    # break on ctrl-c keyboard interrupt
    signal.signal(signal.SIGINT, ctrlc)

    # break on pipe error. need try/except for windows compatibility
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except AttributeError:
        pass

    # enable colors for Windows cmd.exe terminal
    if sys.platform.startswith('win32'):
        os.system('')

    if data is None:
        data = get_stdin()

    options = []
    long_options = {}
    arg_section = ''  # can be query_file or data_files

    for arg in sys.argv[1:]:
        if arg == '-q':
            arg_section = 'query_file'

        elif arg == '-f':
            data = ''
            arg_section = 'data_files'

        elif arg_section == 'query_file':
            try:
                query = read_file(arg)
            except Exception as e:
                print_error(f'jello:  Issue reading query file: {e}')
            finally:
                arg_section = ''

        elif arg_section == 'data_files':
            try:
                data += '\n' + read_file(arg)
            except Exception as e:
                print_error(f'jello:  Issue reading data file: {e}')

        elif arg.startswith('-') and not arg.startswith('--'):
             options.extend(arg[1:])
             arg_section = ''

        elif arg.startswith('--'):
            try:
                k, v = arg[2:].split('=')
                long_options[k] = int(v)
                arg_section = ''
            except Exception:
                print_help()

        else:
            query = arg
            arg_section = ''

    opts.compact = opts.compact or 'c' in options
    opts.initialize = opts.initialize or 'i' in options
    opts.lines = opts.lines or 'l' in options
    opts.empty = opts.empty or 'e' in options
    opts.force_color = opts.force_color or 'C' in options
    opts.mono = opts.mono or ('m' in options or bool(os.getenv('NO_COLOR')))
    opts.nulls = opts.nulls or 'n' in options
    opts.raw = opts.raw or 'r' in options
    opts.schema = opts.schema or 's' in options
    opts.types = opts.types or 't' in options
    opts.version_info = opts.version_info or 'v' in options
    opts.helpme = opts.helpme or 'h' in options

    if opts.helpme:
        print_help()

    if opts.version_info:
        print(textwrap.dedent(f'''\
            jello:  Version: {jello.__version__}
                    Author: {jello.AUTHOR}
                    Website: {jello.WEBSITE}
                    Copyright: {jello.COPYRIGHT}
                    License: {jello.LICENSE}
        '''))
        sys.exit()

    if data is None and not opts.empty:
        print_error('jello:  Missing JSON or JSON Lines data via STDIN or file via -f option.\n')

    if opts.empty:
        data = '{}'

    # load the JSON or JSON Lines into a dict or list of dicts
    try:
        data = load_json(data)
    except Exception as e:
        print_exception(e, ex_type='JSON Load')

    # Read .jelloconf.py (if it exists) and run the query
    response = ''
    try:
        response = pyquery(data, query)
    except Exception as e:
        print_exception(e, data, query, ex_type='Query')

    # reset opts.mono after pyquery since initialization in pyquery can change values
    if opts.force_color:
        opts.mono = False

    # Create and print schema or JSON/JSON-Lines/Lines
    output = ''
    try:
        if opts.schema:
            schema = Schema()
            output = schema.create_schema(response)

            if not opts.mono and (sys.stdout.isatty() or opts.force_color):
                schema.set_colors()
                output = schema.color_output(output)

        else:
            json_out = Json()
            output = json_out.create_json(response)

            if (not opts.mono and not opts.raw) and (sys.stdout.isatty() or opts.force_color):
                json_out.set_colors()
                output = json_out.color_output(output)

        print(output)

    except Exception as e:
        print_exception(e, data, query, response, ex_type='Output')


if __name__ == '__main__':
    main()
