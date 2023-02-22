[![Tests](https://github.com/kellyjonbrazil/jello/workflows/Tests/badge.svg?branch=master)](https://github.com/kellyjonbrazil/jello/actions)
[![Pypi](https://img.shields.io/pypi/v/jello.svg)](https://pypi.org/project/jello/)

>Built on `jello`:
>- [Jello Explorer](https://github.com/kellyjonbrazil/jellex) (aka `jellex`) interactive TUI
>- `jello` [web demo](https://jello-web.onrender.com)

# jello
Filter JSON and JSON Lines data with Python syntax

`jello` is similar to `jq` in that it processes JSON and JSON Lines data except `jello` uses standard python dict and list syntax.

JSON or JSON Lines can be piped into `jello` (JSON Lines are automatically slurped into a list of dictionaries) and are available as the variable `_`. Processed data can be output as JSON, JSON Lines, bash array lines, or a grep-able schema.

For more information on the motivations for this project, see my [blog post](https://blog.kellybrazil.com/2020/03/25/jello-the-jq-alternative-for-pythonistas/).

## Install
You can install `jello` via `pip`, via OS Package Repository, MSI installer for Windows, or by downloading the correct binary for your architecture and running it anywhere on your filesystem.

### Pip (macOS, linux, unix, Windows)
For the most up-to-date version and the most cross-platform option, use `pip` or `pip3` to download and install `jello` directly from [PyPi](https://pypi.org/project/jello/):

[![Pypi](https://img.shields.io/pypi/v/jello.svg)](https://pypi.org/project/jello/)

```bash
pip3 install jello
```

### Packages and Binaries

| OS                    | Command                  |
|-----------------------|--------------------------|
| Debian/Ubuntu linux   | `apt-get install jello`  |
| Fedora linux          | `dnf install jello`      |
| Arch linux            | `pacman -S jello`        |
| macOS                 | `brew install jello`     |

> For more OS packages, see https://repology.org/project/jello/versions.

See [Releases](https://github.com/kellyjonbrazil/jello/releases) on Github for MSI packages and binaries.

### Usage
```
cat data.json | jello [OPTIONS] [QUERY]
```
`QUERY` is optional and can be most any valid python code. `_` is the sanitized JSON from STDIN presented as a python dict or list of dicts. If `QUERY` is omitted then the original JSON input will simply be pretty printed. You can use dot notation or traditional python bracket notation to access key names.

> Note: Reserved key names that cannot be accessed using dot notation can be accessed via standard python dictionary notation. (e.g. `_.foo["get"]` instead of `_.foo.get`)

A simple query:
```bash
cat data.json | jello _.foo
```
or
```bash
cat data.json | jello '_["foo"]'
```

#### Options
- `-c` compact print JSON output instead of pretty printing
- `-C` force color output even when using pipes (overrides `-m` and the `NO_COLOR` env variable)
- `-i` initialize environment with a custom config file
- `-l` lines output (suitable for bash array assignment)
- `-m` monochrome output
- `-n` print selected `null` values
- `-r` raw output of selected strings (no quotes)
- `-s` print the JSON schema in grep-able format
- `-t` print type annotations in schema view
- `-h` help
- `-v` version info

#### Simple Examples
`jello` simply pretty prints the JSON if there are no options  or query passed:
```bash
echo '{"foo":"bar","baz":[1,2,3]}' | jello

{
  "foo": "bar",
  "baz": [
    1,
    2,
    3
  ]
}
```

If you prefer compact output, use the `-c` option:
```bash
echo '{"foo":"bar","baz":[1,2,3]}' | jello -c

{"foo":"bar","baz":[1,2,3]}
```

Use the `-l` option to convert lists/arrays into lines:
```bash
echo '{"foo":"bar","baz":[1,2,3]}' | jello -l _.baz

1
2
3
```

The `-l` option also allows you to create [JSON Lines](https://jsonlines.org/):
```bash
echo '[{"foo":"bar","baz":[1,2,3]},{"fiz":"boo","buz":[4,5,6]}]' | jello -l

{"foo":"bar","baz":[1,2,3]}
{"fiz":"boo","buz":[4,5,6]}
```

You can print a grep-able schema by using the `-s` option:
```bash
echo '{"foo":"bar","baz":[1,2,3]}' | jello -s

_ = {};
_.foo = "bar";
_.baz = [];
_.baz[0] = 1;
_.baz[1] = 2;
_.baz[2] = 3;
```

#### Assigning Results to a Bash Array

Use the `-l` option to print JSON array output in a manner suitable to be assigned to a bash array. The `-r` option can be used to remove quotation marks around strings. If you want `null` values to be printed as `null`, use the `-n` option, otherwise they are printed as blank lines.

Bash variable:
```
variable=($(cat data.json | jello -rl _.foo))
```

Bash array variable (Bash 4+):
```
mapfile -t variable < <(cat data.json | jello -rl _.foo)
```

Bash array variable (older versions of Bash):
```
variable=()
while read -r value; do
    variable+=("$value")
done < <(cat data.json | jello -rl _.foo)
```

### Setting Custom Colors via Environment Variable
Custom colors can be set via the `JELLO_COLORS` environment variable. Any colors set in the environment variable will take precedence over any colors set in the initialization file. (see [Advanced Usage](https://github.com/kellyjonbrazil/jello/blob/master/ADVANCED_USAGE.md))

The `JELLO_COLORS` environment variable takes four comma separated string values in the following format:
```
JELLO_COLORS=<keyname_color>,<keyword_color>,<number_color>,<string_color>
```
Where colors are: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `gray`, `brightblack`, `brightred`, `brightgreen`, `brightyellow`, `brightblue`, `brightmagenta`, `brightcyan`, `white`, or  `default`

For example, to set to the default colors:
```
JELLO_COLORS=blue,brightblack,magenta,green
```
or
```
JELLO_COLORS=default,default,default,default
```

### Disable Colors via Environment Variable
You can set the [`NO_COLOR`](http://no-color.org/) environment variable to any value to disable color output in `jello`. Note that using the `-C` option to force color output will override both the `NO_COLOR` environment variable and the `-m` option.

### Advanced Usage
Here is more [Advanced Usage](https://github.com/kellyjonbrazil/jello/blob/master/ADVANCED_USAGE.md) information.

> To accelerate filter development and testing, try [`jellex`](https://github.com/kellyjonbrazil/jellex). `jellex` is an interactive front-end TUI built on `jello` that allows you to see your filter results in real-time along with any errors.

## Examples:
### Printing the Grep-able Schema
```bash
$ jc -a | jello -s

_ = {};
_.name = "jc";
_.version = "1.17.2";
_.description = "JSON CLI output utility";
_.author = "Kelly Brazil";
_.author_email = "kellyjonbrazil@gmail.com";
_.website = "https://github.com/kellyjonbrazil/jc";
_.copyright = "© 2019-2021 Kelly Brazil";
_.license = "MIT License";
_.parser_count = 80;
_.parsers = [];
_.parsers[0] = {};
_.parsers[0].name = "acpi";
_.parsers[0].argument = "--acpi";
_.parsers[0].version = "1.2";
_.parsers[0].description = "`acpi` command parser";
_.parsers[0].author = "Kelly Brazil";
_.parsers[0].author_email = "kellyjonbrazil@gmail.com";
_.parsers[0].compatible = [];
_.parsers[0].compatible[0] = "linux";
_.parsers[0].magic_commands = [];
_.parsers[0].magic_commands[0] = "acpi";
_.parsers[1] = {};
_.parsers[1].name = "airport";
_.parsers[1].argument = "--airport";
_.parsers[1].version = "1.3";
...
```
### Printing the Grep-able Schema with type annotations (useful for grepping types)
```bash
jc dig example.com | jello -st

_ = [];                                                             //   (array)
_[0] = {};                                                          //  (object)
_[0].id = 23819;                                                    //  (number)
_[0].opcode = "QUERY";                                              //  (string)
_[0].status = "NOERROR";                                            //  (string)
_[0].flags = [];                                                    //   (array)
_[0].flags[0] = "qr";                                               //  (string)
_[0].flags[1] = "rd";                                               //  (string)
_[0].flags[2] = "ra";                                               //  (string)
_[0].query_num = 1;                                                 //  (number)
_[0].answer_num = 1;                                                //  (number)
_[0].authority_num = 0;                                             //  (number)
_[0].additional_num = 1;                                            //  (number)
_[0].opt_pseudosection = {};                                        //  (object)
_[0].opt_pseudosection.edns = {};                                   //  (object)
_[0].opt_pseudosection.edns.version = 0;                            //  (number)
_[0].opt_pseudosection.edns.flags = [];                             //   (array)
_[0].opt_pseudosection.edns.udp = 4096;                             //  (number)
_[0].question = {};                                                 //  (object)
_[0].question.name = "example.com.";                                //  (string)
_[0].question.class = "IN";                                         //  (string)
_[0].question.type = "A";                                           //  (string)
_[0].answer = [];                                                   //   (array)
_[0].answer[0] = {};                                                //  (object)
_[0].answer[0].name = "example.com.";                               //  (string)
_[0].answer[0].class = "IN";                                        //  (string)
_[0].answer[0].type = "A";                                          //  (string)
_[0].answer[0].ttl = 48358;                                         //  (number)
_[0].answer[0].data = "93.184.216.34";                              //  (string)
_[0].query_time = 46;                                               //  (number)
_[0].server = "2600:1700:bab0:d40::1#53(2600:1700:bab0:d40::1)";    //  (string)
_[0].when = "Mon Nov 29 09:41:11 PST 2021";                         //  (string)
_[0].rcvd = 56;                                                     //  (number)
_[0].when_epoch = 1638207671;                                       //  (number)
_[0].when_epoch_utc = null;                                         //    (null)
```
### Printing the Structure of the JSON
```bash
jc dig example.com | jello -st | grep '(object)\|(array)'

_ = [];                                                             //   (array)
_[0] = {};                                                          //  (object)
_[0].flags = [];                                                    //   (array)
_[0].opt_pseudosection = {};                                        //  (object)
_[0].opt_pseudosection.edns = {};                                   //  (object)
_[0].opt_pseudosection.edns.flags = [];                             //   (array)
_[0].question = {};                                                 //  (object)
_[0].answer = [];                                                   //   (array)
_[0].answer[0] = {};                                                //  (object)
```
### Lambda Functions and Math
```bash
echo '{"t1":-30, "t2":-20, "t3":-10, "t4":0}' | jello '\
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

```bash
jc -a | jello 'len([entry for entry in _.parsers if "darwin" in entry.compatible])'

45
```

### For Loops
Output as JSON array
```bash
jc -a | jello '\
result = []
for entry in _.parsers:
  if "darwin" in entry.compatible:
    result.append(entry.name)
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
```bash
jc -a | jello -rl '\
result = []
for entry in _.parsers:
  if "darwin" in entry.compatible:
    result.append(entry.name)
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
```bash
jc -a | jello '[entry.name for entry in _.parsers if "darwin" in entry.compatible]'

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
```bash
jc -a | jello -rl '[entry.name for entry in _.parsers if "darwin" in entry.compatible]'

airport
airport_s
arp
crontab
crontab_u
...
```

### Expressions and Environment Variables
```bash
echo '{"login_name": "joeuser"}' | jello 'os.getenv("LOGNAME") == _.login_name'

true
```

### Using 3rd Party Modules
You can import and use your favorite modules to manipulate the data.  For example, using `glom`:
```bash
jc -a | jello '\
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
```bash
cat jq_twitter.json | jello -l '\
user_ids = set()
for tweet in _:
    user_ids.add(tweet.user.id)
result = []
for user in user_ids:
    user_profile = {}
    tweet_ids = []
    for tweet in _:
        if tweet.user.id == user:
            user_profile.update({
                "user_id": user,
                "user_name": tweet.user.screen_name,
                "user_followers": tweet.user.followers_count})
            tweet_ids.append(str(tweet.id))
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