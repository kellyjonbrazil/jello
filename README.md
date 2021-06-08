![Tests](https://github.com/kellyjonbrazil/jello/workflows/Tests/badge.svg?branch=master)
![Pypi](https://img.shields.io/pypi/v/jello.svg)

> Try the new `jello` [web demo](https://jello-web-demo.herokuapp.com/)!

> `jello` now supports dot notation!

# jello
Filter JSON and JSON Lines data with Python syntax

`jello` is similar to `jq` in that it processes JSON and JSON Lines data except `jello` uses standard python dict and list syntax.

JSON or JSON Lines can be piped into `jello` (JSON Lines are automatically slurped into a list of dictionaries) and are available as the variable `_`. Processed data can be output as JSON, JSON Lines, bash array lines, or a grep-able schema.

For more information on the motivations for this project, see my [blog post](https://blog.kellybrazil.com/2020/03/25/jello-the-jq-alternative-for-pythonistas/).

## Install
You can install `jello` via `pip`, via OS Package Repository, or by downloading the correct binary for your architecture and running it anywhere on your filesystem.

### Pip (macOS, linux, unix, Windows)
For the most up-to-date version and the most cross-platform option, use `pip` or `pip3` to download and install `jello` directly from [PyPi](https://pypi.org/project/jello/):

![Pypi](https://img.shields.io/pypi/v/jello.svg)


```bash
pip3 install jello
```

### OS Packages

[![Packaging status](https://repology.org/badge/vertical-allrepos/jello.svg)](https://repology.org/project/jello/versions)

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
cat data.json | jello [OPTIONS] [QUERY]
``` 
`QUERY` is optional and can be most any valid python code. `_` is the sanitized JSON from STDIN presented as a python dict or list of dicts. If `QUERY` is omitted then the original JSON input will simply be pretty printed. You can use dot notation or traditional python bracket notation to access key names.

> Note: Reserved key names that cannot be accessed using dot notation can be accessed via standard python dictionary notation. (e.g. _.foo["get"] instead of _.foo.get)


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
- `-i` initialize environment with a custom config file
- `-l` lines output (suitable for bash array assignment)
- `-m` monochrome output
- `-n` print selected `null` values
- `-r` raw output of selected strings (no quotes)
- `-s` print the JSON schema in grep-able format
- `-h` help
- `-v` version info

#### Simple Examples
`jello` simply pretty prints the JSON if there are no options passed:
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

Create [JSON Lines](https://jsonlines.org/) by combining the `-c` and `-l` options:
```bash
echo '[{"foo":"bar","baz":[1,2,3]},{"foo":"bar","baz":[1,2,3]}]' | jello -cl
{"foo":"bar","baz":[1,2,3]}
{"foo":"bar","baz":[1,2,3]}
```

You can also print a grep-able schema by using the `-s` option:
```bash
echo '{"foo":"bar","baz":[1,2,3]}' | jello -s
.foo = "bar";
.baz[0] = 1;
.baz[1] = 2;
.baz[2] = 3;
```

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

Here is more [advanced usage](https://github.com/kellyjonbrazil/jc/blob/master/ADVANCED_USAGE.md) information.

## Examples:
### Printing the Grep-able Schema
```bash
jc -a | jello -s
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

### Environment Variables
```bash
echo '{"login_name": "joeuser"}' | jello '\
    True if os.getenv("LOGNAME") == _.login_name else False'
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