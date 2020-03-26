# jello
Filter JSON and JSON Lines data with Python syntax

`jello` is similar to `jq` in that it processes JSON and JSON Lines data except `jello` uses standard python dict and list syntax.

JSON or JSON Lines can be piped into `jello` (JSON Lines are automatically slurped into a list of dictionaries) and are available as the variable `_`. Assign the output the the variable `r` to print as JSON or simple lines.

## Install
```
pip3 install --upgrade jello
```

### Usage
```
<JSON Data> | jello [OPTIONS] query
``` 
`query` can be most any valid python code as long as the result is assigned to `r`. `_` is the sanitized JSON from STDIN presented as a python dict or list of dicts. For example:
```
$ cat data.json | jello 'r = _["key"]'
```
**Options**
- `-c` compact print JSON output instead of pretty printing
- `-r` raw output of selected keys (no quotes)
- `-n` print null values

## Examples:
### lambda functions and math
```
$ echo '{"t1":-30, "t2":-20, "t3":-10, "t4":0}' | jello '\
keys = _.keys()
vals = _.values()
cel = list(map(lambda x: (float(5)/9)*(x-32), vals))
r = dict(zip(keys, cel))'

{
  "t1": -34.44444444444444,
  "t2": -28.88888888888889,
  "t3": -23.333333333333336,
  "t4": -17.77777777777778
}

```
```
$ jc -a | jello 'r = len([entry for entry in _["parsers"] if "darwin" in entry["compatible"]])'

32
```
### for loops
Output as JSON array
```
jc -a | jello '\
r = []
for entry in _["parsers"]:
  if "darwin" in entry["compatible"]:
    r.append(entry["name"])'

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
jc -a | jello -r '\
r = []
for entry in _["parsers"]:
  if "darwin" in entry["compatible"]:
    r.append(entry["name"])
r = bash(r)'

airport
airport_s
arp
crontab
crontab_u
...
```
### List and Dictionary Comprehension
Output as JSON arrauy
```
$ jc -a | jello 'r = [entry["name"] for entry in _["parsers"] if "darwin" in entry["compatible"]]'

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
$ jc -a | jello -r 'r = bash([entry["name"] for entry in _["parsers"] if "darwin" in entry["compatible"]])'

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
r = True if os.getenv("LOGNAME") == _["login_name"] else False'

true
```