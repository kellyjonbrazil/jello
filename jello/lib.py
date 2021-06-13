"""jello - query JSON at the command line with python syntax"""

import os
import sys
import ast
import json
from jello.dotmap import DotMap


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


class JelloTheme:
    def __init__(self):
        # default colors
        self.colors = {
            'key_name': ('ansiblue', '\33[34m'),
            'keyword': ('ansibrightblack', '\33[90m'),
            'number': ('ansimagenta', '\33[35m'),
            'string': ('ansigreen', '\33[32m'),
            'array_id': ('ansired', '\33[31m'),
            'array_bracket': ('ansimagenta', '\33[35m')
        }

        self.color_map = {
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

    def set_colors(self):
        """
        Updates the JelloTheme.colors dictionary used by the JelloStyle class.

        Grab custom colors from JELLO_COLORS environment variable and opts class set by .jelloconf.py file.
        Individual colors from JELLO_COLORS take precedence over .jelloconf.py. Individual colors from
        JELLO_COLORS will fall back to .jelloconf.py or default if the env variable color is set to 'default'

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

        if env_colors and len(color_list) != 6:
            input_error = True

        if env_colors:
            for color in color_list:
                if color not in ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'gray', 'brightblack', 'brightred',
                                 'brightgreen', 'brightyellow', 'brightblue', 'brightmagenta', 'brightcyan', 'white', 'default']:
                    input_error = True
        else:
            color_list = ['default', 'default', 'default', 'default', 'default', 'default']

        # if there is an issue with the env variable, just set all colors to default and move on
        if input_error:
            print('jello:   Warning: could not parse JELLO_COLORS environment variable\n', file=sys.stderr)
            color_list = ['default', 'default', 'default', 'default', 'default', 'default']

        # first set colors from opts class or fallback to defaults
        self.colors = {
            'key_name': self.color_map[opts.keyname_color] if opts.keyname_color else self.colors['key_name'],
            'keyword': self.color_map[opts.keyword_color] if opts.keyword_color else self.colors['keyword'],
            'number': self.color_map[opts.number_color] if opts.number_color else self.colors['number'],
            'string': self.color_map[opts.string_color] if opts.string_color else self.colors['string'],
            'array_id': self.color_map[opts.arrayid_color] if opts.arrayid_color else self.colors['array_id'],
            'array_bracket': self.color_map[opts.arraybracket_color] if opts.arraybracket_color else self.colors['array_bracket']
        }

        # then set colors from JELLO_COLORS env variable or fallback to existing colors
        self.colors = {
            'key_name': self.color_map[color_list[0]] if not color_list[0] == 'default' else self.colors['key_name'],
            'keyword': self.color_map[color_list[1]] if not color_list[1] == 'default' else self.colors['keyword'],
            'number': self.color_map[color_list[2]] if not color_list[2] == 'default' else self.colors['number'],
            'string': self.color_map[color_list[3]] if not color_list[3] == 'default' else self.colors['string'],
            'array_id': self.color_map[color_list[4]] if not color_list[4] == 'default' else self.colors['array_id'],
            'array_bracket': self.color_map[color_list[5]] if not color_list[5] == 'default' else self.colors['array_bracket']
        }


class Schema:
    def __init__(self):
        self.schema_list = []

        self.colors = {
            'key_name': ('ansiblue', '\33[34m'),
            'keyword': ('ansibrightblack', '\33[90m'),
            'number': ('ansimagenta', '\33[35m'),
            'string': ('ansigreen', '\33[32m'),
            'array_id': ('ansired', '\33[31m'),
            'array_bracket': ('ansimagenta', '\33[35m')
        }

    def create_schema(self, src, path=''):
        """
        Creates a grep-able schema representation of the JSON.

        This function is recursive, so output is stored within the schema_list list. Make sure to
        initialize schema_list to a blank list and set colors by calling set_env_colors() before
        calling this function.
        """
        if not opts.mono:
            CEND = '\33[0m'
            CBOLD = '\33[1m'
            CKEYNAME = f'{self.colors["key_name"][1]}'
            CKEYWORD = f'{self.colors["keyword"][1]}'
            CNUMBER = f'{self.colors["number"][1]}'
            CSTRING = f'{self.colors["string"][1]}'
            CARRAYID = f'{self.colors["array_id"][1]}'
            CARRAYBRACKET = f'{self.colors["array_bracket"][1]}'

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
                self.create_schema(item, path=f'.{CARRAYBRACKET}[{CEND}{CARRAYID}{i}{CEND}{CARRAYBRACKET}]{CEND}')

        elif isinstance(src, list):
            for i, item in enumerate(src):
                self.create_schema(item, path=f'{path}.{CBOLD}{CKEYNAME}{src}{CEND}{CARRAYBRACKET}[{CEND}{CARRAYID}{i}{CEND}{CARRAYBRACKET}]{CEND}')

        elif isinstance(src, dict):
            for k, v in src.items():
                if isinstance(v, list):
                    for i, item in enumerate(v):
                        self.create_schema(item, path=f'{path}.{CBOLD}{CKEYNAME}{k}{CEND}{CARRAYBRACKET}[{CEND}{CARRAYID}{i}{CEND}{CARRAYBRACKET}]{CEND}')

                elif isinstance(v, dict):
                    if not opts.mono:
                        k = f'{CBOLD}{CKEYNAME}{k}{CEND}'
                    self.create_schema(v, path=f'{path}.{k}')

                else:
                    k = f'{CBOLD}{CKEYNAME}{k}{CEND}'
                    val = json.dumps(v, ensure_ascii=False)
                    if val == 'true' or val == 'false' or val == 'null':
                        val = f'{CKEYWORD}{val}{CEND}'
                    elif val.replace('.', '', 1).isdigit():
                        val = f'{CNUMBER}{val}{CEND}'
                    else:
                        val = f'{CSTRING}{val}{CEND}'

                    self.schema_list.append(f'{path}.{k} = {val};')

        else:
            val = json.dumps(src, ensure_ascii=False)
            if val == 'true' or val == 'false' or val == 'null':
                val = f'{CKEYWORD}{val}{CEND}'
            elif val.replace('.', '', 1).isdigit():
                val = f'{CNUMBER}{val}{CEND}'
            else:
                val = f'{CSTRING}{val}{CEND}'

            path = path or '.'

            self.schema_list.append(f'{path} = {val};')


def pyquery(data, query):
    '''Sets options and runs the user's query'''
    output = None

    # read data into '_' variable
    # if data is a list of dictionaries, then need to iterate through and convert all dictionaries to DotMap
    if isinstance(data, list):
        _ = [DotMap(i, _dynamic=False, _prevent_method_masking=True) if isinstance(i, dict)
             else i for i in data]

    elif isinstance(data, dict):
        _ = DotMap(data, _dynamic=False, _prevent_method_masking=True)

    else:
        _ = data

    # read initialization file to set colors, options, and user-defined functions
    jelloconf = ''
    conf_file = ''

    if opts.initialize:
        if sys.platform.startswith('win32'):
            conf_file = os.path.join(os.environ['APPDATA'], '.jelloconf.py')
        else:
            conf_file = os.path.join(os.environ["HOME"], '.jelloconf.py')

        try:
            with open(conf_file, 'r') as f:
                jelloconf = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f'-i used and initialization file not found: {conf_file}')

    warn_options = False
    warn_colors = False

    i_block = ast.parse(jelloconf, mode='exec')
    exec(compile(i_block, '<string>', mode='exec'))

    for option in [opts.compact, opts.raw, opts.lines, opts.nulls, opts.mono, opts.schema]:
        if not isinstance(option, bool) and option is not None:
            opts.compact = opts.raw = opts.lines = opts.nulls = opts.mono = opts.schema = False
            warn_options = True

    for color_config in [opts.keyname_color, opts.keyword_color, opts.number_color,
                         opts.string_color, opts.arrayid_color, opts.arraybracket_color]:
        valid_colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'gray', 'brightblack', 'brightred',
                        'brightgreen', 'brightyellow', 'brightblue', 'brightmagenta', 'brightcyan', 'white']

        if color_config not in valid_colors and color_config is not None:
            opts.keyname_color = opts.keyword_color = opts.number_color = opts.string_color = opts.arrayid_color = opts.arraybracket_color = None
            warn_colors = True

    if warn_options:
        print(f'Jello:   Warning: Options must be set to True or False in {conf_file}\n         Unsetting all options.\n', file=sys.stderr)

    if warn_colors:
        valid_colors_string = ', '.join(valid_colors)
        print(f'Jello:   Warning: Colors must be set to one of: {valid_colors_string} in {conf_file}\n         Unsetting all colors.\n', file=sys.stderr)

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

    # if DotMap returns a bound function then we know it was a reserved attribute name
    if hasattr(output, '__self__'):
        raise ValueError('Reserved key name. Use bracket notation to access this key.')

    return output


def load_json(data):
    try:
        json_dict = json.loads(data)
    except Exception:
        # if json.loads fails, assume the data is json lines and parse
        json_dict = [json.loads(i) for i in data.splitlines()]

    return json_dict


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
            raise ValueError('Cannot print list of lists as lines. Try normal JSON output.')

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

    # only non-serializable types are left. Force an exception from json.dumps()
    else:
        json.dumps(data)
        # this code should not run, but just in case something slips by above
        raise TypeError(f'Object is not JSON serializable')
