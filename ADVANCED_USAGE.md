# Jello Advanced Usage

#### Custom Configuration File

You can use the `-i` option to initialize the `jello` environment with your own configuration file. The configuration file accepts valid python code where you can enable/disable `jello` options, customize your colors, add `import` statements for your favorite modules, and define your own functions.

The file must be named `.jelloconf.py` and must be located in the proper directory based on the OS platform:
- Linux, unix, macOS: `~/`
- Windows: `%appdata%/`

##### Setting Options
To set `jello` options in the `.jelloconf.py` file, import the `jello.lib.opts` class, add any of the following and set to `True` or `False`:
```python
from jello.lib import opts
opts.mono = True            # -m option
opts.compact = True         # -c option
opts.empty = True           # -e option
opts.lines = True           # -l option
opts.raw = True             # -r option
opts.raw_input = True       # -R option
opts.force_color = True     # -C option
opts.nulls = True           # -n option
opts.schema = True          # -s option
opts.types = True           # -t option
```
##### Setting Colors
You can customize the colors by importing the `jello.lib.opts` class and setting the following variables to one of the following string values: `'black'`, `'red'`, `'green'`, `'yellow'`, `'blue'`, `'magenta'`, `'cyan'`, `'gray'`, `'brightblack'`, `'brightred'`, `'brightgreen'`, `'brightyellow'`, `'brightblue'`, `'brightmagenta'`, `'brightcyan'`, or `'white'`.
```python
from jello.lib import opts
opts.keyname_color = 'blue'            # Key names
opts.keyword_color = 'brightblack'     # true, false, null
opts.number_color = 'magenta'          # integers, floats
opts.string_color = 'green'            # strings
```
> Note: Any colors set via the `JELLO_COLORS` environment variable will take precedence over any color values set in the `.jelloconf.py` configuration file

##### Importing Modules
To import a module (e.g. `glom`) during initialization, just add the `import` statement to your `.jelloconf.py` file:
```python
from glom import *
```
Then you can use `glom` in your `jello` filters without importing:
```bash
jc -a | jello -i 'glom(_, "parsers.25.name")'
"lsblk"
```

##### Adding Functions
You can also add functions to your initialization file.  For example, you could simplify `glom` use by adding the following function to `.jelloconf.py`:
```python
def g(query):
    import glom
    return glom.glom(_, query)
```

Then you can use the following syntax to filter the JSON data:
```bash
jc -a | jello -i 'g("parsers.6.compatible")'
[
  "linux",
  "darwin",
  "cygwin",
  "win32",
  "aix",
  "freebsd"
]
```

Or you can predefine often-used queries by defining them as functions in `.jelloconf.py`:
```python
def darwin_compatible():
    result = []
    for entry in _.parsers:
      if "darwin" in entry.compatible:
        result.append(entry.name)
    return result
```

Then you can use the predefined query like so:
```bash
jc -a | jello -i 'darwin_compatible()'
[
  "airport",
  "airport_s",
  "arp",
  "asciitable",
  ...
]
```

Tip: Add a the following to print a message to STDERR in your `.jelloconf.py` file to show when the initialization file is being used:
```python
import sys
print('Running initialization file', file=sys.stderr)
```
