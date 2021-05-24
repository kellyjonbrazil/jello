![Tests](https://github.com/kellyjonbrazil/jello/workflows/Tests/badge.svg?branch=master)
![Pypi](https://img.shields.io/pypi/v/jello.svg)

> Try the new `jello` [web demo](https://jello-web-demo.herokuapp.com/)!

# jello
Filter JSON and JSON Lines data with Python syntax

`jello` is similar to `jq` in that it processes JSON and JSON Lines data except `jello` uses standard python dict and list syntax.

JSON or JSON Lines can be piped into `jello` (JSON Lines are automatically slurped into a list of dictionaries) and are available as the variable `_`. Processed data can be output as JSON, JSON Lines, bash array lines, or a grep-able schema.

For more information on the motivations for this project, see my [blog post](https://blog.kellybrazil.com/2020/03/25/jello-the-jq-alternative-for-pythonistas/).

## Install
You can install `jello` via `pip`, via OS Package Repository, MSI installer for Windows, or by downloading the correct binary for your architecture and running it anywhere on your filesystem.

### Pip (macOS, linux, unix, Windows)
For the most up-to-date version and the most cross-platform option, use `pip` or `pip3` to download and install `jello` directly from [PyPi](https://pypi.org/project/jello/):

![Pypi](https://img.shields.io/pypi/v/jello.svg)

```bash
pip3 install jello
```

### OS Packages

[![Packaging status](https://repology.org/badge/vertical-allrepos/jello.svg)](https://repology.org/project/jello/versions)

### MSI Installer (Windows 2016+)
The MSI Installer packages for Windows are built from PyPi and can be installed on modern versions of Windows. These installers may not always be on the very latest `jello` version, but are regularly updated.

| Version   | File                                                                                    | SHA256 Hash                                                       |
|-----------|-----------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| 1.2.11    | [jello-1.2.11.msi](https://jello-packages.s3-us-west-1.amazonaws.com/jello-1.2.11.msi)  | 08da1c91e5d1930542529473350dc10ffc3d4adf5c06cc365c333663ac82a8fc  |

### Binaries (x86_64)
Linux and macOS x86_64 binaries are built from PyPi and can be copied to any location in your path and run. These binaries may not always be on the very latest `jello` version, but are regularly updated.

#### Linux (Fedora, RHEL, CentOS, Debian, Ubuntu)

| Version   | File                                                                                                        | SHA256 Hash (binary file)                                         |
|-----------|-------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| 1.2.9     | [jello-1.2.9-linux.tar.gz](https://jello-packages.s3-us-west-1.amazonaws.com/bin/jello-1.2.9-linux.tar.gz)  | ffe8dfe2cc1dc446aeade32078db654de604176976be5dee89f83f0049551c45  |


#### macOS (Mojave and higher)

| Version   | File                                                                                                          | SHA256 Hash (binary file)                                         |
|-----------|---------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------|
| 1.2.9     | [jello-1.2.9-darwin.tar.gz](https://jello-packages.s3-us-west-1.amazonaws.com/bin/jello-1.2.9-darwin.tar.gz)  | 9355bf19212cce60f5f592a1a778fdf26984f4b86968ceca2a3e99792c258037  |

### Usage
```
<JSON Data> | jello [OPTIONS] [QUERY]
``` 
`QUERY` is optional and can be most any valid python code. `_` is the sanitized JSON from STDIN presented as a python dict or list of dicts. If `QUERY` is omitted then the original JSON input will simply be pretty printed.

A simple query:
```
$ cat data.json | jello '_["foo"]'
```

#### Options
- `-c` compact print JSON output instead of pretty printing
- `-i` initialize environment with a custom config file
- `-l` lines output (suitable for bash array assignment)
- `-m` monochrome output
- `-n` print selected `null` values
- `-r` raw output of selected strings (no quotes)
- `-s` print the JSON schema in grep-able format
- `-h` help
- `-v` version info

#### Assigning Results to a Bash Array

Use the `-l` option to print JSON array output in a manner suitable to be assigned to a bash array. The `-r` option can be used to remove quotation marks around strings. If you want `null` values to be printed as `null`, use the `-n` option, otherwise they are skipped.

Bash variable:
```
variable=($(cat data.json | jello -rl '_["foo"]'))
```

Bash array variable:
```
variable=()
while read -r value; do
    variable+=("$value")
done < <(cat data.json | jello -rl '_["foo"]')
```

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
```
$ jc -a | jello -i 'glom(_, "parsers.25.name")'

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
```
$ jc -a | jello -i 'g("parsers.6.compatible")'

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

## Examples:
### Printing the Grep-able Schema
```
$ jc -a | jello -s

.name = "jc";
.version = "1.10.2";
.description = "jc cli output JSON conversion tool";
.author = "Kelly Brazil";
.author_email = "kellyjonbrazil@gmail.com";
.parser_count = 50;
.parsers[0].name = "airport";
.parsers[0].argument = "--airport";
.parsers[0].version = "1.0";
.parsers[0].description = "airport -I command parser";
.parsers[0].author = "Kelly Brazil";
.parsers[0].author_email = "kellyjonbrazil@gmail.com";
.parsers[0].compatible[0] = "darwin";
.parsers[0].magic_commands[0] = "airport -I";
.parsers[1].name = "airport_s";
.parsers[1].argument = "--airport-s";
.parsers[1].version = "1.0";
...
```
### Lambda Functions and Math
```
$ echo '{"t1":-30, "t2":-20, "t3":-10, "t4":0}' | jello '\
keys = _.keys()
vals = _.values()
cel = list(map(lambda x: (float(5)/9)*(x-32), vals))
dict(zip(keys, cel))'

{
  "t1": -34.44444444444444,
  "t2": -28.88888888888889,
  "t3": -23.333333333333336,
  "t4": -17.77777777777778
}

```
```
$ jc -a | jello 'len([entry for entry in _["parsers"] if "darwin" in entry["compatible"]])'

32
```
### For Loops
Output as JSON array
```
$ jc -a | jello '\
result = []
for entry in _["parsers"]:
  if "darwin" in entry["compatible"]:
    result.append(entry["name"])
result'

[
  "airport",
  "airport_s",
  "arp",
  "crontab",
  "crontab_u",
  ...
]
```
Output as bash array
```
$ jc -a | jello -rl '\
result = []
for entry in _["parsers"]:
  if "darwin" in entry["compatible"]:
    result.append(entry["name"])
result'

airport
airport_s
arp
crontab
crontab_u
...
```
### List and Dictionary Comprehension
Output as JSON array
```
$ jc -a | jello '[entry["name"] for entry in _["parsers"] if "darwin" in entry["compatible"]]'

[
  "airport",
  "airport_s",
  "arp",
  "crontab",
  "crontab_u",
  ...
]
```
Output as bash array
```
$ jc -a | jello -rl '[entry["name"] for entry in _["parsers"] if "darwin" in entry["compatible"]]'

airport
airport_s
arp
crontab
crontab_u
...
```
### Environment Variables
```
$ echo '{"login_name": "joeuser"}' | jello '\
True if os.getenv("LOGNAME") == _["login_name"] else False'

true
```
### Using 3rd Party Modules
You can import and use your favorite modules to manipulate the data.  For example, using `glom`:
```
$ jc -a | jello '\
from glom import *
glom(_, ("parsers", ["name"]))'

[
  "airport",
  "airport_s",
  "arp",
  "blkid",
  "crontab",
  "crontab_u",
  "csv",
  ...
]
```
### Advanced JSON Manipulation
The data from this example comes from https://programminghistorian.org/assets/jq_twitter.json

Under **Grouping and Counting**, Matthew describes an advanced `jq` filter against a sample Twitter dataset that includes JSON Lines data. There he describes the following query:

> "We can now create a table of users. Let’s create a table with columns for the user id, user name, followers count, and a column of their tweet ids separated by a semicolon."

https://programminghistorian.org/en/lessons/json-and-jq

Here is a simple solution using `jello`:
```
$ cat jq_twitter.json | jello -l '\
user_ids = set()
for tweet in _:
    user_ids.add(tweet["user"]["id"])
result = []
for user in user_ids:
    user_profile = {}
    tweet_ids = []
    for tweet in _:
        if tweet["user"]["id"] == user:
            user_profile.update({
                "user_id": user,
                "user_name": tweet["user"]["screen_name"],
                "user_followers": tweet["user"]["followers_count"]})
            tweet_ids.append(str(tweet["id"]))
    user_profile["tweet_ids"] = ";".join(tweet_ids)
    result.append(user_profile)
result'

...
{"user_id": 2696111005, "user_name": "EGEVER142", "user_followers": 1433, "tweet_ids": "619172303654518784"}
{"user_id": 42226593, "user_name": "shirleycolleen", "user_followers": 2114, "tweet_ids": "619172281294655488;619172179960328192"}
{"user_id": 106948003, "user_name": "MrKneeGrow", "user_followers": 172, "tweet_ids": "501064228627705857"}
{"user_id": 18270633, "user_name": "ahhthatswhy", "user_followers": 559, "tweet_ids": "501064204661850113"}
{"user_id": 14331818, "user_name": "edsu", "user_followers": 4220, "tweet_ids": "615973042443956225;618602288781860864"}
{"user_id": 2569107372, "user_name": "SlavinOleg", "user_followers": 35, "tweet_ids": "501064198973960192;501064202794971136;501064214467731457;501064215759568897;501064220121632768"}
{"user_id": 22668719, "user_name": "nodehyena", "user_followers": 294, "tweet_ids": "501064222772445187"}
...
```