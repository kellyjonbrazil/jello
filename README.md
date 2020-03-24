# jello
Filter JSON data with Python syntax

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
jc -a | jello '\
r = []
for entry in _["parsers"]:
  if "darwin" in entry["compatible"]:
    r.append(entry["name"])
r = "\n".join(r)'

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
$ jc -a | jello 'r = "\n".join([entry["name"] for entry in _["parsers"] if "darwin" in entry["compatible"]])'

airport
airport_s
arp
crontab
crontab_u
...
```
```
$ jc -a | jello 'r = len([entry for entry in _["parsers"] if "darwin" in entry["compatible"]])'

32
```
### Environment Variables
```
$ echo '{"login_name": "kbrazil"}' | jello '\
r = True if os.getenv("LOGNAME") == _["login_name"] else False'

True
```