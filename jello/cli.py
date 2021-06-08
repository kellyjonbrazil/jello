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
from jello.dotmap import DotMap


__version__ = '1.3.0'
AUTHOR = 'Kelly Brazil'
WEBSITE = 'https://github.com/kellyjonbrazil/jello'
COPYRIGHT = '© 2020-2021 Kelly Brazil'
LICENSE = 'MIT License'

color_map = {
    'black': ('ansiblack', '\33[30m'),
    'red': ('ansired', '\33[31m'),
    'green': ('ansigreen', '\33[32m'),
    'yellow': ('ansiyellow', '\33[33m'),
    'blue': ('ansiblue', '\33[34m'),
    'magenta': ('ansimagenta', '\33[35m'),
    'cyan': ('ansicyan', '\33[36m'),
    'gray': ('ansigray', '\33[37m'),
    'brightblack': ('ansibrightblack', '\33[90m'),
    'brightred': ('ansibrightred', '\33[91m'),
    'brightgreen': ('ansibrightgreen', '\33[92m'),
    'brightyellow': ('ansibrightyellow', '\33[93m'),
    'brightblue': ('ansibrightblue', '\33[94m'),
    'brightmagenta': ('ansibrightmagenta', '\33[95m'),
    'brightcyan': ('ansibrightcyan', '\33[96m'),
    'white': ('ansiwhite', '\33[97m'),
}


class opts:
    initialize = None
    version_info = None
    helpme = None
    compact = None
    nulls = None
    raw = None
    lines = None
    mono = None
    schema = None
    keyname_color = None
    keyword_color = None
    number_color = None
    string_color = None
    arrayid_color = None
    arraybracket_color = None


schema_list = []


class JelloTheme:
    """this class will contain the colors dictionary generated from set_env_colors()"""
    pass


def set_env_colors():
    """
    This function does not return a value. It just updates the JelloTheme.colors dictionary.

    Grab custom colors from JELLO_COLORS environment variable and .jelloconf.py file. Individual colors from JELLO_COLORS
    take precedence over .jelloconf.py. Individual colors from JELLO_COLORS will fall back to .jelloconf.py or default
    if the env variable color is set to 'default'

    JELLO_COLORS env variable takes 6 comma separated string values and should be in the format of:

    JELLO_COLORS=<keyname_color>,<keyword_color>,<number_color>,<string_color>,<arrayid_color>,<arraybracket_color>

    Where colors are: black, red, green, yellow, blue, magenta, cyan, gray, brightblack, brightred,
                      brightgreen, brightyellow, brightblue, brightmagenta, brightcyan, white, default

    Default colors:

    JELLO_COLORS=blue,brightblack,magenta,green,red,magenta
    or
    JELLO_COLORS=default,default,default,default,default,default

    """
    env_colors = os.getenv('JELLO_COLORS')
    input_error = False

    if env_colors:
        color_list = env_colors.split(',')
    else:
        input_error = True

    if env_colors and len(color_list) != 6:
        input_error = True

    if env_colors:
        for color in color_list:
            if color not in ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'gray', 'brightblack', 'brightred',
                             'brightgreen', 'brightyellow', 'brightblue', 'brightmagenta', 'brightcyan', 'white', 'default']:
                input_error = True

    # if there is an issue with the env variable, just set all colors to default and move on
    if input_error:
        print('jello:   Warning: could not parse JELLO_COLORS environment variable\n', file=sys.stderr)
        color_list = ['default', 'default', 'default', 'default', 'default', 'default']

    # Try the color set in the JELLO_COLORS env variable first. If it is set to default, then fall back to .jelloconf.py
    # configuration. If nothing is set in jelloconf.py, then use the default colors.
    JelloTheme.colors = {
        'key_name': color_map[color_list[0]] if not color_list[0] == 'default' else color_map[opts.keyname_color] if opts.keyname_color else color_map['blue'],
        'keyword': color_map[color_list[1]] if not color_list[1] == 'default' else color_map[opts.keyword_color] if opts.keyword_color else color_map['brightblack'],
        'number': color_map[color_list[2]] if not color_list[2] == 'default' else color_map[opts.number_color] if opts.number_color else color_map['magenta'],
        'string': color_map[color_list[3]] if not color_list[3] == 'default' else color_map[opts.string_color] if opts.string_color else color_map['green'],
        'array_id': color_map[color_list[4]] if not color_list[4] == 'default' else color_map[opts.arrayid_color] if opts.arrayid_color else color_map['red'],
        'array_bracket': color_map[color_list[5]] if not color_list[5] == 'default' else color_map[opts.arraybracket_color] if opts.arraybracket_color else color_map['magenta']
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

        Example:
                cat data.json | jello _.foo
                cat data.json | jello '_["foo"]'
                variable=($(cat data.json | jello -l _.foo))
    '''))
    sys.exit()


def create_schema(src, path=''):
    """
    Creates a grep-able schema representation of the JSON.

    This function is recursive, so output is stored within the schema_list list. Make sure to
    initialize schema_list to a blank list and set colors by calling set_env_colors() before
    calling this function.
    """
    if not opts.mono:
        CEND = '\33[0m'
        CBOLD = '\33[1m'
        CKEYNAME = f'{JelloTheme.colors["key_name"][1]}'
        CKEYWORD = f'{JelloTheme.colors["keyword"][1]}'
        CNUMBER = f'{JelloTheme.colors["number"][1]}'
        CSTRING = f'{JelloTheme.colors["string"][1]}'
        CARRAYID = f'{JelloTheme.colors["array_id"][1]}'
        CARRAYBRACKET = f'{JelloTheme.colors["array_bracket"][1]}'

    else:
        CEND = ''
        CBOLD = ''
        CKEYNAME = ''
        CKEYWORD = ''
        CNUMBER = ''
        CSTRING = ''
        CARRAYID = ''
        CARRAYBRACKET = ''

    if isinstance(src, list) and path == '':
        for i, item in enumerate(src):
            create_schema(item, path=f'.{CARRAYBRACKET}[{CEND}{CARRAYID}{i}{CEND}{CARRAYBRACKET}]{CEND}')

    elif isinstance(src, list):
        for i, item in enumerate(src):
            create_schema(item, path=f'{path}.{CBOLD}{CKEYNAME}{src}{CEND}{CARRAYBRACKET}[{CEND}{CARRAYID}{i}{CEND}{CARRAYBRACKET}]{CEND}')

    elif isinstance(src, dict):
        for k, v in src.items():
            if isinstance(v, list):
                for i, item in enumerate(v):
                    create_schema(item, path=f'{path}.{CBOLD}{CKEYNAME}{k}{CEND}{CARRAYBRACKET}[{CEND}{CARRAYID}{i}{CEND}{CARRAYBRACKET}]{CEND}')

            elif isinstance(v, dict):
                if not opts.mono:
                    k = f'{CBOLD}{CKEYNAME}{k}{CEND}'
                create_schema(v, path=f'{path}.{k}')

            else:
                k = f'{CBOLD}{CKEYNAME}{k}{CEND}'
                val = json.dumps(v)
                if val == 'true' or val == 'false' or val == 'null':
                    val = f'{CKEYWORD}{val}{CEND}'
                elif val.replace('.', '', 1).isdigit():
                    val = f'{CNUMBER}{val}{CEND}'
                else:
                    val = f'{CSTRING}{val}{CEND}'

                schema_list.append(f'{path}.{k} = {val};')

    else:
        val = json.dumps(src)
        if val == 'true' or val == 'false' or val == 'null':
            val = f'{CKEYWORD}{val}{CEND}'
        elif val.replace('.', '', 1).isdigit():
            val = f'{CNUMBER}{val}{CEND}'
        else:
            val = f'{CSTRING}{val}{CEND}'

        path = path or '.'

        schema_list.append(f'{path} = {val};')


def create_json(data):
    separators = None
    indent = 2

    if opts.compact or opts.lines:
        separators = (',', ':')
        indent = None

    if isinstance(data, dict):
        return json.dumps(data, separators=separators, indent=indent, ensure_ascii=False)

    if isinstance(data, list):
        if not opts.lines:
            return json.dumps(data, separators=separators, indent=indent, ensure_ascii=False)

        # check if this list includes lists
        list_includes_list = False
        for item in data:
            if isinstance(item, list):
                list_includes_list = True
                break

        if opts.lines and list_includes_list:
            raise ValueError('Cannot print list of lists as lines. Try normal JSON output.\n')

        # print lines for a flat list
        else:
            flat_list = ''
            for entry in data:
                if entry is None:
                    if opts.nulls:
                        flat_list += 'null\n'
                    else:
                        flat_list += '\n'

                elif isinstance(entry, (dict, bool, int, float)):
                    flat_list += json.dumps(entry, separators=separators, ensure_ascii=False) + '\n'

                elif isinstance(entry, str):
                    # replace \n with \\n here so lines with newlines literally print the \n char
                    entry = entry.replace('\n', '\\n')
                    if opts.raw:
                        flat_list += f'{entry}' + '\n'
                    else:
                        flat_list += f'"{entry}"' + '\n'

            return flat_list.rstrip()

    # naked single item return case
    elif data is None:
        if opts.nulls:
            return 'null'
        else:
            return ''

    elif isinstance(data, (bool, int, float)):
        return json.dumps(data, ensure_ascii=False)

    elif isinstance(data, str):
        # replace \n with \\n here so lines with newlines literally print the \n char
        data = data.replace('\n', '\\n')
        if opts.raw:
            return f'{data}'
        else:
            return f'"{data}"'


def pyquery(data, query):
    # if data is a list of dictionaries, then need to iterate through and convert all dictionaries to DotMap
    if isinstance(data, list):
        _ = [DotMap(i, _dynamic=False, _prevent_method_masking=True) if isinstance(i, dict)
             else i for i in data]

    elif isinstance(data, dict):
        _ = DotMap(data, _dynamic=False, _prevent_method_masking=True)

    else:
        _ = data

    jelloconf = ''

    if opts.initialize:
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

    # extract jello options from .jelloconf.py (compact, raw, lines, nulls, mono, and custom colors)
    for expr in ast.parse(jelloconf).body:
        if isinstance(expr, ast.Assign):
            if expr.targets[0].id == 'compact':
                opts.compact = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
            if expr.targets[0].id == 'raw':
                opts.raw = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
            if expr.targets[0].id == 'lines':
                opts.lines = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
            if expr.targets[0].id == 'nulls':
                opts.nulls = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
            if expr.targets[0].id == 'mono':
                opts.mono = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
            if expr.targets[0].id == 'schema':
                opts.schema = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
            if expr.targets[0].id == 'keyname_color':
                opts.keyname_color = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
            if expr.targets[0].id == 'keyword_color':
                opts.keyword_color = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
            if expr.targets[0].id == 'number_color':
                opts.number_color = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
            if expr.targets[0].id == 'string_color':
                opts.string_color = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
            if expr.targets[0].id == 'arrayid_color':
                opts.arrayid_color = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
            if expr.targets[0].id == 'arraybracket_color':
                opts.arraybracket_color = eval(compile(ast.Expression(expr.value), '<string>', "eval"))

            # validate the data in the initialization file
            warn_options = False
            warn_colors = False

            for option in [opts.compact, opts.raw, opts.lines, opts.nulls, opts.mono, opts.schema]:
                if not isinstance(option, bool):
                    opts.compact = opts.raw = opts.lines = opts.nulls = opts.mono = opts.schema = None
                    warn_options = True

            for color_config in [opts.keyname_color, opts.keyword_color, opts.number_color,
                                 opts.string_color, opts.arrayid_color, opts.arraybracket_color]:
                valid_colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'gray', 'brightblack', 'brightred',
                                'brightgreen', 'brightyellow', 'brightblue', 'brightmagenta', 'brightcyan', 'white']
                if color_config not in valid_colors and color_config is not None:
                    opts.keyname_color = opts.keyword_color = opts.number_color = opts.string_color = opts.arrayid_color = opts.arraybracket_color = None
                    warn_colors = True

            if warn_options:
                print(f'Jello:   Warning: Options must be set to True or False in {conf_file}\n         Unsetting all options.\n')

            if warn_colors:
                valid_colors_string = ', '.join(valid_colors)
                print(f'Jello:   Warning: Colors must be set to one of: {valid_colors_string} in {conf_file}\n         Unsetting all colors.\n')

    # run the query
    block = ast.parse(query, mode='exec')
    last = ast.Expression(block.body.pop().value)    # assumes last node is an expression
    exec(compile(block, '<string>', mode='exec'))
    output = eval(compile(last, '<string>', mode='eval'))

    # convert output back to normal dict
    if isinstance(output, list):
        output = [i.toDict() if isinstance(i, DotMap) else i for i in output]

    elif isinstance(output, DotMap):
        output = output.toDict()

    return output


def load_json(data):
    try:
        json_dict = json.loads(data)
    except Exception:
        # if json.loads fails, assume the data is json lines and parse
        json_dict = [json.loads(i) for i in data.splitlines()]

    return json_dict


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
            jello:   Version: {__version__}
                     Author: {AUTHOR}
                     Website: {WEBSITE}
                     Copyright: {COPYRIGHT}
                     License: {LICENSE}
        '''))
        sys.exit()

    if data is None:
        print_error('jello:  missing piped JSON or JSON Lines data\n')

    # only process if there is data
    if data and not data.isspace():

        # load the JSON or JSON Lines
        try:
            list_dict_data = load_json(data)
        except Exception as e:
            # can't parse the data. Throw an error and quit
            msg = f'''JSON Load Exception: {e}
        Cannot parse the data (Not valid JSON or JSON Lines)
        '''
            print_error(f'''jello:  {msg}''')

        # run the query and check for various errors
        try:
            response = pyquery(list_dict_data, query)

        except KeyError as e:
            msg = f'Key does not exist: {e}'
            print_error(textwrap.dedent(f'''\
                jello:  {msg}
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
            msg = f'TypeError: {e}'
            print_error(textwrap.dedent(f'''\
                jello:  {msg}
            '''))

        except AttributeError as e:
            msg = f'AttributeError: {e}'
            print_error(textwrap.dedent(f'''\
                jello:  {msg}
            '''))

        except NameError as e:
            msg = f'NameError: {e}'
            print_error(textwrap.dedent(f'''\
                jello:  {msg}
            '''))

        except Exception as e:
            if len(str(list_dict_data)) > 70:
                err_data = str(list_dict_data)[0:35] + ' ... ' + str(list_dict_data)[-35:-1]

            if len(str(query)) > 70:
                query = str(query)[0:35] + ' ... ' + str(query)[-35:-1]

            if len(str(response)) > 70:
                response = str(response)[0:35] + ' ... ' + str(response)[-35:-1]

            msg = textwrap.dedent(f'''Query Exception: {e}
                                      query: {query}
                                      data: {err_data}
                                      output: {response}''')
            print_error(textwrap.dedent(f'''\
                jello:  {msg}
            '''))

        # if DotMap returns a bound function then we know it was a reserved attribute name
        if hasattr(response, '__self__'):
            print_error(textwrap.dedent(f'''\
                jello:  A reserved key name with dotted notation was used in the query.
                        Please use python bracket dict notation to access this key.

                        query: {query}
            '''))

        set_env_colors()

        # create JelloStyle class with user values from set_env_colors() or default values
        # need to do this here (not at global level), otherwise default values will not be updated
        class JelloStyle(Style):
            styles = {
                Name.Tag: f'bold {JelloTheme.colors["key_name"][0]}',   # key names
                Keyword: f'{JelloTheme.colors["keyword"][0]}',          # true, false, null
                Number: f'{JelloTheme.colors["number"][0]}',            # int, float
                String: f'{JelloTheme.colors["string"][0]}'             # string
            }

        # output as a schema if the user desires, otherwise generate JSON or Lines
        try:
            if opts.schema:
                if not sys.stdout.isatty():
                    opts.mono = True
                create_schema(response)
                print('\n'.join(schema_list))
                sys.exit()
            else:
                output = create_json(response)
        except Exception as e:
            if len(str(list_dict_data)) > 70:
                list_dict_data = str(list_dict_data)[0:35] + ' ... ' + str(list_dict_data)[-35:-1]

            if len(str(response)) > 70:
                response = str(response)[0:35] + ' ... ' + str(response)[-35:-1]

            if len(str(query)) > 70:
                query = str(query)[0:35] + ' ... ' + str(query)[-35:-1]
            print_error(textwrap.dedent(f'''\
                jello:  Formatting Exception:  {e}
                        query: {query}
                        data: {list_dict_data}
                        response: {response}
            '''))

        # Print colorized or mono JSON to STDOUT
        try:
            if not opts.mono and not opts.lines and sys.stdout.isatty():
                lexer = JsonLexer()
                formatter = Terminal256Formatter(style=JelloStyle)
                highlighted_json = highlight(output, lexer, formatter)
                print(highlighted_json[0:-1])
            else:
                print(output)

        except Exception as e:
            if len(str(list_dict_data)) > 70:
                list_dict_data = str(list_dict_data)[0:35] + ' ... ' + str(list_dict_data)[-35:-1]

            if len(str(response)) > 70:
                response = str(response)[0:35] + ' ... ' + str(response)[-35:-1]

            if len(str(output)) > 70:
                output = str(output)[0:35] + ' ... ' + str(output)[-35:-1]

            if len(str(query)) > 70:
                query = str(query)[0:35] + ' ... ' + str(query)[-35:-1]

            print_error(textwrap.dedent(f'''\
                jello:  Output Exception:  {e}
                        query: {query}
                        data: {list_dict_data}
                        response: {response}
                        output: {output}
            '''))


if __name__ == '__main__':
    main()
