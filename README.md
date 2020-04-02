![Test code](https://github.com/kellyjonbrazil/jello/workflows/Test%20code/badge.svg?branch=master)

# jello
Filter JSON and JSON Lines data with Python syntax

`jello` is similar to `jq` in that it processes JSON and JSON Lines data except `jello` uses standard python dict and list syntax.

JSON or JSON Lines can be piped into `jello` (JSON Lines are automatically slurped into a list of dictionaries) and are available as the variable `_`. Processed data can be output as JSON, JSON Lines, or bash array lines.

For more information on the motivations for this project, see my [blog post](https://blog.kellybrazil.com/2020/03/25/jello-the-jq-alternative-for-pythonistas/).

## Install
```
pip3 install --upgrade jello
```

### Usage
```
<JSON Data> | jello [OPTIONS] query
``` 
`query` can be most any valid python code. `_` is the sanitized JSON from STDIN presented as a python dict or list of dicts. For example:
```
$ cat data.json | jello '_["key"]'
```

**Options**
- `-c` compact print JSON output instead of pretty printing
- `-i` initialize environment with a custom config file
- `-l` lines output (suitable for bash array assignment)
- `-m` monochrome output
- `-n` print selected `null` values
- `-r` raw output of selected keys (no quotes)
- `-h` help
- `-v` version info

**Assigning Results to a Bash Array**

Use the `-l` option to print JSON array output in a manner suitable to be assigned to a bash array. The `-r` option can be used to remove quotation marks around strings. If you want `null` values to be printed as `null`, use the `-n` option, otherwise they are skipped.
```
variable=($(cat data.json | jello -rl '_["foo"]'))
```
> Note: The `lines()` convenience function has been deprecated and will be removed in a future version. Use the `-l` option instead to generate output suitable for assignment to a bash variable or array. Use of the `lines()` function will generate a warning message to `STDERR`.

**Custom Configuration File**

You can use the `-i` option to initialize the `jello` environment with your own configuration file. The configuration file accepts valid python code and can be as simple as adding `import` statements for your favorite libraries.

The filename must be `.jelloconf.py` and must be located in the proper directory based on the OS platform:
- Linux: `~/`
- Windows: `%appdata%/`

To simply import a module (e.g. `glom`) your `.jelloconf.py` file would look like this:
```
from glom import *
```
Then you could use `glom` in your `jello` filters:
```
$ jc -a | jello -i 'glom(_, "parsers.25.name")'

"lsblk"
```

Alternatively, if you wanted to initialize your `jello` environment to add `glom` syntax, your `.jelloconf.py` file could look like this:
```
def g(q, data=_):
    import glom
    return glom.glom(data, q)
```
Then you could use the following syntax to filter the JSON data:
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

## Examples:
### lambda functions and math
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
### for loops
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
### Using 3rd Party Libraries
You can import and use your favorite libraries to manipulate the data.  For example, using `glom`:
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
### Complex JSON Manipulation
The data from this example comes from https://programminghistorian.org/assets/jq_twitter.json

Under **Grouping and Counting**, Matthew describes an advanced `jq` filter against a sample Twitter dataset that includes JSON Lines data. There he describes the following query:

“We can now create a table of users. Let’s create a table with columns for the user id, user name, followers count, and a column of their tweet ids separated by a semicolon.”

https://programminghistorian.org/en/lessons/json-and-jq

Here is a simple solution using `jello`:
```
$ cat jq_twitter.json | jello -l '\
user_ids = set()
result = []
for tweet in _:
    user_ids.add(tweet["user"]["id"])
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