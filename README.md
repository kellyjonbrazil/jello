# jwlk
Filter JSON data with Python syntax

## Examples:
```
$ cat farenheit
{"t1":-30, "t2":-20, "t3":-10, "t4":0}
cat far.json | ./cli.py 'keys = _.keys(); vals = _.values(); cel = list(map(lambda x: (float(5)/9)*(x-32), vals)); dict(zip(keys, cel))'
{
  "t1": -34.44444444444444,
  "t2": -28.88888888888889,
  "t3": -23.333333333333336,
  "t4": -17.77777777777778
}
```