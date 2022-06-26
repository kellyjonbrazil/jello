"""jello - query JSON at the command line with python syntax"""

import os
import sys
import ast
import json
import shutil
from textwrap import TextWrapper
from jello.dotmap import DotMap

# make pygments import optional
try:
    from pygments import highlight
    from pygments.style import Style
    from pygments.token import (Name, Number, String, Keyword)
    from pygments.lexers import JsonLexer
    from pygments.lexers.javascript import JavascriptLexer
    from pygments.formatters import Terminal256Formatter
    from pygments.formatters import HtmlFormatter
    PYGMENTS_INSTALLED = True
except Exception:
    PYGMENTS_INSTALLED = False


class opts:
    initialize = None
    version_info = None
    helpme = None
    compact = None
    nulls = None
    raw = None
    lines = None
    force_color = None
    mono = None
    schema = None
    types = None
    keyname_color = None
    keyword_color = None
    number_color = None
    string_color = None


class JelloTheme:
    if PYGMENTS_INSTALLED:
        theme = {
            Name: 'bold ansiblue',
            Keyword: 'ansibrightblack',
            Number: 'ansimagenta',
            String: 'ansigreen'
        }

    def set_colors(self):
        """
        Updates the JelloTheme.theme dictionary used by the JelloStyle class.

        Grab custom colors from JELLO_COLORS environment variable and opts class set by .jelloconf.py file.
        Individual colors from JELLO_COLORS take precedence over .jelloconf.py. Individual colors from
        JELLO_COLORS will fall back to .jelloconf.py or default if the env variable color is set to 'default'

        JELLO_COLORS env variable takes 4 comma separated string values and should be in the format of:

        JELLO_COLORS=<keyname_color>,<keyword_color>,<number_color>,<string_color>

        Where colors are: black, red, green, yellow, blue, magenta, cyan, gray, brightblack, brightred,
                          brightgreen, brightyellow, brightblue, brightmagenta, brightcyan, white, default

        Default colors:
            JELLO_COLORS=blue,brightblack,magenta,green
            or
            JELLO_COLORS=default,default,default,default
        """
        env_colors = os.getenv('JELLO_COLORS')
        input_error = False

        if env_colors:
            color_list = env_colors.split(',')

        if env_colors and len(color_list) != 4:
            input_error = True

        if env_colors:
            for color in color_list:
                if color not in ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'gray', 'brightblack', 'brightred',
                                 'brightgreen', 'brightyellow', 'brightblue', 'brightmagenta', 'brightcyan', 'white', 'default']:
                    input_error = True
        else:
            color_list = ['default', 'default', 'default', 'default']

        # if there is an issue with the env variable, just set all colors to default and move on
        if input_error:
            warning_message(['could not parse JELLO_COLORS environment variable'])
            color_list = ['default', 'default', 'default', 'default']

        if PYGMENTS_INSTALLED:
            # first set theme from opts class or fallback to defaults
            self.theme = {
                Name: f'bold ansi{opts.keyname_color}' if opts.keyname_color else self.theme[Name],
                Keyword: f'ansi{opts.keyword_color}' if opts.keyword_color else self.theme[Keyword],
                Number: f'ansi{opts.number_color}' if opts.number_color else self.theme[Number],
                String: f'ansi{opts.string_color}' if opts.string_color else self.theme[String]
            }

            # then set theme from JELLO_COLORS env variable or fallback to existing colors
            self.theme = {
                Name: f'bold ansi{color_list[0]}' if not color_list[0] == 'default' else self.theme[Name],
                Keyword: f'ansi{color_list[1]}' if not color_list[1] == 'default' else self.theme[Keyword],
                Number: f'ansi{color_list[2]}' if not color_list[2] == 'default' else self.theme[Number],
                String: f'ansi{color_list[3]}' if not color_list[3] == 'default' else self.theme[String]
            }


class Schema(JelloTheme):
    """Inherits theme and set_colors() from JelloTheme"""

    def __init__(self):
        self._schema_list = []

    def color_output(self, data):
        if not opts.mono and PYGMENTS_INSTALLED:
            class JelloStyle(Style):
                styles = self.theme

            lexer = JavascriptLexer()
            formatter = Terminal256Formatter(style=JelloStyle)
            return highlight(data, lexer, formatter)[0:-1]

        else:
            return data

    def html_output(self, data):
        class JelloStyle(Style):
            styles = self.theme

        lexer = JavascriptLexer()
        formatter = HtmlFormatter(style=JelloStyle, noclasses=True)
        return highlight(data, lexer, formatter)

    def create_schema(self, data):
        self._schema_gen(data)
        myschema = '\n'.join(self._schema_list)
        # unsure if this is helpful, but trying to reduce memory footprint by clearing the list
        self._schema_list *= 0
        return myschema

    def _schema_gen(self, src, path='_'):
        """
        Creates a grep-able schema representation of the JSON.
        This method is recursive, and output is stored within self._schema_list (list).
        """
        if isinstance(src, list):
            # print empty brackets as first list definition
            val = '[]'
            val_type = ''
            padding = ''
            if opts.types:
                val_type = '//   (array)'
                padding = '  '
                if len(path) + len(val) + len(val_type) < 76:
                    padding = ' ' * (76 - (len(path) + len(val) + len(val_type)))

            self._schema_list.append(f'{path} = {val};{padding}{val_type}')

            for i, item in enumerate(src):
                self._schema_gen(item, path=f'{path}[{i}]')

        elif isinstance(src, dict):
            # print empty curly brackets as first object definition
            val = '{}'
            val_type = ''
            padding = ''
            if opts.types:
                val_type = '//  (object)'
                padding = '  '
                if len(path) + len(val) + len(val_type) < 76:
                    padding = ' ' * (76 - (len(path) + len(val) + len(val_type)))

            self._schema_list.append(f'{path} = {val};{padding}{val_type}')

            for k, v in src.items():
                # encapsulate key in brackets if it includes spaces
                if ' ' in k:
                    k = f'["{k}"]'
                else:
                    k = f'.{k}'

                if isinstance(v, list):
                    # print empty brackets as first list definition
                    val = '[]'
                    val_type = ''
                    padding = ''
                    if opts.types:
                        val_type = '//   (array)'
                        padding = '  '
                        if len(path) + len(val) + len(val_type) < 76:
                            padding = ' ' * (76 - (len(f'{path}{k}') + len(val) + len(val_type)))

                    self._schema_list.append(f'{path}{k} = {val};{padding}{val_type}')

                    for i, item in enumerate(v):
                        self._schema_gen(item, path=f'{path}{k}[{i}]')

                elif isinstance(v, dict):
                    self._schema_gen(v, path=f'{path}{k}')

                else:
                    val = json.dumps(v, ensure_ascii=False)
                    val_type = ''
                    padding = ''
                    if opts.types:
                        if val == 'true' or val == 'false':
                            val_type = '// (boolean)'
                        elif val == 'null':
                            val_type = '//    (null)'
                        elif val.replace('.', '', 1).isdigit():
                            val_type = '//  (number)'
                        else:
                            val_type = '//  (string)'

                        padding = '  '
                        if len(path) + len(k) + len(val) + len(val_type) < 76:
                            padding = ' ' * (76 - (len(path) + len(k) + len(val) + len(val_type)))

                    self._schema_list.append(f'{path}{k} = {val};{padding}{val_type}')

        else:
            val = json.dumps(src, ensure_ascii=False)
            val_type = ''
            padding = ''
            if opts.types:
                if val == 'true' or val == 'false':
                    val_type = '// (boolean)'
                elif val == 'null':
                    val_type = '//    (null)'
                elif val.replace('.', '', 1).isdigit():
                    val_type = '//  (number)'
                else:
                    val_type = '//  (string)'

                padding = '  '
                if len(path) + len(val) + len(val_type) < 76:
                    padding = ' ' * (76 - (len(path) + len(val) + len(val_type)))

            self._schema_list.append(f'{path} = {val};{padding}{val_type}')


class Json(JelloTheme):
    """Inherits theme and set_colors() from JelloTheme"""

    def color_output(self, data):
        if not opts.mono and PYGMENTS_INSTALLED:
            class JelloStyle(Style):
                styles = self.theme

            lexer = JsonLexer()
            formatter = Terminal256Formatter(style=JelloStyle)
            return highlight(data, lexer, formatter)[0:-1]

        else:
            return data

    def html_output(self, data):
        class JelloStyle(Style):
            styles = self.theme

        lexer = JsonLexer()
        formatter = HtmlFormatter(style=JelloStyle, noclasses=True)
        return highlight(data, lexer, formatter)

    def create_json(self, data):
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

            # print lines
            else:
                flat_list = ''
                for entry in data:
                    if entry is None:
                        if opts.nulls:
                            flat_list += 'null\n'
                        else:
                            flat_list += '\n'

                    elif isinstance(entry, (dict, list, bool, int, float)):
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


def load_json(data):
    try:
        json_dict = json.loads(data)
    except Exception as e:
        try:
            # if json.loads fails, try loading as json lines
            json_dict = [json.loads(i) for i in data.splitlines()]
        except Exception:
            # raise original JSON exception instead of JSON Lines exception
            raise e

    return json_dict


def warning_message(message_lines):
    """
    Prints warning message for non-fatal issues. The first line is prepended with
    'jello:  Warning - ' and subsequent lines are indented. Wraps text as needed
    based on the terminal width.

    Parameters:

        message:   (list) list of string lines

    Returns:

        None - just prints output to STDERR
    """
    columns = shutil.get_terminal_size().columns

    first_wrapper = TextWrapper(width=columns, subsequent_indent=' ' * 12)
    next_wrapper = TextWrapper(width=columns, initial_indent=' ' * 8,
                               subsequent_indent=' ' * 12)

    first_line = message_lines.pop(0)
    first_str = f'jello:  Warning - {first_line}'
    first_str = first_wrapper.fill(first_str)
    print(first_str, file=sys.stderr)

    for line in message_lines:
        if line == '':
            continue
        message = next_wrapper.fill(line)
        print(message, file=sys.stderr)


def pyquery(data, query):
    """Sets options and runs the user's query."""
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

    for option in [opts.compact, opts.raw, opts.lines, opts.nulls, opts.force_color, opts.mono, opts.schema, opts.types]:
        if not isinstance(option, bool) and option is not None:
            opts.compact = opts.raw = opts.lines = opts.nulls = opts.force_color = opts.mono = opts.schema = opts.types = False
            warn_options = True

    for color_config in [opts.keyname_color, opts.keyword_color, opts.number_color, opts.string_color]:
        valid_colors = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'gray', 'brightblack',
                        'brightred', 'brightgreen', 'brightyellow', 'brightblue', 'brightmagenta', 'brightcyan',
                        'white']

        if color_config not in valid_colors and color_config is not None:
            opts.keyname_color = opts.keyword_color = opts.number_color = opts.string_color = None
            warn_colors = True

    if warn_options:
        warning_message([
            f'Options must be set to True or False in {conf_file}',
            'Unsetting all options.'
        ])

    if warn_colors:
        valid_colors_string = ', '.join(valid_colors)
        warning_message([
            f'Colors must be set to one of: {valid_colors_string} in {conf_file}',
            'Unsetting all colors.'
        ])

    # run the query
    block = ast.parse(query, mode='exec')
    last = ast.Expression(block.body.pop().value)    # assumes last node is an expression
    scope = {'_': _, 'os': os}
    exec(compile(block, '<string>', mode='exec'), scope)
    output = eval(compile(last, '<string>', mode='eval'), scope)

    # convert output back to normal dict
    if isinstance(output, list):
        output = [i.toDict() if isinstance(i, DotMap) else i for i in output]

    elif isinstance(output, DotMap):
        output = output.toDict()

    # if DotMap returns a bound function then we know it was a reserved attribute name
    if hasattr(output, '__self__'):
        raise ValueError('Reserved key name. Use bracket notation to access this key.')

    return output


if __name__ == '__main__':
    pass
