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


__version__ = '1.2.4'

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


class JelloTheme:
    """this class will contain the colors dictionary generated from set_env_colors()"""
    pass


def set_env_colors(keyname_color, keyword_color, number_color, string_color,
                   arrayid_color, arraybracket_color):
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
        print('jello:   Warning: could not parse JELLO_COLORS environment variable\n', file=sys.stderr)
        input_error = True

    if env_colors:
        for color in color_list:
            if color not in ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'gray', 'brightblack', 'brightred',
                             'brightgreen', 'brightyellow', 'brightblue', 'brightmagenta', 'brightcyan', 'white', 'default']:
                print('jello:   Warning: could not parse JELLO_COLORS environment variable\n', file=sys.stderr)
                input_error = True

    # if there is an issue with the env variable, just set all colors to default and move on
    if input_error:
        color_list = ['default', 'default', 'default', 'default', 'default', 'default']

    # Try the color set in the JELLO_COLORS env variable first. If it is set to default, then fall back to .jelloconf.py
    # configuration. If nothing is set in jelloconf.py, then use the default colors.
    JelloTheme.colors = {
        'key_name': color_map[color_list[0]] if not color_list[0] == 'default' else color_map[keyname_color] if keyname_color else color_map['blue'],
        'keyword': color_map[color_list[1]] if not color_list[1] == 'default' else color_map[keyword_color] if keyword_color else color_map['brightblack'],
        'number': color_map[color_list[2]] if not color_list[2] == 'default' else color_map[number_color] if number_color else color_map['magenta'],
        'string': color_map[color_list[3]] if not color_list[3] == 'default' else color_map[string_color] if string_color else color_map['green'],
        'array_id': color_map[color_list[4]] if not color_list[4] == 'default' else color_map[arrayid_color] if arrayid_color else color_map['red'],
        'array_bracket': color_map[color_list[5]] if not color_list[5] == 'default' else color_map[arraybracket_color] if arraybracket_color else color_map['magenta']
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
    if not mono:
        CEND = '\33[0m'
        CBOLD = '\33[1m'
        CKEYNAME = f'{JelloTheme.colors["key_name"][1]}'
        CKEYWORD = f'{JelloTheme.colors["keyword"][1]}'
        CNUMBER = f'{JelloTheme.colors["number"][1]}'
        CSTRING = f'{JelloTheme.colors["string"][1]}'
        CARRAYID = f'{JelloTheme.colors["array_id"][1]}'
        CARRAYBRACKET =  f'{JelloTheme.colors["array_bracket"][1]}'

    else:
        CEND = ''
        CBOLD = ''
        CKEYNAME = ''
        CKEYWORD = ''
        CNUMBER = ''
        CSTRING = ''
        CARRAYID = ''
        CARRAYBRACKET =  ''

    if isinstance(src, list) and path == '':
        for i, item in enumerate(src):
            print_schema(item, path=f'.{CARRAYBRACKET}[{CEND}{CARRAYID}{i}{CEND}{CARRAYBRACKET}]{CEND}', mono=mono)

    elif isinstance(src, list):
        for i, item in enumerate(src):
            print_schema(item, path=f'{path}.{CBOLD}{CKEYNAME}{src}{CEND}{CARRAYBRACKET}[{CEND}{CARRAYID}{i}{CEND}{CARRAYBRACKET}]{CEND}', mono=mono)

    elif isinstance(src, dict):
        for k, v in src.items():
            if isinstance(v, list):
                for i, item in enumerate(v):
                    print_schema(item, path=f'{path}.{CBOLD}{CKEYNAME}{k}{CEND}{CARRAYBRACKET}[{CEND}{CARRAYID}{i}{CEND}{CARRAYBRACKET}]{CEND}', mono=mono)

            elif isinstance(v, dict):
                if not mono:
                    k = f'{CBOLD}{CKEYNAME}{k}{CEND}'
                print_schema(v, path=f'{path}.{k}', mono=mono)

            else:
                k = f'{CBOLD}{CKEYNAME}{k}{CEND}'
                val = json.dumps(v)
                if val == 'true' or val == 'false' or val == 'null':
                    val = f'{CKEYWORD}{val}{CEND}'
                elif val.replace('.', '', 1).isdigit():
                    val = f'{CNUMBER}{val}{CEND}'
                else:
                    val = f'{CSTRING}{val}{CEND}'

                print(f'{path}.{k} = {val};')

    else:
        val = json.dumps(src)
        if val == 'true' or val == 'false' or val == 'null':
            val = f'{CKEYWORD}{val}{CEND}'
        elif val.replace('.', '', 1).isdigit():
            val = f'{CNUMBER}{val}{CEND}'
        else:
            val = f'{CSTRING}{val}{CEND}'

        print(f'{path} = {val};')


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


def pyquery(data, query, initialize=None, compact=None, nulls=None, raw=None, lines=None, mono=None, schema=None,
            keyname_color=None, keyword_color=None, number_color=None, string_color=None, arrayid_color=None,
            arraybracket_color=None):
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
        # extract jello options from .jelloconf.py (compact, raw, lines, nulls, mono, and custom colors)
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
                if expr.targets[0].id == 'keyname_color':
                    keyname_color = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
                if expr.targets[0].id == 'keyword_color':
                    keyword_color = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
                if expr.targets[0].id == 'number_color':
                    number_color = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
                if expr.targets[0].id == 'string_color':
                    string_color = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
                if expr.targets[0].id == 'arrayid_color':
                    arrayid_color = eval(compile(ast.Expression(expr.value), '<string>', "eval"))
                if expr.targets[0].id == 'arraybracket_color':
                    arraybracket_color = eval(compile(ast.Expression(expr.value), '<string>', "eval"))

                # validate the data in the initialization file
                warn_options = False
                warn_colors = False

                for option in [compact, raw, lines, nulls, mono, schema]:
                    if not isinstance(option, bool):
                        compact = raw = lines = nulls = mono = schema = None
                        warn_options = True

                for color_config in [keyname_color, keyword_color, number_color, string_color, arrayid_color, arraybracket_color]:
                    valid_colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'gray', 'brightblack', 'brightred',
                                    'brightgreen', 'brightyellow', 'brightblue', 'brightmagenta', 'brightcyan', 'white']
                    if color_config not in valid_colors and color_config is not None:
                        keyname_color = keyword_color = number_color = string_color = arrayid_color = arraybracket_color = None
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

        # need to return compact, nulls, raw, lines, mono, schema, keyname_color, number_color, sring_color,
        # arrayid_color, arraybracket_color in case they were changed in .jelloconf.py
        return (output, compact, nulls, raw, lines, mono, schema, keyname_color, keyword_color, number_color, string_color,
                arrayid_color, arraybracket_color)

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

    # break on pipe error. need try/except for windows compatibility
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except AttributeError:
        pass

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

    keyname_color = keyword_color = number_color = string_color = arrayid_color = arraybracket_color = None

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
    (response, compact, nulls, raw, lines, mono, schema, 
     keyname_color, keyword_color, number_color, string_color,
     arrayid_color, arraybracket_color) = pyquery(list_dict_data, query, initialize=initialize,
                                                  compact=compact, nulls=nulls, raw=raw, lines=lines,
                                                  mono=mono, schema=schema, keyname_color=keyname_color,
                                                  keyword_color=keyword_color, number_color=number_color,
                                                  string_color=string_color, arrayid_color=arrayid_color,
                                                  arraybracket_color=arraybracket_color)

    set_env_colors(keyname_color, keyword_color, number_color,
                   string_color, arrayid_color, arraybracket_color)

    # create JelloStyle class with user values from set_env_colors() or default values
    # need to do this here (not at global level), otherwise default values will not be updated
    class JelloStyle(Style):
        styles = {
            Name.Tag: f'bold {JelloTheme.colors["key_name"][0]}',   # key names
            Keyword: f'{JelloTheme.colors["keyword"][0]}',          # true, false, null
            Number: f'{JelloTheme.colors["number"][0]}',            # int, float
            String: f'{JelloTheme.colors["string"][0]}'             # string
        }
 

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
                lexer = JsonLexer()
                formatter = Terminal256Formatter(style=JelloStyle)
                highlighted_json = highlight(output, lexer, formatter)
                print(highlighted_json[0:-1])
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
