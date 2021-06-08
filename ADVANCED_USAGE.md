# Jello Advanced Usage

#### Custom Configuration File

You can use the `-i` option to initialize the `jello` environment with your own configuration file. The configuration file accepts valid python code where you can set the `jello` options you would like enabled or disabled, customize your colors, add `import` statements for your favorite modules, and define your own functions.

The file must be named `.jelloconf.py` and must be located in the proper directory based on the OS platform:
- Linux, unix, macOS: `~/`
- Windows: `%appdata%/`

##### Setting Options
To set `jello` options in the `.jelloconf.py` file, add any of the following and set to `True` or `False`:
```
mono = True            # -m option
compact = True         # -c option
lines = True           # -l option
raw = True             # -r option
nulls = True           # -n option
schema = True          # -s option
```
##### Setting Colors
You can customize the colors by setting the following variables to one of the following string values: `'black'`, `'red'`, `'green'`, `'yellow'`, `'blue'`, `'magenta'`, `'cyan'`, `'gray'`, `'brightblack'`, `'brightred'`, `'brightgreen'`, `'brightyellow'`, `'brightblue'`, `'brightmagenta'`, `'brightcyan'`, or `'white'`.
```
keyname_color = 'blue'            # Key names
keyword_color = 'brightblack'     # true, false, null
number_color = 'magenta'          # integers, floats
string_color = 'green'            # strings
arrayid_color = 'red'             # array IDs in Schema view
arraybracket_color = 'magenta'    # array brackets in Schema view
```
> Note: Any colors set via the `JELLO_COLORS` environment variable will take precedence over any color values set in the `.jelloconf.py` configuration file

##### Importing Modules
To import a module (e.g. `glom`) during initialization, just add the `import` statement to your `.jelloconf.py` file:
```
from glom import *
```
Then you can use `glom` in your `jello` filters without importing:
```bash
jc -a | jello -i 'glom(_, "parsers.25.name")'
"lsblk"
```

##### Adding Functions
You can also add functions to your initialization file.  For example, you could simplify `glom` use by adding the following function to `.jelloconf.py`:
```
def g(q, data=_):
    import glom
    return glom.glom(data, q)
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
## Setting Custom Colors via Environment Variable
In addition to setting custom colors in the `.jelloconf.py` intialization file, you can also set them via the `JELLO_COLORS` environment variable. Any colors set in the environment variable will take precedence over any colors set in the initialization file.

The `JELLO_COLORS` environment variable takes six comma separated string values in the following format:
```
JELLO_COLORS=<keyname_color>,<keyword_color>,<number_color>,<string_color>,<arrayid_color>,<arraybracket_color>
```
Where colors are: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `gray`, `brightblack`, `brightred`, `brightgreen`, `brightyellow`, `brightblue`, `brightmagenta`, `brightcyan`, `white`, or  `default`

For example, to set to the default colors:
```
JELLO_COLORS=blue,brightblack,magenta,green,red,magenta
```
or
```
JELLO_COLORS=default,default,default,default,default,default
```
