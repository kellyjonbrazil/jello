"""jello - query JSON at the command line with python syntax"""

import os
import sys
import textwrap
import signal
from pygments import highlight
from pygments.style import Style
from pygments.token import (Name, Number, String, Keyword)
from pygments.lexers import JsonLexer
from pygments.formatters import Terminal256Formatter
import jello
from jello.lib import opts, JelloTheme, set_env_colors, load_json, create_schema, create_json, pyquery


def ctrlc(signum, frame):
    """exit with error on SIGINT"""
    sys.exit(1)


def get_stdin():
    """return STDIN data"""
    if sys.stdin.isatty():
        return None
    else:
        return sys.stdin.read()


def print_error(message):
    """print error messages to STDERR and quit with error code"""
    print(message, file=sys.stderr)
    sys.exit(1)


def helptext():
    print(textwrap.dedent('''\
        jello:  query JSON at the command line with python syntax

        Usage:  cat data.json | jello [OPTIONS] [QUERY]

                -c   compact JSON output
                -i   initialize environment with .jelloconf.py in ~ (linux) or %appdata% (Windows)
                -l   output as lines suitable for assignment to a bash array
                -m   monochrome output
                -n   print selected null values
                -r   raw string output (no quotes)
                -s   print the JSON schema in grep-able format
                -v   version info
                -h   help

        Use '_' as the input data and use python dict and list bracket syntax or dot notation.

        Examples:
                cat data.json | jello _.foo
                cat data.json | jello '_["foo"]'
                variable=($(cat data.json | jello -l _.foo))
    '''))
    sys.exit()


def format_exception(e=None, list_dict_data='', query='', response='', output=''):
    list_dict_data = str(list_dict_data).replace('\n', '\\n')
    query = str(query).replace('\n', '\\n')
    response = str(response).replace('\n', '\\n')
    output = str(output).replace('\n', '\\n')
    e_text = ''

    if hasattr(e, 'text'):
        e_text = e.text

    if len(str(list_dict_data)) > 70:
        list_dict_data = str(list_dict_data)[:34] + ' ... ' + str(list_dict_data)[-34:]

    if len(str(query)) > 70:
        query = str(query)[:34] + ' ... ' + str(query)[-34:]

    if len(str(response)) > 70:
        response = str(response)[:34] + ' ... ' + str(response)[-34:]

    if len(str(output)) > 70:
        output = str(output)[0:34] + ' ... ' + str(output)[-34:]

    return e, e_text, list_dict_data, query, response, output


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

    opts.compact = opts.compact or 'c' in options
    opts.initialize = opts.initialize or 'i' in options
    opts.lines = opts.lines or 'l' in options
    opts.mono = opts.mono or 'm' in options
    opts.nulls = opts.nulls or 'n' in options
    opts.raw = opts.raw or 'r' in options
    opts.schema = opts.schema or 's' in options
    opts.version_info = opts.version_info or 'v' in options
    opts.helpme = opts.helpme or 'h' in options

    if opts.helpme:
        helptext()

    if opts.version_info:
        print(textwrap.dedent(f'''\
            jello:   Version: {jello.__version__}
                     Author: {jello.AUTHOR}
                     Website: {jello.WEBSITE}
                     Copyright: {jello.COPYRIGHT}
                     License: {jello.LICENSE}
        '''))
        sys.exit()

    if data is None:
        print_error('jello:  missing piped JSON or JSON Lines data\n')

    # only process if there is data
    if data and not data.isspace():

        # load the JSON or JSON Lines
        list_dict_data = None
        try:
            list_dict_data = load_json(data)
        except Exception as e:
            # can't parse the data. Throw an error and quit
            msg = f'''JSON Load Exception: {e}
        Cannot parse the data (Not valid JSON or JSON Lines)
        '''
            print_error(f'''jello:  {msg}''')

        # run the query and check for various errors
        response = ''
        try:
            response = pyquery(list_dict_data, query)

        except Exception as e:
            e, e_text, list_dict_data, query, response, output = format_exception(e,
                                                                                  list_dict_data,
                                                                                  query)

            print_error(textwrap.dedent(f'''\
                jello:  Query Exception:  {e.__class__.__name__}
                        {e}
                        {e_text}
                        query: {query}
                        data: {list_dict_data}
            '''))

        set_env_colors()

        # output as a schema if the user desires, otherwise generate JSON or Lines
        output = ''
        try:
            if opts.schema:
                if not sys.stdout.isatty():
                    opts.mono = True
                create_schema(response)
                print('\n'.join(jello.lib.schema_list))
                sys.exit()
            else:
                output = create_json(response)

        except Exception as e:
            e, e_text, list_dict_data, query, response, output = format_exception(e,
                                                                                  list_dict_data,
                                                                                  query,
                                                                                  response)

            print_error(textwrap.dedent(f'''\
                jello:  Formatting Exception:  {e.__class__.__name__}
                        {e}
                        {e_text}
                        query: {query}
                        data: {list_dict_data}
                        response: {response}
            '''))

        # Print colorized or mono JSON to STDOUT
        try:
            if not opts.mono and not opts.raw and sys.stdout.isatty():
                # create JelloStyle class with user values from set_env_colors() or default values
                # need to do this here (not at global level), otherwise default values will not be updated
                class JelloStyle(Style):
                    styles = {
                        Name.Tag: f'bold {JelloTheme.colors["key_name"][0]}',   # key names
                        Keyword: f'{JelloTheme.colors["keyword"][0]}',          # true, false, null
                        Number: f'{JelloTheme.colors["number"][0]}',            # int, float
                        String: f'{JelloTheme.colors["string"][0]}'             # string
                    }

                lexer = JsonLexer()
                formatter = Terminal256Formatter(style=JelloStyle)
                highlighted_json = highlight(output, lexer, formatter)
                print(highlighted_json[0:-1])
            else:
                print(output)

        except Exception as e:
            e, e_text, list_dict_data, query, response, output = format_exception(e,
                                                                                  list_dict_data,
                                                                                  query,
                                                                                  response,
                                                                                  output)

            print_error(textwrap.dedent(f'''\
                jello:  Output Exception:  {e.__class__.__name__}
                        {e}
                        {e_text}
                        query: {query}
                        data: {list_dict_data}
                        response: {response}
                        output: {output}
            '''))


if __name__ == '__main__':
    main()
