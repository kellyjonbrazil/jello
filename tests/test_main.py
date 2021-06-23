#!/usr/bin/env python3

import os
import sys
import io
import contextlib
import unittest
from unittest.mock import patch
import jello.cli
from jello.lib import opts


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class MyTests(unittest.TestCase):

    def setUp(self):
        # initialize options
        opts.initialize = None
        opts.version_info = None
        opts.helpme = None
        opts.compact = None
        opts.nulls = None
        opts.raw = None
        opts.lines = None
        opts.mono = None
        opts.schema = None
        opts.types = None
        opts.keyname_color = None
        opts.keyword_color = None
        opts.number_color = None
        opts.string_color = None

        self.jc_a_output = '''{"name": "jc", "version": "1.9.3", "description": "jc cli output JSON conversion tool", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "parser_count": 50, "parsers": [{"name": "airport", "argument": "--airport", "version": "1.0", "description": "airport -I command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["darwin"], "magic_commands": ["airport -I"]}, {"name": "airport_s", "argument": "--airport-s", "version": "1.0", "description": "airport -s command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["darwin"], "magic_commands": ["airport -s"]}, {"name": "arp", "argument": "--arp", "version": "1.2", "description": "arp command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "aix", "freebsd", "darwin"], "magic_commands": ["arp"]}, {"name": "blkid", "argument": "--blkid", "version": "1.0", "description": "blkid command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["blkid"]}, {"name": "crontab", "argument": "--crontab", "version": "1.1", "description": "crontab command and file parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "aix", "freebsd"], "magic_commands": ["crontab"]}, {"name": "crontab_u", "argument": "--crontab-u", "version": "1.0", "description": "crontab file parser with user support", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "aix", "freebsd"]}, {"name": "csv", "argument": "--csv", "version": "1.0", "description": "CSV file parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "details": "Using the python standard csv library", "compatible": ["linux", "darwin", "cygwin", "win32", "aix", "freebsd"]}, {"name": "df", "argument": "--df", "version": "1.1", "description": "df command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin"], "magic_commands": ["df"]}, {"name": "dig", "argument": "--dig", "version": "1.1", "description": "dig command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "aix", "freebsd", "darwin"], "magic_commands": ["dig"]}, {"name": "du", "argument": "--du", "version": "1.1", "description": "du command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "aix", "freebsd"], "magic_commands": ["du"]}, {"name": "env", "argument": "--env", "version": "1.1", "description": "env command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "cygwin", "win32", "aix", "freebsd"], "magic_commands": ["env"]}, {"name": "file", "argument": "--file", "version": "1.1", "description": "file command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "aix", "freebsd", "darwin"], "magic_commands": ["file"]}, {"name": "free", "argument": "--free", "version": "1.0", "description": "free command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["free"]}, {"name": "fstab", "argument": "--fstab", "version": "1.0", "description": "fstab file parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"]}, {"name": "group", "argument": "--group", "version": "1.0", "description": "/etc/group file parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "aix", "freebsd"]}, {"name": "gshadow", "argument": "--gshadow", "version": "1.0", "description": "/etc/gshadow file parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "aix", "freebsd"]}, {"name": "history", "argument": "--history", "version": "1.2", "description": "history command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "details": "Optimizations by https://github.com/philippeitis", "compatible": ["linux", "darwin", "cygwin", "aix", "freebsd"]}, {"name": "hosts", "argument": "--hosts", "version": "1.0", "description": "/etc/hosts file parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "cygwin", "win32", "aix", "freebsd"]}, {"name": "id", "argument": "--id", "version": "1.0", "description": "id command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "aix", "freebsd"], "magic_commands": ["id"]}, {"name": "ifconfig", "argument": "--ifconfig", "version": "1.5", "description": "ifconfig command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "details": "Using ifconfig-parser package from https://github.com/KnightWhoSayNi/ifconfig-parser", "compatible": ["linux", "aix", "freebsd", "darwin"], "magic_commands": ["ifconfig"]}, {"name": "ini", "argument": "--ini", "version": "1.0", "description": "INI file parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "details": "Using configparser from the standard library", "compatible": ["linux", "darwin", "cygwin", "win32", "aix", "freebsd"]}, {"name": "iptables", "argument": "--iptables", "version": "1.1", "description": "iptables command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["iptables"]}, {"name": "jobs", "argument": "--jobs", "version": "1.0", "description": "jobs command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "cygwin", "aix", "freebsd"], "magic_commands": ["jobs"]}, {"name": "last", "argument": "--last", "version": "1.0", "description": "last and lastb command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "aix", "freebsd"], "magic_commands": ["last", "lastb"]}, {"name": "ls", "argument": "--ls", "version": "1.3", "description": "ls command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "cygwin", "aix", "freebsd"], "magic_commands": ["ls"]}, {"name": "lsblk", "argument": "--lsblk", "version": "1.3", "description": "lsblk command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["lsblk"]}, {"name": "lsmod", "argument": "--lsmod", "version": "1.1", "description": "lsmod command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["lsmod"]}, {"name": "lsof", "argument": "--lsof", "version": "1.0", "description": "lsof command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["lsof"]}, {"name": "mount", "argument": "--mount", "version": "1.1", "description": "mount command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin"], "magic_commands": ["mount"]}, {"name": "netstat", "argument": "--netstat", "version": "1.2", "description": "netstat command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["netstat"]}, {"name": "ntpq", "argument": "--ntpq", "version": "1.0", "description": "ntpq -p command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["ntpq"]}, {"name": "passwd", "argument": "--passwd", "version": "1.0", "description": "/etc/passwd file parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "aix", "freebsd"]}, {"name": "pip_list", "argument": "--pip-list", "version": "1.0", "description": "pip list command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "cygwin", "win32", "aix", "freebsd"], "magic_commands": ["pip list", "pip3 list"]}, {"name": "pip_show", "argument": "--pip-show", "version": "1.0", "description": "pip show command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "cygwin", "win32", "aix", "freebsd"], "magic_commands": ["pip show", "pip3 show"]}, {"name": "ps", "argument": "--ps", "version": "1.1", "description": "ps command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "cygwin", "aix", "freebsd"], "magic_commands": ["ps"]}, {"name": "route", "argument": "--route", "version": "1.0", "description": "route command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["route"]}, {"name": "shadow", "argument": "--shadow", "version": "1.0", "description": "/etc/shadow file parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "aix", "freebsd"]}, {"name": "ss", "argument": "--ss", "version": "1.0", "description": "ss command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["ss"]}, {"name": "stat", "argument": "--stat", "version": "1.0", "description": "stat command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["stat"]}, {"name": "systemctl", "argument": "--systemctl", "version": "1.0", "description": "systemctl command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["systemctl"]}, {"name": "systemctl_lj", "argument": "--systemctl-lj", "version": "1.0", "description": "systemctl list-jobs command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["systemctl list-jobs"]}, {"name": "systemctl_ls", "argument": "--systemctl-ls", "version": "1.0", "description": "systemctl list-sockets command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["systemctl list-sockets"]}, {"name": "systemctl_luf", "argument": "--systemctl-luf", "version": "1.0", "description": "systemctl list-unit-files command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["systemctl list-unit-files"]}, {"name": "timedatectl", "argument": "--timedatectl", "version": "1.0", "description": "timedatectl status command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux"], "magic_commands": ["timedatectl", "timedatectl status"]}, {"name": "uname", "argument": "--uname", "version": "1.1", "description": "uname -a command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin"], "magic_commands": ["uname"]}, {"name": "uptime", "argument": "--uptime", "version": "1.0", "description": "uptime command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "cygwin", "aix", "freebsd"], "magic_commands": ["uptime"]}, {"name": "w", "argument": "--w", "version": "1.0", "description": "w command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "cygwin", "aix", "freebsd"], "magic_commands": ["w"]}, {"name": "who", "argument": "--who", "version": "1.0", "description": "who command parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "compatible": ["linux", "darwin", "cygwin", "aix", "freebsd"], "magic_commands": ["who"]}, {"name": "xml", "argument": "--xml", "version": "1.0", "description": "XML file parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "details": "Using the xmltodict library at https://github.com/martinblech/xmltodict", "compatible": ["linux", "darwin", "cygwin", "win32", "aix", "freebsd"]}, {"name": "yaml", "argument": "--yaml", "version": "1.0", "description": "YAML file parser", "author": "Kelly Brazil", "author_email": "kellyjonbrazil@gmail.com", "details": "Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml", "compatible": ["linux", "darwin", "cygwin", "win32", "aix", "freebsd"]}]}'''

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/twitterdata.jlines'), 'r', encoding='utf-8') as f:
            self.twitterdata = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/twitterdata.json'), 'r', encoding='utf-8') as f:
            self.twitterdata_output = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/twitter-table-output.jlines'), 'r', encoding='utf-8') as f:
            self.twitter_table_output = f.read()

        with open(os.path.join(THIS_DIR, os.pardir, 'tests/fixtures/twitter-table-output.schema'), 'r', encoding='utf-8') as f:
            self.twitter_table_output_schema = f.read()

    def test_jc_a(self):
        """
        Test jc -a | jello
        """
        self.expected = '''\
{
  "name": "jc",
  "version": "1.9.3",
  "description": "jc cli output JSON conversion tool",
  "author": "Kelly Brazil",
  "author_email": "kellyjonbrazil@gmail.com",
  "parser_count": 50,
  "parsers": [
    {
      "name": "airport",
      "argument": "--airport",
      "version": "1.0",
      "description": "airport -I command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "darwin"
      ],
      "magic_commands": [
        "airport -I"
      ]
    },
    {
      "name": "airport_s",
      "argument": "--airport-s",
      "version": "1.0",
      "description": "airport -s command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "darwin"
      ],
      "magic_commands": [
        "airport -s"
      ]
    },
    {
      "name": "arp",
      "argument": "--arp",
      "version": "1.2",
      "description": "arp command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "aix",
        "freebsd",
        "darwin"
      ],
      "magic_commands": [
        "arp"
      ]
    },
    {
      "name": "blkid",
      "argument": "--blkid",
      "version": "1.0",
      "description": "blkid command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "blkid"
      ]
    },
    {
      "name": "crontab",
      "argument": "--crontab",
      "version": "1.1",
      "description": "crontab command and file parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "crontab"
      ]
    },
    {
      "name": "crontab_u",
      "argument": "--crontab-u",
      "version": "1.0",
      "description": "crontab file parser with user support",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "aix",
        "freebsd"
      ]
    },
    {
      "name": "csv",
      "argument": "--csv",
      "version": "1.0",
      "description": "CSV file parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "details": "Using the python standard csv library",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "win32",
        "aix",
        "freebsd"
      ]
    },
    {
      "name": "df",
      "argument": "--df",
      "version": "1.1",
      "description": "df command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin"
      ],
      "magic_commands": [
        "df"
      ]
    },
    {
      "name": "dig",
      "argument": "--dig",
      "version": "1.1",
      "description": "dig command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "aix",
        "freebsd",
        "darwin"
      ],
      "magic_commands": [
        "dig"
      ]
    },
    {
      "name": "du",
      "argument": "--du",
      "version": "1.1",
      "description": "du command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "du"
      ]
    },
    {
      "name": "env",
      "argument": "--env",
      "version": "1.1",
      "description": "env command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "win32",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "env"
      ]
    },
    {
      "name": "file",
      "argument": "--file",
      "version": "1.1",
      "description": "file command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "aix",
        "freebsd",
        "darwin"
      ],
      "magic_commands": [
        "file"
      ]
    },
    {
      "name": "free",
      "argument": "--free",
      "version": "1.0",
      "description": "free command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "free"
      ]
    },
    {
      "name": "fstab",
      "argument": "--fstab",
      "version": "1.0",
      "description": "fstab file parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ]
    },
    {
      "name": "group",
      "argument": "--group",
      "version": "1.0",
      "description": "/etc/group file parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "aix",
        "freebsd"
      ]
    },
    {
      "name": "gshadow",
      "argument": "--gshadow",
      "version": "1.0",
      "description": "/etc/gshadow file parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "aix",
        "freebsd"
      ]
    },
    {
      "name": "history",
      "argument": "--history",
      "version": "1.2",
      "description": "history command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "details": "Optimizations by https://github.com/philippeitis",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "aix",
        "freebsd"
      ]
    },
    {
      "name": "hosts",
      "argument": "--hosts",
      "version": "1.0",
      "description": "/etc/hosts file parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "win32",
        "aix",
        "freebsd"
      ]
    },
    {
      "name": "id",
      "argument": "--id",
      "version": "1.0",
      "description": "id command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "id"
      ]
    },
    {
      "name": "ifconfig",
      "argument": "--ifconfig",
      "version": "1.5",
      "description": "ifconfig command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "details": "Using ifconfig-parser package from https://github.com/KnightWhoSayNi/ifconfig-parser",
      "compatible": [
        "linux",
        "aix",
        "freebsd",
        "darwin"
      ],
      "magic_commands": [
        "ifconfig"
      ]
    },
    {
      "name": "ini",
      "argument": "--ini",
      "version": "1.0",
      "description": "INI file parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "details": "Using configparser from the standard library",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "win32",
        "aix",
        "freebsd"
      ]
    },
    {
      "name": "iptables",
      "argument": "--iptables",
      "version": "1.1",
      "description": "iptables command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "iptables"
      ]
    },
    {
      "name": "jobs",
      "argument": "--jobs",
      "version": "1.0",
      "description": "jobs command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "jobs"
      ]
    },
    {
      "name": "last",
      "argument": "--last",
      "version": "1.0",
      "description": "last and lastb command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "last",
        "lastb"
      ]
    },
    {
      "name": "ls",
      "argument": "--ls",
      "version": "1.3",
      "description": "ls command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "ls"
      ]
    },
    {
      "name": "lsblk",
      "argument": "--lsblk",
      "version": "1.3",
      "description": "lsblk command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "lsblk"
      ]
    },
    {
      "name": "lsmod",
      "argument": "--lsmod",
      "version": "1.1",
      "description": "lsmod command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "lsmod"
      ]
    },
    {
      "name": "lsof",
      "argument": "--lsof",
      "version": "1.0",
      "description": "lsof command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "lsof"
      ]
    },
    {
      "name": "mount",
      "argument": "--mount",
      "version": "1.1",
      "description": "mount command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin"
      ],
      "magic_commands": [
        "mount"
      ]
    },
    {
      "name": "netstat",
      "argument": "--netstat",
      "version": "1.2",
      "description": "netstat command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "netstat"
      ]
    },
    {
      "name": "ntpq",
      "argument": "--ntpq",
      "version": "1.0",
      "description": "ntpq -p command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "ntpq"
      ]
    },
    {
      "name": "passwd",
      "argument": "--passwd",
      "version": "1.0",
      "description": "/etc/passwd file parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "aix",
        "freebsd"
      ]
    },
    {
      "name": "pip_list",
      "argument": "--pip-list",
      "version": "1.0",
      "description": "pip list command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "win32",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "pip list",
        "pip3 list"
      ]
    },
    {
      "name": "pip_show",
      "argument": "--pip-show",
      "version": "1.0",
      "description": "pip show command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "win32",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "pip show",
        "pip3 show"
      ]
    },
    {
      "name": "ps",
      "argument": "--ps",
      "version": "1.1",
      "description": "ps command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "ps"
      ]
    },
    {
      "name": "route",
      "argument": "--route",
      "version": "1.0",
      "description": "route command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "route"
      ]
    },
    {
      "name": "shadow",
      "argument": "--shadow",
      "version": "1.0",
      "description": "/etc/shadow file parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "aix",
        "freebsd"
      ]
    },
    {
      "name": "ss",
      "argument": "--ss",
      "version": "1.0",
      "description": "ss command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "ss"
      ]
    },
    {
      "name": "stat",
      "argument": "--stat",
      "version": "1.0",
      "description": "stat command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "stat"
      ]
    },
    {
      "name": "systemctl",
      "argument": "--systemctl",
      "version": "1.0",
      "description": "systemctl command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "systemctl"
      ]
    },
    {
      "name": "systemctl_lj",
      "argument": "--systemctl-lj",
      "version": "1.0",
      "description": "systemctl list-jobs command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "systemctl list-jobs"
      ]
    },
    {
      "name": "systemctl_ls",
      "argument": "--systemctl-ls",
      "version": "1.0",
      "description": "systemctl list-sockets command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "systemctl list-sockets"
      ]
    },
    {
      "name": "systemctl_luf",
      "argument": "--systemctl-luf",
      "version": "1.0",
      "description": "systemctl list-unit-files command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "systemctl list-unit-files"
      ]
    },
    {
      "name": "timedatectl",
      "argument": "--timedatectl",
      "version": "1.0",
      "description": "timedatectl status command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux"
      ],
      "magic_commands": [
        "timedatectl",
        "timedatectl status"
      ]
    },
    {
      "name": "uname",
      "argument": "--uname",
      "version": "1.1",
      "description": "uname -a command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin"
      ],
      "magic_commands": [
        "uname"
      ]
    },
    {
      "name": "uptime",
      "argument": "--uptime",
      "version": "1.0",
      "description": "uptime command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "uptime"
      ]
    },
    {
      "name": "w",
      "argument": "--w",
      "version": "1.0",
      "description": "w command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "w"
      ]
    },
    {
      "name": "who",
      "argument": "--who",
      "version": "1.0",
      "description": "who command parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "aix",
        "freebsd"
      ],
      "magic_commands": [
        "who"
      ]
    },
    {
      "name": "xml",
      "argument": "--xml",
      "version": "1.0",
      "description": "XML file parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "details": "Using the xmltodict library at https://github.com/martinblech/xmltodict",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "win32",
        "aix",
        "freebsd"
      ]
    },
    {
      "name": "yaml",
      "argument": "--yaml",
      "version": "1.0",
      "description": "YAML file parser",
      "author": "Kelly Brazil",
      "author_email": "kellyjonbrazil@gmail.com",
      "details": "Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml",
      "compatible": [
        "linux",
        "darwin",
        "cygwin",
        "win32",
        "aix",
        "freebsd"
      ]
    }
  ]
}
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_s(self):
        """
        Test jc -a | jello -s
        """
        self.expected = '''\
.name = "jc";
.version = "1.9.3";
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
.parsers[1].description = "airport -s command parser";
.parsers[1].author = "Kelly Brazil";
.parsers[1].author_email = "kellyjonbrazil@gmail.com";
.parsers[1].compatible[0] = "darwin";
.parsers[1].magic_commands[0] = "airport -s";
.parsers[2].name = "arp";
.parsers[2].argument = "--arp";
.parsers[2].version = "1.2";
.parsers[2].description = "arp command parser";
.parsers[2].author = "Kelly Brazil";
.parsers[2].author_email = "kellyjonbrazil@gmail.com";
.parsers[2].compatible[0] = "linux";
.parsers[2].compatible[1] = "aix";
.parsers[2].compatible[2] = "freebsd";
.parsers[2].compatible[3] = "darwin";
.parsers[2].magic_commands[0] = "arp";
.parsers[3].name = "blkid";
.parsers[3].argument = "--blkid";
.parsers[3].version = "1.0";
.parsers[3].description = "blkid command parser";
.parsers[3].author = "Kelly Brazil";
.parsers[3].author_email = "kellyjonbrazil@gmail.com";
.parsers[3].compatible[0] = "linux";
.parsers[3].magic_commands[0] = "blkid";
.parsers[4].name = "crontab";
.parsers[4].argument = "--crontab";
.parsers[4].version = "1.1";
.parsers[4].description = "crontab command and file parser";
.parsers[4].author = "Kelly Brazil";
.parsers[4].author_email = "kellyjonbrazil@gmail.com";
.parsers[4].compatible[0] = "linux";
.parsers[4].compatible[1] = "darwin";
.parsers[4].compatible[2] = "aix";
.parsers[4].compatible[3] = "freebsd";
.parsers[4].magic_commands[0] = "crontab";
.parsers[5].name = "crontab_u";
.parsers[5].argument = "--crontab-u";
.parsers[5].version = "1.0";
.parsers[5].description = "crontab file parser with user support";
.parsers[5].author = "Kelly Brazil";
.parsers[5].author_email = "kellyjonbrazil@gmail.com";
.parsers[5].compatible[0] = "linux";
.parsers[5].compatible[1] = "darwin";
.parsers[5].compatible[2] = "aix";
.parsers[5].compatible[3] = "freebsd";
.parsers[6].name = "csv";
.parsers[6].argument = "--csv";
.parsers[6].version = "1.0";
.parsers[6].description = "CSV file parser";
.parsers[6].author = "Kelly Brazil";
.parsers[6].author_email = "kellyjonbrazil@gmail.com";
.parsers[6].details = "Using the python standard csv library";
.parsers[6].compatible[0] = "linux";
.parsers[6].compatible[1] = "darwin";
.parsers[6].compatible[2] = "cygwin";
.parsers[6].compatible[3] = "win32";
.parsers[6].compatible[4] = "aix";
.parsers[6].compatible[5] = "freebsd";
.parsers[7].name = "df";
.parsers[7].argument = "--df";
.parsers[7].version = "1.1";
.parsers[7].description = "df command parser";
.parsers[7].author = "Kelly Brazil";
.parsers[7].author_email = "kellyjonbrazil@gmail.com";
.parsers[7].compatible[0] = "linux";
.parsers[7].compatible[1] = "darwin";
.parsers[7].magic_commands[0] = "df";
.parsers[8].name = "dig";
.parsers[8].argument = "--dig";
.parsers[8].version = "1.1";
.parsers[8].description = "dig command parser";
.parsers[8].author = "Kelly Brazil";
.parsers[8].author_email = "kellyjonbrazil@gmail.com";
.parsers[8].compatible[0] = "linux";
.parsers[8].compatible[1] = "aix";
.parsers[8].compatible[2] = "freebsd";
.parsers[8].compatible[3] = "darwin";
.parsers[8].magic_commands[0] = "dig";
.parsers[9].name = "du";
.parsers[9].argument = "--du";
.parsers[9].version = "1.1";
.parsers[9].description = "du command parser";
.parsers[9].author = "Kelly Brazil";
.parsers[9].author_email = "kellyjonbrazil@gmail.com";
.parsers[9].compatible[0] = "linux";
.parsers[9].compatible[1] = "darwin";
.parsers[9].compatible[2] = "aix";
.parsers[9].compatible[3] = "freebsd";
.parsers[9].magic_commands[0] = "du";
.parsers[10].name = "env";
.parsers[10].argument = "--env";
.parsers[10].version = "1.1";
.parsers[10].description = "env command parser";
.parsers[10].author = "Kelly Brazil";
.parsers[10].author_email = "kellyjonbrazil@gmail.com";
.parsers[10].compatible[0] = "linux";
.parsers[10].compatible[1] = "darwin";
.parsers[10].compatible[2] = "cygwin";
.parsers[10].compatible[3] = "win32";
.parsers[10].compatible[4] = "aix";
.parsers[10].compatible[5] = "freebsd";
.parsers[10].magic_commands[0] = "env";
.parsers[11].name = "file";
.parsers[11].argument = "--file";
.parsers[11].version = "1.1";
.parsers[11].description = "file command parser";
.parsers[11].author = "Kelly Brazil";
.parsers[11].author_email = "kellyjonbrazil@gmail.com";
.parsers[11].compatible[0] = "linux";
.parsers[11].compatible[1] = "aix";
.parsers[11].compatible[2] = "freebsd";
.parsers[11].compatible[3] = "darwin";
.parsers[11].magic_commands[0] = "file";
.parsers[12].name = "free";
.parsers[12].argument = "--free";
.parsers[12].version = "1.0";
.parsers[12].description = "free command parser";
.parsers[12].author = "Kelly Brazil";
.parsers[12].author_email = "kellyjonbrazil@gmail.com";
.parsers[12].compatible[0] = "linux";
.parsers[12].magic_commands[0] = "free";
.parsers[13].name = "fstab";
.parsers[13].argument = "--fstab";
.parsers[13].version = "1.0";
.parsers[13].description = "fstab file parser";
.parsers[13].author = "Kelly Brazil";
.parsers[13].author_email = "kellyjonbrazil@gmail.com";
.parsers[13].compatible[0] = "linux";
.parsers[14].name = "group";
.parsers[14].argument = "--group";
.parsers[14].version = "1.0";
.parsers[14].description = "/etc/group file parser";
.parsers[14].author = "Kelly Brazil";
.parsers[14].author_email = "kellyjonbrazil@gmail.com";
.parsers[14].compatible[0] = "linux";
.parsers[14].compatible[1] = "darwin";
.parsers[14].compatible[2] = "aix";
.parsers[14].compatible[3] = "freebsd";
.parsers[15].name = "gshadow";
.parsers[15].argument = "--gshadow";
.parsers[15].version = "1.0";
.parsers[15].description = "/etc/gshadow file parser";
.parsers[15].author = "Kelly Brazil";
.parsers[15].author_email = "kellyjonbrazil@gmail.com";
.parsers[15].compatible[0] = "linux";
.parsers[15].compatible[1] = "aix";
.parsers[15].compatible[2] = "freebsd";
.parsers[16].name = "history";
.parsers[16].argument = "--history";
.parsers[16].version = "1.2";
.parsers[16].description = "history command parser";
.parsers[16].author = "Kelly Brazil";
.parsers[16].author_email = "kellyjonbrazil@gmail.com";
.parsers[16].details = "Optimizations by https://github.com/philippeitis";
.parsers[16].compatible[0] = "linux";
.parsers[16].compatible[1] = "darwin";
.parsers[16].compatible[2] = "cygwin";
.parsers[16].compatible[3] = "aix";
.parsers[16].compatible[4] = "freebsd";
.parsers[17].name = "hosts";
.parsers[17].argument = "--hosts";
.parsers[17].version = "1.0";
.parsers[17].description = "/etc/hosts file parser";
.parsers[17].author = "Kelly Brazil";
.parsers[17].author_email = "kellyjonbrazil@gmail.com";
.parsers[17].compatible[0] = "linux";
.parsers[17].compatible[1] = "darwin";
.parsers[17].compatible[2] = "cygwin";
.parsers[17].compatible[3] = "win32";
.parsers[17].compatible[4] = "aix";
.parsers[17].compatible[5] = "freebsd";
.parsers[18].name = "id";
.parsers[18].argument = "--id";
.parsers[18].version = "1.0";
.parsers[18].description = "id command parser";
.parsers[18].author = "Kelly Brazil";
.parsers[18].author_email = "kellyjonbrazil@gmail.com";
.parsers[18].compatible[0] = "linux";
.parsers[18].compatible[1] = "darwin";
.parsers[18].compatible[2] = "aix";
.parsers[18].compatible[3] = "freebsd";
.parsers[18].magic_commands[0] = "id";
.parsers[19].name = "ifconfig";
.parsers[19].argument = "--ifconfig";
.parsers[19].version = "1.5";
.parsers[19].description = "ifconfig command parser";
.parsers[19].author = "Kelly Brazil";
.parsers[19].author_email = "kellyjonbrazil@gmail.com";
.parsers[19].details = "Using ifconfig-parser package from https://github.com/KnightWhoSayNi/ifconfig-parser";
.parsers[19].compatible[0] = "linux";
.parsers[19].compatible[1] = "aix";
.parsers[19].compatible[2] = "freebsd";
.parsers[19].compatible[3] = "darwin";
.parsers[19].magic_commands[0] = "ifconfig";
.parsers[20].name = "ini";
.parsers[20].argument = "--ini";
.parsers[20].version = "1.0";
.parsers[20].description = "INI file parser";
.parsers[20].author = "Kelly Brazil";
.parsers[20].author_email = "kellyjonbrazil@gmail.com";
.parsers[20].details = "Using configparser from the standard library";
.parsers[20].compatible[0] = "linux";
.parsers[20].compatible[1] = "darwin";
.parsers[20].compatible[2] = "cygwin";
.parsers[20].compatible[3] = "win32";
.parsers[20].compatible[4] = "aix";
.parsers[20].compatible[5] = "freebsd";
.parsers[21].name = "iptables";
.parsers[21].argument = "--iptables";
.parsers[21].version = "1.1";
.parsers[21].description = "iptables command parser";
.parsers[21].author = "Kelly Brazil";
.parsers[21].author_email = "kellyjonbrazil@gmail.com";
.parsers[21].compatible[0] = "linux";
.parsers[21].magic_commands[0] = "iptables";
.parsers[22].name = "jobs";
.parsers[22].argument = "--jobs";
.parsers[22].version = "1.0";
.parsers[22].description = "jobs command parser";
.parsers[22].author = "Kelly Brazil";
.parsers[22].author_email = "kellyjonbrazil@gmail.com";
.parsers[22].compatible[0] = "linux";
.parsers[22].compatible[1] = "darwin";
.parsers[22].compatible[2] = "cygwin";
.parsers[22].compatible[3] = "aix";
.parsers[22].compatible[4] = "freebsd";
.parsers[22].magic_commands[0] = "jobs";
.parsers[23].name = "last";
.parsers[23].argument = "--last";
.parsers[23].version = "1.0";
.parsers[23].description = "last and lastb command parser";
.parsers[23].author = "Kelly Brazil";
.parsers[23].author_email = "kellyjonbrazil@gmail.com";
.parsers[23].compatible[0] = "linux";
.parsers[23].compatible[1] = "darwin";
.parsers[23].compatible[2] = "aix";
.parsers[23].compatible[3] = "freebsd";
.parsers[23].magic_commands[0] = "last";
.parsers[23].magic_commands[1] = "lastb";
.parsers[24].name = "ls";
.parsers[24].argument = "--ls";
.parsers[24].version = "1.3";
.parsers[24].description = "ls command parser";
.parsers[24].author = "Kelly Brazil";
.parsers[24].author_email = "kellyjonbrazil@gmail.com";
.parsers[24].compatible[0] = "linux";
.parsers[24].compatible[1] = "darwin";
.parsers[24].compatible[2] = "cygwin";
.parsers[24].compatible[3] = "aix";
.parsers[24].compatible[4] = "freebsd";
.parsers[24].magic_commands[0] = "ls";
.parsers[25].name = "lsblk";
.parsers[25].argument = "--lsblk";
.parsers[25].version = "1.3";
.parsers[25].description = "lsblk command parser";
.parsers[25].author = "Kelly Brazil";
.parsers[25].author_email = "kellyjonbrazil@gmail.com";
.parsers[25].compatible[0] = "linux";
.parsers[25].magic_commands[0] = "lsblk";
.parsers[26].name = "lsmod";
.parsers[26].argument = "--lsmod";
.parsers[26].version = "1.1";
.parsers[26].description = "lsmod command parser";
.parsers[26].author = "Kelly Brazil";
.parsers[26].author_email = "kellyjonbrazil@gmail.com";
.parsers[26].compatible[0] = "linux";
.parsers[26].magic_commands[0] = "lsmod";
.parsers[27].name = "lsof";
.parsers[27].argument = "--lsof";
.parsers[27].version = "1.0";
.parsers[27].description = "lsof command parser";
.parsers[27].author = "Kelly Brazil";
.parsers[27].author_email = "kellyjonbrazil@gmail.com";
.parsers[27].compatible[0] = "linux";
.parsers[27].magic_commands[0] = "lsof";
.parsers[28].name = "mount";
.parsers[28].argument = "--mount";
.parsers[28].version = "1.1";
.parsers[28].description = "mount command parser";
.parsers[28].author = "Kelly Brazil";
.parsers[28].author_email = "kellyjonbrazil@gmail.com";
.parsers[28].compatible[0] = "linux";
.parsers[28].compatible[1] = "darwin";
.parsers[28].magic_commands[0] = "mount";
.parsers[29].name = "netstat";
.parsers[29].argument = "--netstat";
.parsers[29].version = "1.2";
.parsers[29].description = "netstat command parser";
.parsers[29].author = "Kelly Brazil";
.parsers[29].author_email = "kellyjonbrazil@gmail.com";
.parsers[29].compatible[0] = "linux";
.parsers[29].magic_commands[0] = "netstat";
.parsers[30].name = "ntpq";
.parsers[30].argument = "--ntpq";
.parsers[30].version = "1.0";
.parsers[30].description = "ntpq -p command parser";
.parsers[30].author = "Kelly Brazil";
.parsers[30].author_email = "kellyjonbrazil@gmail.com";
.parsers[30].compatible[0] = "linux";
.parsers[30].magic_commands[0] = "ntpq";
.parsers[31].name = "passwd";
.parsers[31].argument = "--passwd";
.parsers[31].version = "1.0";
.parsers[31].description = "/etc/passwd file parser";
.parsers[31].author = "Kelly Brazil";
.parsers[31].author_email = "kellyjonbrazil@gmail.com";
.parsers[31].compatible[0] = "linux";
.parsers[31].compatible[1] = "darwin";
.parsers[31].compatible[2] = "aix";
.parsers[31].compatible[3] = "freebsd";
.parsers[32].name = "pip_list";
.parsers[32].argument = "--pip-list";
.parsers[32].version = "1.0";
.parsers[32].description = "pip list command parser";
.parsers[32].author = "Kelly Brazil";
.parsers[32].author_email = "kellyjonbrazil@gmail.com";
.parsers[32].compatible[0] = "linux";
.parsers[32].compatible[1] = "darwin";
.parsers[32].compatible[2] = "cygwin";
.parsers[32].compatible[3] = "win32";
.parsers[32].compatible[4] = "aix";
.parsers[32].compatible[5] = "freebsd";
.parsers[32].magic_commands[0] = "pip list";
.parsers[32].magic_commands[1] = "pip3 list";
.parsers[33].name = "pip_show";
.parsers[33].argument = "--pip-show";
.parsers[33].version = "1.0";
.parsers[33].description = "pip show command parser";
.parsers[33].author = "Kelly Brazil";
.parsers[33].author_email = "kellyjonbrazil@gmail.com";
.parsers[33].compatible[0] = "linux";
.parsers[33].compatible[1] = "darwin";
.parsers[33].compatible[2] = "cygwin";
.parsers[33].compatible[3] = "win32";
.parsers[33].compatible[4] = "aix";
.parsers[33].compatible[5] = "freebsd";
.parsers[33].magic_commands[0] = "pip show";
.parsers[33].magic_commands[1] = "pip3 show";
.parsers[34].name = "ps";
.parsers[34].argument = "--ps";
.parsers[34].version = "1.1";
.parsers[34].description = "ps command parser";
.parsers[34].author = "Kelly Brazil";
.parsers[34].author_email = "kellyjonbrazil@gmail.com";
.parsers[34].compatible[0] = "linux";
.parsers[34].compatible[1] = "darwin";
.parsers[34].compatible[2] = "cygwin";
.parsers[34].compatible[3] = "aix";
.parsers[34].compatible[4] = "freebsd";
.parsers[34].magic_commands[0] = "ps";
.parsers[35].name = "route";
.parsers[35].argument = "--route";
.parsers[35].version = "1.0";
.parsers[35].description = "route command parser";
.parsers[35].author = "Kelly Brazil";
.parsers[35].author_email = "kellyjonbrazil@gmail.com";
.parsers[35].compatible[0] = "linux";
.parsers[35].magic_commands[0] = "route";
.parsers[36].name = "shadow";
.parsers[36].argument = "--shadow";
.parsers[36].version = "1.0";
.parsers[36].description = "/etc/shadow file parser";
.parsers[36].author = "Kelly Brazil";
.parsers[36].author_email = "kellyjonbrazil@gmail.com";
.parsers[36].compatible[0] = "linux";
.parsers[36].compatible[1] = "darwin";
.parsers[36].compatible[2] = "aix";
.parsers[36].compatible[3] = "freebsd";
.parsers[37].name = "ss";
.parsers[37].argument = "--ss";
.parsers[37].version = "1.0";
.parsers[37].description = "ss command parser";
.parsers[37].author = "Kelly Brazil";
.parsers[37].author_email = "kellyjonbrazil@gmail.com";
.parsers[37].compatible[0] = "linux";
.parsers[37].magic_commands[0] = "ss";
.parsers[38].name = "stat";
.parsers[38].argument = "--stat";
.parsers[38].version = "1.0";
.parsers[38].description = "stat command parser";
.parsers[38].author = "Kelly Brazil";
.parsers[38].author_email = "kellyjonbrazil@gmail.com";
.parsers[38].compatible[0] = "linux";
.parsers[38].magic_commands[0] = "stat";
.parsers[39].name = "systemctl";
.parsers[39].argument = "--systemctl";
.parsers[39].version = "1.0";
.parsers[39].description = "systemctl command parser";
.parsers[39].author = "Kelly Brazil";
.parsers[39].author_email = "kellyjonbrazil@gmail.com";
.parsers[39].compatible[0] = "linux";
.parsers[39].magic_commands[0] = "systemctl";
.parsers[40].name = "systemctl_lj";
.parsers[40].argument = "--systemctl-lj";
.parsers[40].version = "1.0";
.parsers[40].description = "systemctl list-jobs command parser";
.parsers[40].author = "Kelly Brazil";
.parsers[40].author_email = "kellyjonbrazil@gmail.com";
.parsers[40].compatible[0] = "linux";
.parsers[40].magic_commands[0] = "systemctl list-jobs";
.parsers[41].name = "systemctl_ls";
.parsers[41].argument = "--systemctl-ls";
.parsers[41].version = "1.0";
.parsers[41].description = "systemctl list-sockets command parser";
.parsers[41].author = "Kelly Brazil";
.parsers[41].author_email = "kellyjonbrazil@gmail.com";
.parsers[41].compatible[0] = "linux";
.parsers[41].magic_commands[0] = "systemctl list-sockets";
.parsers[42].name = "systemctl_luf";
.parsers[42].argument = "--systemctl-luf";
.parsers[42].version = "1.0";
.parsers[42].description = "systemctl list-unit-files command parser";
.parsers[42].author = "Kelly Brazil";
.parsers[42].author_email = "kellyjonbrazil@gmail.com";
.parsers[42].compatible[0] = "linux";
.parsers[42].magic_commands[0] = "systemctl list-unit-files";
.parsers[43].name = "timedatectl";
.parsers[43].argument = "--timedatectl";
.parsers[43].version = "1.0";
.parsers[43].description = "timedatectl status command parser";
.parsers[43].author = "Kelly Brazil";
.parsers[43].author_email = "kellyjonbrazil@gmail.com";
.parsers[43].compatible[0] = "linux";
.parsers[43].magic_commands[0] = "timedatectl";
.parsers[43].magic_commands[1] = "timedatectl status";
.parsers[44].name = "uname";
.parsers[44].argument = "--uname";
.parsers[44].version = "1.1";
.parsers[44].description = "uname -a command parser";
.parsers[44].author = "Kelly Brazil";
.parsers[44].author_email = "kellyjonbrazil@gmail.com";
.parsers[44].compatible[0] = "linux";
.parsers[44].compatible[1] = "darwin";
.parsers[44].magic_commands[0] = "uname";
.parsers[45].name = "uptime";
.parsers[45].argument = "--uptime";
.parsers[45].version = "1.0";
.parsers[45].description = "uptime command parser";
.parsers[45].author = "Kelly Brazil";
.parsers[45].author_email = "kellyjonbrazil@gmail.com";
.parsers[45].compatible[0] = "linux";
.parsers[45].compatible[1] = "darwin";
.parsers[45].compatible[2] = "cygwin";
.parsers[45].compatible[3] = "aix";
.parsers[45].compatible[4] = "freebsd";
.parsers[45].magic_commands[0] = "uptime";
.parsers[46].name = "w";
.parsers[46].argument = "--w";
.parsers[46].version = "1.0";
.parsers[46].description = "w command parser";
.parsers[46].author = "Kelly Brazil";
.parsers[46].author_email = "kellyjonbrazil@gmail.com";
.parsers[46].compatible[0] = "linux";
.parsers[46].compatible[1] = "darwin";
.parsers[46].compatible[2] = "cygwin";
.parsers[46].compatible[3] = "aix";
.parsers[46].compatible[4] = "freebsd";
.parsers[46].magic_commands[0] = "w";
.parsers[47].name = "who";
.parsers[47].argument = "--who";
.parsers[47].version = "1.0";
.parsers[47].description = "who command parser";
.parsers[47].author = "Kelly Brazil";
.parsers[47].author_email = "kellyjonbrazil@gmail.com";
.parsers[47].compatible[0] = "linux";
.parsers[47].compatible[1] = "darwin";
.parsers[47].compatible[2] = "cygwin";
.parsers[47].compatible[3] = "aix";
.parsers[47].compatible[4] = "freebsd";
.parsers[47].magic_commands[0] = "who";
.parsers[48].name = "xml";
.parsers[48].argument = "--xml";
.parsers[48].version = "1.0";
.parsers[48].description = "XML file parser";
.parsers[48].author = "Kelly Brazil";
.parsers[48].author_email = "kellyjonbrazil@gmail.com";
.parsers[48].details = "Using the xmltodict library at https://github.com/martinblech/xmltodict";
.parsers[48].compatible[0] = "linux";
.parsers[48].compatible[1] = "darwin";
.parsers[48].compatible[2] = "cygwin";
.parsers[48].compatible[3] = "win32";
.parsers[48].compatible[4] = "aix";
.parsers[48].compatible[5] = "freebsd";
.parsers[49].name = "yaml";
.parsers[49].argument = "--yaml";
.parsers[49].version = "1.0";
.parsers[49].description = "YAML file parser";
.parsers[49].author = "Kelly Brazil";
.parsers[49].author_email = "kellyjonbrazil@gmail.com";
.parsers[49].details = "Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml";
.parsers[49].compatible[0] = "linux";
.parsers[49].compatible[1] = "darwin";
.parsers[49].compatible[2] = "cygwin";
.parsers[49].compatible[3] = "win32";
.parsers[49].compatible[4] = "aix";
.parsers[49].compatible[5] = "freebsd";
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-s']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_parsers(self):
        """
        Test jc -a | jello '_["parsers"]'
        """
        self.expected = '''\
[
  {
    "name": "airport",
    "argument": "--airport",
    "version": "1.0",
    "description": "airport -I command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "darwin"
    ],
    "magic_commands": [
      "airport -I"
    ]
  },
  {
    "name": "airport_s",
    "argument": "--airport-s",
    "version": "1.0",
    "description": "airport -s command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "darwin"
    ],
    "magic_commands": [
      "airport -s"
    ]
  },
  {
    "name": "arp",
    "argument": "--arp",
    "version": "1.2",
    "description": "arp command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "aix",
      "freebsd",
      "darwin"
    ],
    "magic_commands": [
      "arp"
    ]
  },
  {
    "name": "blkid",
    "argument": "--blkid",
    "version": "1.0",
    "description": "blkid command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "blkid"
    ]
  },
  {
    "name": "crontab",
    "argument": "--crontab",
    "version": "1.1",
    "description": "crontab command and file parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "aix",
      "freebsd"
    ],
    "magic_commands": [
      "crontab"
    ]
  },
  {
    "name": "crontab_u",
    "argument": "--crontab-u",
    "version": "1.0",
    "description": "crontab file parser with user support",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "aix",
      "freebsd"
    ]
  },
  {
    "name": "csv",
    "argument": "--csv",
    "version": "1.0",
    "description": "CSV file parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "details": "Using the python standard csv library",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "win32",
      "aix",
      "freebsd"
    ]
  },
  {
    "name": "df",
    "argument": "--df",
    "version": "1.1",
    "description": "df command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin"
    ],
    "magic_commands": [
      "df"
    ]
  },
  {
    "name": "dig",
    "argument": "--dig",
    "version": "1.1",
    "description": "dig command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "aix",
      "freebsd",
      "darwin"
    ],
    "magic_commands": [
      "dig"
    ]
  },
  {
    "name": "du",
    "argument": "--du",
    "version": "1.1",
    "description": "du command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "aix",
      "freebsd"
    ],
    "magic_commands": [
      "du"
    ]
  },
  {
    "name": "env",
    "argument": "--env",
    "version": "1.1",
    "description": "env command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "win32",
      "aix",
      "freebsd"
    ],
    "magic_commands": [
      "env"
    ]
  },
  {
    "name": "file",
    "argument": "--file",
    "version": "1.1",
    "description": "file command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "aix",
      "freebsd",
      "darwin"
    ],
    "magic_commands": [
      "file"
    ]
  },
  {
    "name": "free",
    "argument": "--free",
    "version": "1.0",
    "description": "free command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "free"
    ]
  },
  {
    "name": "fstab",
    "argument": "--fstab",
    "version": "1.0",
    "description": "fstab file parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ]
  },
  {
    "name": "group",
    "argument": "--group",
    "version": "1.0",
    "description": "/etc/group file parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "aix",
      "freebsd"
    ]
  },
  {
    "name": "gshadow",
    "argument": "--gshadow",
    "version": "1.0",
    "description": "/etc/gshadow file parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "aix",
      "freebsd"
    ]
  },
  {
    "name": "history",
    "argument": "--history",
    "version": "1.2",
    "description": "history command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "details": "Optimizations by https://github.com/philippeitis",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "aix",
      "freebsd"
    ]
  },
  {
    "name": "hosts",
    "argument": "--hosts",
    "version": "1.0",
    "description": "/etc/hosts file parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "win32",
      "aix",
      "freebsd"
    ]
  },
  {
    "name": "id",
    "argument": "--id",
    "version": "1.0",
    "description": "id command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "aix",
      "freebsd"
    ],
    "magic_commands": [
      "id"
    ]
  },
  {
    "name": "ifconfig",
    "argument": "--ifconfig",
    "version": "1.5",
    "description": "ifconfig command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "details": "Using ifconfig-parser package from https://github.com/KnightWhoSayNi/ifconfig-parser",
    "compatible": [
      "linux",
      "aix",
      "freebsd",
      "darwin"
    ],
    "magic_commands": [
      "ifconfig"
    ]
  },
  {
    "name": "ini",
    "argument": "--ini",
    "version": "1.0",
    "description": "INI file parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "details": "Using configparser from the standard library",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "win32",
      "aix",
      "freebsd"
    ]
  },
  {
    "name": "iptables",
    "argument": "--iptables",
    "version": "1.1",
    "description": "iptables command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "iptables"
    ]
  },
  {
    "name": "jobs",
    "argument": "--jobs",
    "version": "1.0",
    "description": "jobs command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "aix",
      "freebsd"
    ],
    "magic_commands": [
      "jobs"
    ]
  },
  {
    "name": "last",
    "argument": "--last",
    "version": "1.0",
    "description": "last and lastb command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "aix",
      "freebsd"
    ],
    "magic_commands": [
      "last",
      "lastb"
    ]
  },
  {
    "name": "ls",
    "argument": "--ls",
    "version": "1.3",
    "description": "ls command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "aix",
      "freebsd"
    ],
    "magic_commands": [
      "ls"
    ]
  },
  {
    "name": "lsblk",
    "argument": "--lsblk",
    "version": "1.3",
    "description": "lsblk command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "lsblk"
    ]
  },
  {
    "name": "lsmod",
    "argument": "--lsmod",
    "version": "1.1",
    "description": "lsmod command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "lsmod"
    ]
  },
  {
    "name": "lsof",
    "argument": "--lsof",
    "version": "1.0",
    "description": "lsof command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "lsof"
    ]
  },
  {
    "name": "mount",
    "argument": "--mount",
    "version": "1.1",
    "description": "mount command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin"
    ],
    "magic_commands": [
      "mount"
    ]
  },
  {
    "name": "netstat",
    "argument": "--netstat",
    "version": "1.2",
    "description": "netstat command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "netstat"
    ]
  },
  {
    "name": "ntpq",
    "argument": "--ntpq",
    "version": "1.0",
    "description": "ntpq -p command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "ntpq"
    ]
  },
  {
    "name": "passwd",
    "argument": "--passwd",
    "version": "1.0",
    "description": "/etc/passwd file parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "aix",
      "freebsd"
    ]
  },
  {
    "name": "pip_list",
    "argument": "--pip-list",
    "version": "1.0",
    "description": "pip list command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "win32",
      "aix",
      "freebsd"
    ],
    "magic_commands": [
      "pip list",
      "pip3 list"
    ]
  },
  {
    "name": "pip_show",
    "argument": "--pip-show",
    "version": "1.0",
    "description": "pip show command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "win32",
      "aix",
      "freebsd"
    ],
    "magic_commands": [
      "pip show",
      "pip3 show"
    ]
  },
  {
    "name": "ps",
    "argument": "--ps",
    "version": "1.1",
    "description": "ps command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "aix",
      "freebsd"
    ],
    "magic_commands": [
      "ps"
    ]
  },
  {
    "name": "route",
    "argument": "--route",
    "version": "1.0",
    "description": "route command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "route"
    ]
  },
  {
    "name": "shadow",
    "argument": "--shadow",
    "version": "1.0",
    "description": "/etc/shadow file parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "aix",
      "freebsd"
    ]
  },
  {
    "name": "ss",
    "argument": "--ss",
    "version": "1.0",
    "description": "ss command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "ss"
    ]
  },
  {
    "name": "stat",
    "argument": "--stat",
    "version": "1.0",
    "description": "stat command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "stat"
    ]
  },
  {
    "name": "systemctl",
    "argument": "--systemctl",
    "version": "1.0",
    "description": "systemctl command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "systemctl"
    ]
  },
  {
    "name": "systemctl_lj",
    "argument": "--systemctl-lj",
    "version": "1.0",
    "description": "systemctl list-jobs command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "systemctl list-jobs"
    ]
  },
  {
    "name": "systemctl_ls",
    "argument": "--systemctl-ls",
    "version": "1.0",
    "description": "systemctl list-sockets command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "systemctl list-sockets"
    ]
  },
  {
    "name": "systemctl_luf",
    "argument": "--systemctl-luf",
    "version": "1.0",
    "description": "systemctl list-unit-files command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "systemctl list-unit-files"
    ]
  },
  {
    "name": "timedatectl",
    "argument": "--timedatectl",
    "version": "1.0",
    "description": "timedatectl status command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux"
    ],
    "magic_commands": [
      "timedatectl",
      "timedatectl status"
    ]
  },
  {
    "name": "uname",
    "argument": "--uname",
    "version": "1.1",
    "description": "uname -a command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin"
    ],
    "magic_commands": [
      "uname"
    ]
  },
  {
    "name": "uptime",
    "argument": "--uptime",
    "version": "1.0",
    "description": "uptime command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "aix",
      "freebsd"
    ],
    "magic_commands": [
      "uptime"
    ]
  },
  {
    "name": "w",
    "argument": "--w",
    "version": "1.0",
    "description": "w command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "aix",
      "freebsd"
    ],
    "magic_commands": [
      "w"
    ]
  },
  {
    "name": "who",
    "argument": "--who",
    "version": "1.0",
    "description": "who command parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "aix",
      "freebsd"
    ],
    "magic_commands": [
      "who"
    ]
  },
  {
    "name": "xml",
    "argument": "--xml",
    "version": "1.0",
    "description": "XML file parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "details": "Using the xmltodict library at https://github.com/martinblech/xmltodict",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "win32",
      "aix",
      "freebsd"
    ]
  },
  {
    "name": "yaml",
    "argument": "--yaml",
    "version": "1.0",
    "description": "YAML file parser",
    "author": "Kelly Brazil",
    "author_email": "kellyjonbrazil@gmail.com",
    "details": "Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml",
    "compatible": [
      "linux",
      "darwin",
      "cygwin",
      "win32",
      "aix",
      "freebsd"
    ]
  }
]
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '_["parsers"]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_s_parsers_dot(self):
        """
        Test jc -a | jello -s '_.parsers'
        """
        self.expected = '''\
.[0].name = "airport";
.[0].argument = "--airport";
.[0].version = "1.0";
.[0].description = "airport -I command parser";
.[0].author = "Kelly Brazil";
.[0].author_email = "kellyjonbrazil@gmail.com";
.[0].compatible[0] = "darwin";
.[0].magic_commands[0] = "airport -I";
.[1].name = "airport_s";
.[1].argument = "--airport-s";
.[1].version = "1.0";
.[1].description = "airport -s command parser";
.[1].author = "Kelly Brazil";
.[1].author_email = "kellyjonbrazil@gmail.com";
.[1].compatible[0] = "darwin";
.[1].magic_commands[0] = "airport -s";
.[2].name = "arp";
.[2].argument = "--arp";
.[2].version = "1.2";
.[2].description = "arp command parser";
.[2].author = "Kelly Brazil";
.[2].author_email = "kellyjonbrazil@gmail.com";
.[2].compatible[0] = "linux";
.[2].compatible[1] = "aix";
.[2].compatible[2] = "freebsd";
.[2].compatible[3] = "darwin";
.[2].magic_commands[0] = "arp";
.[3].name = "blkid";
.[3].argument = "--blkid";
.[3].version = "1.0";
.[3].description = "blkid command parser";
.[3].author = "Kelly Brazil";
.[3].author_email = "kellyjonbrazil@gmail.com";
.[3].compatible[0] = "linux";
.[3].magic_commands[0] = "blkid";
.[4].name = "crontab";
.[4].argument = "--crontab";
.[4].version = "1.1";
.[4].description = "crontab command and file parser";
.[4].author = "Kelly Brazil";
.[4].author_email = "kellyjonbrazil@gmail.com";
.[4].compatible[0] = "linux";
.[4].compatible[1] = "darwin";
.[4].compatible[2] = "aix";
.[4].compatible[3] = "freebsd";
.[4].magic_commands[0] = "crontab";
.[5].name = "crontab_u";
.[5].argument = "--crontab-u";
.[5].version = "1.0";
.[5].description = "crontab file parser with user support";
.[5].author = "Kelly Brazil";
.[5].author_email = "kellyjonbrazil@gmail.com";
.[5].compatible[0] = "linux";
.[5].compatible[1] = "darwin";
.[5].compatible[2] = "aix";
.[5].compatible[3] = "freebsd";
.[6].name = "csv";
.[6].argument = "--csv";
.[6].version = "1.0";
.[6].description = "CSV file parser";
.[6].author = "Kelly Brazil";
.[6].author_email = "kellyjonbrazil@gmail.com";
.[6].details = "Using the python standard csv library";
.[6].compatible[0] = "linux";
.[6].compatible[1] = "darwin";
.[6].compatible[2] = "cygwin";
.[6].compatible[3] = "win32";
.[6].compatible[4] = "aix";
.[6].compatible[5] = "freebsd";
.[7].name = "df";
.[7].argument = "--df";
.[7].version = "1.1";
.[7].description = "df command parser";
.[7].author = "Kelly Brazil";
.[7].author_email = "kellyjonbrazil@gmail.com";
.[7].compatible[0] = "linux";
.[7].compatible[1] = "darwin";
.[7].magic_commands[0] = "df";
.[8].name = "dig";
.[8].argument = "--dig";
.[8].version = "1.1";
.[8].description = "dig command parser";
.[8].author = "Kelly Brazil";
.[8].author_email = "kellyjonbrazil@gmail.com";
.[8].compatible[0] = "linux";
.[8].compatible[1] = "aix";
.[8].compatible[2] = "freebsd";
.[8].compatible[3] = "darwin";
.[8].magic_commands[0] = "dig";
.[9].name = "du";
.[9].argument = "--du";
.[9].version = "1.1";
.[9].description = "du command parser";
.[9].author = "Kelly Brazil";
.[9].author_email = "kellyjonbrazil@gmail.com";
.[9].compatible[0] = "linux";
.[9].compatible[1] = "darwin";
.[9].compatible[2] = "aix";
.[9].compatible[3] = "freebsd";
.[9].magic_commands[0] = "du";
.[10].name = "env";
.[10].argument = "--env";
.[10].version = "1.1";
.[10].description = "env command parser";
.[10].author = "Kelly Brazil";
.[10].author_email = "kellyjonbrazil@gmail.com";
.[10].compatible[0] = "linux";
.[10].compatible[1] = "darwin";
.[10].compatible[2] = "cygwin";
.[10].compatible[3] = "win32";
.[10].compatible[4] = "aix";
.[10].compatible[5] = "freebsd";
.[10].magic_commands[0] = "env";
.[11].name = "file";
.[11].argument = "--file";
.[11].version = "1.1";
.[11].description = "file command parser";
.[11].author = "Kelly Brazil";
.[11].author_email = "kellyjonbrazil@gmail.com";
.[11].compatible[0] = "linux";
.[11].compatible[1] = "aix";
.[11].compatible[2] = "freebsd";
.[11].compatible[3] = "darwin";
.[11].magic_commands[0] = "file";
.[12].name = "free";
.[12].argument = "--free";
.[12].version = "1.0";
.[12].description = "free command parser";
.[12].author = "Kelly Brazil";
.[12].author_email = "kellyjonbrazil@gmail.com";
.[12].compatible[0] = "linux";
.[12].magic_commands[0] = "free";
.[13].name = "fstab";
.[13].argument = "--fstab";
.[13].version = "1.0";
.[13].description = "fstab file parser";
.[13].author = "Kelly Brazil";
.[13].author_email = "kellyjonbrazil@gmail.com";
.[13].compatible[0] = "linux";
.[14].name = "group";
.[14].argument = "--group";
.[14].version = "1.0";
.[14].description = "/etc/group file parser";
.[14].author = "Kelly Brazil";
.[14].author_email = "kellyjonbrazil@gmail.com";
.[14].compatible[0] = "linux";
.[14].compatible[1] = "darwin";
.[14].compatible[2] = "aix";
.[14].compatible[3] = "freebsd";
.[15].name = "gshadow";
.[15].argument = "--gshadow";
.[15].version = "1.0";
.[15].description = "/etc/gshadow file parser";
.[15].author = "Kelly Brazil";
.[15].author_email = "kellyjonbrazil@gmail.com";
.[15].compatible[0] = "linux";
.[15].compatible[1] = "aix";
.[15].compatible[2] = "freebsd";
.[16].name = "history";
.[16].argument = "--history";
.[16].version = "1.2";
.[16].description = "history command parser";
.[16].author = "Kelly Brazil";
.[16].author_email = "kellyjonbrazil@gmail.com";
.[16].details = "Optimizations by https://github.com/philippeitis";
.[16].compatible[0] = "linux";
.[16].compatible[1] = "darwin";
.[16].compatible[2] = "cygwin";
.[16].compatible[3] = "aix";
.[16].compatible[4] = "freebsd";
.[17].name = "hosts";
.[17].argument = "--hosts";
.[17].version = "1.0";
.[17].description = "/etc/hosts file parser";
.[17].author = "Kelly Brazil";
.[17].author_email = "kellyjonbrazil@gmail.com";
.[17].compatible[0] = "linux";
.[17].compatible[1] = "darwin";
.[17].compatible[2] = "cygwin";
.[17].compatible[3] = "win32";
.[17].compatible[4] = "aix";
.[17].compatible[5] = "freebsd";
.[18].name = "id";
.[18].argument = "--id";
.[18].version = "1.0";
.[18].description = "id command parser";
.[18].author = "Kelly Brazil";
.[18].author_email = "kellyjonbrazil@gmail.com";
.[18].compatible[0] = "linux";
.[18].compatible[1] = "darwin";
.[18].compatible[2] = "aix";
.[18].compatible[3] = "freebsd";
.[18].magic_commands[0] = "id";
.[19].name = "ifconfig";
.[19].argument = "--ifconfig";
.[19].version = "1.5";
.[19].description = "ifconfig command parser";
.[19].author = "Kelly Brazil";
.[19].author_email = "kellyjonbrazil@gmail.com";
.[19].details = "Using ifconfig-parser package from https://github.com/KnightWhoSayNi/ifconfig-parser";
.[19].compatible[0] = "linux";
.[19].compatible[1] = "aix";
.[19].compatible[2] = "freebsd";
.[19].compatible[3] = "darwin";
.[19].magic_commands[0] = "ifconfig";
.[20].name = "ini";
.[20].argument = "--ini";
.[20].version = "1.0";
.[20].description = "INI file parser";
.[20].author = "Kelly Brazil";
.[20].author_email = "kellyjonbrazil@gmail.com";
.[20].details = "Using configparser from the standard library";
.[20].compatible[0] = "linux";
.[20].compatible[1] = "darwin";
.[20].compatible[2] = "cygwin";
.[20].compatible[3] = "win32";
.[20].compatible[4] = "aix";
.[20].compatible[5] = "freebsd";
.[21].name = "iptables";
.[21].argument = "--iptables";
.[21].version = "1.1";
.[21].description = "iptables command parser";
.[21].author = "Kelly Brazil";
.[21].author_email = "kellyjonbrazil@gmail.com";
.[21].compatible[0] = "linux";
.[21].magic_commands[0] = "iptables";
.[22].name = "jobs";
.[22].argument = "--jobs";
.[22].version = "1.0";
.[22].description = "jobs command parser";
.[22].author = "Kelly Brazil";
.[22].author_email = "kellyjonbrazil@gmail.com";
.[22].compatible[0] = "linux";
.[22].compatible[1] = "darwin";
.[22].compatible[2] = "cygwin";
.[22].compatible[3] = "aix";
.[22].compatible[4] = "freebsd";
.[22].magic_commands[0] = "jobs";
.[23].name = "last";
.[23].argument = "--last";
.[23].version = "1.0";
.[23].description = "last and lastb command parser";
.[23].author = "Kelly Brazil";
.[23].author_email = "kellyjonbrazil@gmail.com";
.[23].compatible[0] = "linux";
.[23].compatible[1] = "darwin";
.[23].compatible[2] = "aix";
.[23].compatible[3] = "freebsd";
.[23].magic_commands[0] = "last";
.[23].magic_commands[1] = "lastb";
.[24].name = "ls";
.[24].argument = "--ls";
.[24].version = "1.3";
.[24].description = "ls command parser";
.[24].author = "Kelly Brazil";
.[24].author_email = "kellyjonbrazil@gmail.com";
.[24].compatible[0] = "linux";
.[24].compatible[1] = "darwin";
.[24].compatible[2] = "cygwin";
.[24].compatible[3] = "aix";
.[24].compatible[4] = "freebsd";
.[24].magic_commands[0] = "ls";
.[25].name = "lsblk";
.[25].argument = "--lsblk";
.[25].version = "1.3";
.[25].description = "lsblk command parser";
.[25].author = "Kelly Brazil";
.[25].author_email = "kellyjonbrazil@gmail.com";
.[25].compatible[0] = "linux";
.[25].magic_commands[0] = "lsblk";
.[26].name = "lsmod";
.[26].argument = "--lsmod";
.[26].version = "1.1";
.[26].description = "lsmod command parser";
.[26].author = "Kelly Brazil";
.[26].author_email = "kellyjonbrazil@gmail.com";
.[26].compatible[0] = "linux";
.[26].magic_commands[0] = "lsmod";
.[27].name = "lsof";
.[27].argument = "--lsof";
.[27].version = "1.0";
.[27].description = "lsof command parser";
.[27].author = "Kelly Brazil";
.[27].author_email = "kellyjonbrazil@gmail.com";
.[27].compatible[0] = "linux";
.[27].magic_commands[0] = "lsof";
.[28].name = "mount";
.[28].argument = "--mount";
.[28].version = "1.1";
.[28].description = "mount command parser";
.[28].author = "Kelly Brazil";
.[28].author_email = "kellyjonbrazil@gmail.com";
.[28].compatible[0] = "linux";
.[28].compatible[1] = "darwin";
.[28].magic_commands[0] = "mount";
.[29].name = "netstat";
.[29].argument = "--netstat";
.[29].version = "1.2";
.[29].description = "netstat command parser";
.[29].author = "Kelly Brazil";
.[29].author_email = "kellyjonbrazil@gmail.com";
.[29].compatible[0] = "linux";
.[29].magic_commands[0] = "netstat";
.[30].name = "ntpq";
.[30].argument = "--ntpq";
.[30].version = "1.0";
.[30].description = "ntpq -p command parser";
.[30].author = "Kelly Brazil";
.[30].author_email = "kellyjonbrazil@gmail.com";
.[30].compatible[0] = "linux";
.[30].magic_commands[0] = "ntpq";
.[31].name = "passwd";
.[31].argument = "--passwd";
.[31].version = "1.0";
.[31].description = "/etc/passwd file parser";
.[31].author = "Kelly Brazil";
.[31].author_email = "kellyjonbrazil@gmail.com";
.[31].compatible[0] = "linux";
.[31].compatible[1] = "darwin";
.[31].compatible[2] = "aix";
.[31].compatible[3] = "freebsd";
.[32].name = "pip_list";
.[32].argument = "--pip-list";
.[32].version = "1.0";
.[32].description = "pip list command parser";
.[32].author = "Kelly Brazil";
.[32].author_email = "kellyjonbrazil@gmail.com";
.[32].compatible[0] = "linux";
.[32].compatible[1] = "darwin";
.[32].compatible[2] = "cygwin";
.[32].compatible[3] = "win32";
.[32].compatible[4] = "aix";
.[32].compatible[5] = "freebsd";
.[32].magic_commands[0] = "pip list";
.[32].magic_commands[1] = "pip3 list";
.[33].name = "pip_show";
.[33].argument = "--pip-show";
.[33].version = "1.0";
.[33].description = "pip show command parser";
.[33].author = "Kelly Brazil";
.[33].author_email = "kellyjonbrazil@gmail.com";
.[33].compatible[0] = "linux";
.[33].compatible[1] = "darwin";
.[33].compatible[2] = "cygwin";
.[33].compatible[3] = "win32";
.[33].compatible[4] = "aix";
.[33].compatible[5] = "freebsd";
.[33].magic_commands[0] = "pip show";
.[33].magic_commands[1] = "pip3 show";
.[34].name = "ps";
.[34].argument = "--ps";
.[34].version = "1.1";
.[34].description = "ps command parser";
.[34].author = "Kelly Brazil";
.[34].author_email = "kellyjonbrazil@gmail.com";
.[34].compatible[0] = "linux";
.[34].compatible[1] = "darwin";
.[34].compatible[2] = "cygwin";
.[34].compatible[3] = "aix";
.[34].compatible[4] = "freebsd";
.[34].magic_commands[0] = "ps";
.[35].name = "route";
.[35].argument = "--route";
.[35].version = "1.0";
.[35].description = "route command parser";
.[35].author = "Kelly Brazil";
.[35].author_email = "kellyjonbrazil@gmail.com";
.[35].compatible[0] = "linux";
.[35].magic_commands[0] = "route";
.[36].name = "shadow";
.[36].argument = "--shadow";
.[36].version = "1.0";
.[36].description = "/etc/shadow file parser";
.[36].author = "Kelly Brazil";
.[36].author_email = "kellyjonbrazil@gmail.com";
.[36].compatible[0] = "linux";
.[36].compatible[1] = "darwin";
.[36].compatible[2] = "aix";
.[36].compatible[3] = "freebsd";
.[37].name = "ss";
.[37].argument = "--ss";
.[37].version = "1.0";
.[37].description = "ss command parser";
.[37].author = "Kelly Brazil";
.[37].author_email = "kellyjonbrazil@gmail.com";
.[37].compatible[0] = "linux";
.[37].magic_commands[0] = "ss";
.[38].name = "stat";
.[38].argument = "--stat";
.[38].version = "1.0";
.[38].description = "stat command parser";
.[38].author = "Kelly Brazil";
.[38].author_email = "kellyjonbrazil@gmail.com";
.[38].compatible[0] = "linux";
.[38].magic_commands[0] = "stat";
.[39].name = "systemctl";
.[39].argument = "--systemctl";
.[39].version = "1.0";
.[39].description = "systemctl command parser";
.[39].author = "Kelly Brazil";
.[39].author_email = "kellyjonbrazil@gmail.com";
.[39].compatible[0] = "linux";
.[39].magic_commands[0] = "systemctl";
.[40].name = "systemctl_lj";
.[40].argument = "--systemctl-lj";
.[40].version = "1.0";
.[40].description = "systemctl list-jobs command parser";
.[40].author = "Kelly Brazil";
.[40].author_email = "kellyjonbrazil@gmail.com";
.[40].compatible[0] = "linux";
.[40].magic_commands[0] = "systemctl list-jobs";
.[41].name = "systemctl_ls";
.[41].argument = "--systemctl-ls";
.[41].version = "1.0";
.[41].description = "systemctl list-sockets command parser";
.[41].author = "Kelly Brazil";
.[41].author_email = "kellyjonbrazil@gmail.com";
.[41].compatible[0] = "linux";
.[41].magic_commands[0] = "systemctl list-sockets";
.[42].name = "systemctl_luf";
.[42].argument = "--systemctl-luf";
.[42].version = "1.0";
.[42].description = "systemctl list-unit-files command parser";
.[42].author = "Kelly Brazil";
.[42].author_email = "kellyjonbrazil@gmail.com";
.[42].compatible[0] = "linux";
.[42].magic_commands[0] = "systemctl list-unit-files";
.[43].name = "timedatectl";
.[43].argument = "--timedatectl";
.[43].version = "1.0";
.[43].description = "timedatectl status command parser";
.[43].author = "Kelly Brazil";
.[43].author_email = "kellyjonbrazil@gmail.com";
.[43].compatible[0] = "linux";
.[43].magic_commands[0] = "timedatectl";
.[43].magic_commands[1] = "timedatectl status";
.[44].name = "uname";
.[44].argument = "--uname";
.[44].version = "1.1";
.[44].description = "uname -a command parser";
.[44].author = "Kelly Brazil";
.[44].author_email = "kellyjonbrazil@gmail.com";
.[44].compatible[0] = "linux";
.[44].compatible[1] = "darwin";
.[44].magic_commands[0] = "uname";
.[45].name = "uptime";
.[45].argument = "--uptime";
.[45].version = "1.0";
.[45].description = "uptime command parser";
.[45].author = "Kelly Brazil";
.[45].author_email = "kellyjonbrazil@gmail.com";
.[45].compatible[0] = "linux";
.[45].compatible[1] = "darwin";
.[45].compatible[2] = "cygwin";
.[45].compatible[3] = "aix";
.[45].compatible[4] = "freebsd";
.[45].magic_commands[0] = "uptime";
.[46].name = "w";
.[46].argument = "--w";
.[46].version = "1.0";
.[46].description = "w command parser";
.[46].author = "Kelly Brazil";
.[46].author_email = "kellyjonbrazil@gmail.com";
.[46].compatible[0] = "linux";
.[46].compatible[1] = "darwin";
.[46].compatible[2] = "cygwin";
.[46].compatible[3] = "aix";
.[46].compatible[4] = "freebsd";
.[46].magic_commands[0] = "w";
.[47].name = "who";
.[47].argument = "--who";
.[47].version = "1.0";
.[47].description = "who command parser";
.[47].author = "Kelly Brazil";
.[47].author_email = "kellyjonbrazil@gmail.com";
.[47].compatible[0] = "linux";
.[47].compatible[1] = "darwin";
.[47].compatible[2] = "cygwin";
.[47].compatible[3] = "aix";
.[47].compatible[4] = "freebsd";
.[47].magic_commands[0] = "who";
.[48].name = "xml";
.[48].argument = "--xml";
.[48].version = "1.0";
.[48].description = "XML file parser";
.[48].author = "Kelly Brazil";
.[48].author_email = "kellyjonbrazil@gmail.com";
.[48].details = "Using the xmltodict library at https://github.com/martinblech/xmltodict";
.[48].compatible[0] = "linux";
.[48].compatible[1] = "darwin";
.[48].compatible[2] = "cygwin";
.[48].compatible[3] = "win32";
.[48].compatible[4] = "aix";
.[48].compatible[5] = "freebsd";
.[49].name = "yaml";
.[49].argument = "--yaml";
.[49].version = "1.0";
.[49].description = "YAML file parser";
.[49].author = "Kelly Brazil";
.[49].author_email = "kellyjonbrazil@gmail.com";
.[49].details = "Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml";
.[49].compatible[0] = "linux";
.[49].compatible[1] = "darwin";
.[49].compatible[2] = "cygwin";
.[49].compatible[3] = "win32";
.[49].compatible[4] = "aix";
.[49].compatible[5] = "freebsd";
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-s', '_.parsers']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_c_parsers(self):
        """
        Test jc -a | jello -c '_["parsers"]'
        """
        self.expected = '''[{"name":"airport","argument":"--airport","version":"1.0","description":"airport -I command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["darwin"],"magic_commands":["airport -I"]},{"name":"airport_s","argument":"--airport-s","version":"1.0","description":"airport -s command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["darwin"],"magic_commands":["airport -s"]},{"name":"arp","argument":"--arp","version":"1.2","description":"arp command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["arp"]},{"name":"blkid","argument":"--blkid","version":"1.0","description":"blkid command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["blkid"]},{"name":"crontab","argument":"--crontab","version":"1.1","description":"crontab command and file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["crontab"]},{"name":"crontab_u","argument":"--crontab-u","version":"1.0","description":"crontab file parser with user support","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]},{"name":"csv","argument":"--csv","version":"1.0","description":"CSV file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the python standard csv library","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]},{"name":"df","argument":"--df","version":"1.1","description":"df command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin"],"magic_commands":["df"]},{"name":"dig","argument":"--dig","version":"1.1","description":"dig command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["dig"]},{"name":"du","argument":"--du","version":"1.1","description":"du command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["du"]},{"name":"env","argument":"--env","version":"1.1","description":"env command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["env"]},{"name":"file","argument":"--file","version":"1.1","description":"file command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["file"]},{"name":"free","argument":"--free","version":"1.0","description":"free command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["free"]},{"name":"fstab","argument":"--fstab","version":"1.0","description":"fstab file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"]},{"name":"group","argument":"--group","version":"1.0","description":"/etc/group file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]},{"name":"gshadow","argument":"--gshadow","version":"1.0","description":"/etc/gshadow file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd"]},{"name":"history","argument":"--history","version":"1.2","description":"history command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Optimizations by https://github.com/philippeitis","compatible":["linux","darwin","cygwin","aix","freebsd"]},{"name":"hosts","argument":"--hosts","version":"1.0","description":"/etc/hosts file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]},{"name":"id","argument":"--id","version":"1.0","description":"id command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["id"]},{"name":"ifconfig","argument":"--ifconfig","version":"1.5","description":"ifconfig command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using ifconfig-parser package from https://github.com/KnightWhoSayNi/ifconfig-parser","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["ifconfig"]},{"name":"ini","argument":"--ini","version":"1.0","description":"INI file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using configparser from the standard library","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]},{"name":"iptables","argument":"--iptables","version":"1.1","description":"iptables command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["iptables"]},{"name":"jobs","argument":"--jobs","version":"1.0","description":"jobs command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["jobs"]},{"name":"last","argument":"--last","version":"1.0","description":"last and lastb command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["last","lastb"]},{"name":"ls","argument":"--ls","version":"1.3","description":"ls command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["ls"]},{"name":"lsblk","argument":"--lsblk","version":"1.3","description":"lsblk command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsblk"]},{"name":"lsmod","argument":"--lsmod","version":"1.1","description":"lsmod command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsmod"]},{"name":"lsof","argument":"--lsof","version":"1.0","description":"lsof command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsof"]},{"name":"mount","argument":"--mount","version":"1.1","description":"mount command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin"],"magic_commands":["mount"]},{"name":"netstat","argument":"--netstat","version":"1.2","description":"netstat command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["netstat"]},{"name":"ntpq","argument":"--ntpq","version":"1.0","description":"ntpq -p command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["ntpq"]},{"name":"passwd","argument":"--passwd","version":"1.0","description":"/etc/passwd file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]},{"name":"pip_list","argument":"--pip-list","version":"1.0","description":"pip list command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["pip list","pip3 list"]},{"name":"pip_show","argument":"--pip-show","version":"1.0","description":"pip show command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["pip show","pip3 show"]},{"name":"ps","argument":"--ps","version":"1.1","description":"ps command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["ps"]},{"name":"route","argument":"--route","version":"1.0","description":"route command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["route"]},{"name":"shadow","argument":"--shadow","version":"1.0","description":"/etc/shadow file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]},{"name":"ss","argument":"--ss","version":"1.0","description":"ss command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["ss"]},{"name":"stat","argument":"--stat","version":"1.0","description":"stat command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["stat"]},{"name":"systemctl","argument":"--systemctl","version":"1.0","description":"systemctl command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl"]},{"name":"systemctl_lj","argument":"--systemctl-lj","version":"1.0","description":"systemctl list-jobs command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-jobs"]},{"name":"systemctl_ls","argument":"--systemctl-ls","version":"1.0","description":"systemctl list-sockets command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-sockets"]},{"name":"systemctl_luf","argument":"--systemctl-luf","version":"1.0","description":"systemctl list-unit-files command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-unit-files"]},{"name":"timedatectl","argument":"--timedatectl","version":"1.0","description":"timedatectl status command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["timedatectl","timedatectl status"]},{"name":"uname","argument":"--uname","version":"1.1","description":"uname -a command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin"],"magic_commands":["uname"]},{"name":"uptime","argument":"--uptime","version":"1.0","description":"uptime command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["uptime"]},{"name":"w","argument":"--w","version":"1.0","description":"w command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["w"]},{"name":"who","argument":"--who","version":"1.0","description":"who command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["who"]},{"name":"xml","argument":"--xml","version":"1.0","description":"XML file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the xmltodict library at https://github.com/martinblech/xmltodict","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]},{"name":"yaml","argument":"--yaml","version":"1.0","description":"YAML file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]}]
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-c', '_["parsers"]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_c_parsers_dot(self):
        """
        Test jc -a | jello -c _.parsers
        """
        self.expected = '''[{"name":"airport","argument":"--airport","version":"1.0","description":"airport -I command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["darwin"],"magic_commands":["airport -I"]},{"name":"airport_s","argument":"--airport-s","version":"1.0","description":"airport -s command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["darwin"],"magic_commands":["airport -s"]},{"name":"arp","argument":"--arp","version":"1.2","description":"arp command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["arp"]},{"name":"blkid","argument":"--blkid","version":"1.0","description":"blkid command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["blkid"]},{"name":"crontab","argument":"--crontab","version":"1.1","description":"crontab command and file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["crontab"]},{"name":"crontab_u","argument":"--crontab-u","version":"1.0","description":"crontab file parser with user support","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]},{"name":"csv","argument":"--csv","version":"1.0","description":"CSV file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the python standard csv library","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]},{"name":"df","argument":"--df","version":"1.1","description":"df command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin"],"magic_commands":["df"]},{"name":"dig","argument":"--dig","version":"1.1","description":"dig command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["dig"]},{"name":"du","argument":"--du","version":"1.1","description":"du command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["du"]},{"name":"env","argument":"--env","version":"1.1","description":"env command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["env"]},{"name":"file","argument":"--file","version":"1.1","description":"file command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["file"]},{"name":"free","argument":"--free","version":"1.0","description":"free command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["free"]},{"name":"fstab","argument":"--fstab","version":"1.0","description":"fstab file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"]},{"name":"group","argument":"--group","version":"1.0","description":"/etc/group file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]},{"name":"gshadow","argument":"--gshadow","version":"1.0","description":"/etc/gshadow file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd"]},{"name":"history","argument":"--history","version":"1.2","description":"history command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Optimizations by https://github.com/philippeitis","compatible":["linux","darwin","cygwin","aix","freebsd"]},{"name":"hosts","argument":"--hosts","version":"1.0","description":"/etc/hosts file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]},{"name":"id","argument":"--id","version":"1.0","description":"id command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["id"]},{"name":"ifconfig","argument":"--ifconfig","version":"1.5","description":"ifconfig command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using ifconfig-parser package from https://github.com/KnightWhoSayNi/ifconfig-parser","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["ifconfig"]},{"name":"ini","argument":"--ini","version":"1.0","description":"INI file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using configparser from the standard library","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]},{"name":"iptables","argument":"--iptables","version":"1.1","description":"iptables command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["iptables"]},{"name":"jobs","argument":"--jobs","version":"1.0","description":"jobs command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["jobs"]},{"name":"last","argument":"--last","version":"1.0","description":"last and lastb command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["last","lastb"]},{"name":"ls","argument":"--ls","version":"1.3","description":"ls command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["ls"]},{"name":"lsblk","argument":"--lsblk","version":"1.3","description":"lsblk command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsblk"]},{"name":"lsmod","argument":"--lsmod","version":"1.1","description":"lsmod command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsmod"]},{"name":"lsof","argument":"--lsof","version":"1.0","description":"lsof command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsof"]},{"name":"mount","argument":"--mount","version":"1.1","description":"mount command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin"],"magic_commands":["mount"]},{"name":"netstat","argument":"--netstat","version":"1.2","description":"netstat command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["netstat"]},{"name":"ntpq","argument":"--ntpq","version":"1.0","description":"ntpq -p command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["ntpq"]},{"name":"passwd","argument":"--passwd","version":"1.0","description":"/etc/passwd file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]},{"name":"pip_list","argument":"--pip-list","version":"1.0","description":"pip list command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["pip list","pip3 list"]},{"name":"pip_show","argument":"--pip-show","version":"1.0","description":"pip show command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["pip show","pip3 show"]},{"name":"ps","argument":"--ps","version":"1.1","description":"ps command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["ps"]},{"name":"route","argument":"--route","version":"1.0","description":"route command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["route"]},{"name":"shadow","argument":"--shadow","version":"1.0","description":"/etc/shadow file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]},{"name":"ss","argument":"--ss","version":"1.0","description":"ss command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["ss"]},{"name":"stat","argument":"--stat","version":"1.0","description":"stat command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["stat"]},{"name":"systemctl","argument":"--systemctl","version":"1.0","description":"systemctl command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl"]},{"name":"systemctl_lj","argument":"--systemctl-lj","version":"1.0","description":"systemctl list-jobs command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-jobs"]},{"name":"systemctl_ls","argument":"--systemctl-ls","version":"1.0","description":"systemctl list-sockets command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-sockets"]},{"name":"systemctl_luf","argument":"--systemctl-luf","version":"1.0","description":"systemctl list-unit-files command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-unit-files"]},{"name":"timedatectl","argument":"--timedatectl","version":"1.0","description":"timedatectl status command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["timedatectl","timedatectl status"]},{"name":"uname","argument":"--uname","version":"1.1","description":"uname -a command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin"],"magic_commands":["uname"]},{"name":"uptime","argument":"--uptime","version":"1.0","description":"uptime command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["uptime"]},{"name":"w","argument":"--w","version":"1.0","description":"w command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["w"]},{"name":"who","argument":"--who","version":"1.0","description":"who command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["who"]},{"name":"xml","argument":"--xml","version":"1.0","description":"XML file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the xmltodict library at https://github.com/martinblech/xmltodict","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]},{"name":"yaml","argument":"--yaml","version":"1.0","description":"YAML file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]}]
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-c', '_.parsers']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_l_parsers(self):
        """
        Test jc -a | jello -l '_["parsers"]'
        """
        self.expected = '''\
{"name":"airport","argument":"--airport","version":"1.0","description":"airport -I command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["darwin"],"magic_commands":["airport -I"]}
{"name":"airport_s","argument":"--airport-s","version":"1.0","description":"airport -s command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["darwin"],"magic_commands":["airport -s"]}
{"name":"arp","argument":"--arp","version":"1.2","description":"arp command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["arp"]}
{"name":"blkid","argument":"--blkid","version":"1.0","description":"blkid command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["blkid"]}
{"name":"crontab","argument":"--crontab","version":"1.1","description":"crontab command and file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["crontab"]}
{"name":"crontab_u","argument":"--crontab-u","version":"1.0","description":"crontab file parser with user support","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]}
{"name":"csv","argument":"--csv","version":"1.0","description":"CSV file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the python standard csv library","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]}
{"name":"df","argument":"--df","version":"1.1","description":"df command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin"],"magic_commands":["df"]}
{"name":"dig","argument":"--dig","version":"1.1","description":"dig command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["dig"]}
{"name":"du","argument":"--du","version":"1.1","description":"du command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["du"]}
{"name":"env","argument":"--env","version":"1.1","description":"env command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["env"]}
{"name":"file","argument":"--file","version":"1.1","description":"file command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["file"]}
{"name":"free","argument":"--free","version":"1.0","description":"free command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["free"]}
{"name":"fstab","argument":"--fstab","version":"1.0","description":"fstab file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"]}
{"name":"group","argument":"--group","version":"1.0","description":"/etc/group file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]}
{"name":"gshadow","argument":"--gshadow","version":"1.0","description":"/etc/gshadow file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd"]}
{"name":"history","argument":"--history","version":"1.2","description":"history command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Optimizations by https://github.com/philippeitis","compatible":["linux","darwin","cygwin","aix","freebsd"]}
{"name":"hosts","argument":"--hosts","version":"1.0","description":"/etc/hosts file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]}
{"name":"id","argument":"--id","version":"1.0","description":"id command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["id"]}
{"name":"ifconfig","argument":"--ifconfig","version":"1.5","description":"ifconfig command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using ifconfig-parser package from https://github.com/KnightWhoSayNi/ifconfig-parser","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["ifconfig"]}
{"name":"ini","argument":"--ini","version":"1.0","description":"INI file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using configparser from the standard library","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]}
{"name":"iptables","argument":"--iptables","version":"1.1","description":"iptables command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["iptables"]}
{"name":"jobs","argument":"--jobs","version":"1.0","description":"jobs command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["jobs"]}
{"name":"last","argument":"--last","version":"1.0","description":"last and lastb command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["last","lastb"]}
{"name":"ls","argument":"--ls","version":"1.3","description":"ls command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["ls"]}
{"name":"lsblk","argument":"--lsblk","version":"1.3","description":"lsblk command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsblk"]}
{"name":"lsmod","argument":"--lsmod","version":"1.1","description":"lsmod command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsmod"]}
{"name":"lsof","argument":"--lsof","version":"1.0","description":"lsof command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsof"]}
{"name":"mount","argument":"--mount","version":"1.1","description":"mount command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin"],"magic_commands":["mount"]}
{"name":"netstat","argument":"--netstat","version":"1.2","description":"netstat command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["netstat"]}
{"name":"ntpq","argument":"--ntpq","version":"1.0","description":"ntpq -p command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["ntpq"]}
{"name":"passwd","argument":"--passwd","version":"1.0","description":"/etc/passwd file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]}
{"name":"pip_list","argument":"--pip-list","version":"1.0","description":"pip list command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["pip list","pip3 list"]}
{"name":"pip_show","argument":"--pip-show","version":"1.0","description":"pip show command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["pip show","pip3 show"]}
{"name":"ps","argument":"--ps","version":"1.1","description":"ps command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["ps"]}
{"name":"route","argument":"--route","version":"1.0","description":"route command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["route"]}
{"name":"shadow","argument":"--shadow","version":"1.0","description":"/etc/shadow file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]}
{"name":"ss","argument":"--ss","version":"1.0","description":"ss command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["ss"]}
{"name":"stat","argument":"--stat","version":"1.0","description":"stat command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["stat"]}
{"name":"systemctl","argument":"--systemctl","version":"1.0","description":"systemctl command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl"]}
{"name":"systemctl_lj","argument":"--systemctl-lj","version":"1.0","description":"systemctl list-jobs command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-jobs"]}
{"name":"systemctl_ls","argument":"--systemctl-ls","version":"1.0","description":"systemctl list-sockets command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-sockets"]}
{"name":"systemctl_luf","argument":"--systemctl-luf","version":"1.0","description":"systemctl list-unit-files command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-unit-files"]}
{"name":"timedatectl","argument":"--timedatectl","version":"1.0","description":"timedatectl status command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["timedatectl","timedatectl status"]}
{"name":"uname","argument":"--uname","version":"1.1","description":"uname -a command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin"],"magic_commands":["uname"]}
{"name":"uptime","argument":"--uptime","version":"1.0","description":"uptime command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["uptime"]}
{"name":"w","argument":"--w","version":"1.0","description":"w command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["w"]}
{"name":"who","argument":"--who","version":"1.0","description":"who command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["who"]}
{"name":"xml","argument":"--xml","version":"1.0","description":"XML file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the xmltodict library at https://github.com/martinblech/xmltodict","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]}
{"name":"yaml","argument":"--yaml","version":"1.0","description":"YAML file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]}
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-l', '_["parsers"]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_l_parsers_dot(self):
        """
        Test jc -a | jello -l _.parsers
        """
        self.expected = '''\
{"name":"airport","argument":"--airport","version":"1.0","description":"airport -I command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["darwin"],"magic_commands":["airport -I"]}
{"name":"airport_s","argument":"--airport-s","version":"1.0","description":"airport -s command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["darwin"],"magic_commands":["airport -s"]}
{"name":"arp","argument":"--arp","version":"1.2","description":"arp command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["arp"]}
{"name":"blkid","argument":"--blkid","version":"1.0","description":"blkid command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["blkid"]}
{"name":"crontab","argument":"--crontab","version":"1.1","description":"crontab command and file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["crontab"]}
{"name":"crontab_u","argument":"--crontab-u","version":"1.0","description":"crontab file parser with user support","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]}
{"name":"csv","argument":"--csv","version":"1.0","description":"CSV file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the python standard csv library","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]}
{"name":"df","argument":"--df","version":"1.1","description":"df command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin"],"magic_commands":["df"]}
{"name":"dig","argument":"--dig","version":"1.1","description":"dig command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["dig"]}
{"name":"du","argument":"--du","version":"1.1","description":"du command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["du"]}
{"name":"env","argument":"--env","version":"1.1","description":"env command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["env"]}
{"name":"file","argument":"--file","version":"1.1","description":"file command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["file"]}
{"name":"free","argument":"--free","version":"1.0","description":"free command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["free"]}
{"name":"fstab","argument":"--fstab","version":"1.0","description":"fstab file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"]}
{"name":"group","argument":"--group","version":"1.0","description":"/etc/group file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]}
{"name":"gshadow","argument":"--gshadow","version":"1.0","description":"/etc/gshadow file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","aix","freebsd"]}
{"name":"history","argument":"--history","version":"1.2","description":"history command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Optimizations by https://github.com/philippeitis","compatible":["linux","darwin","cygwin","aix","freebsd"]}
{"name":"hosts","argument":"--hosts","version":"1.0","description":"/etc/hosts file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]}
{"name":"id","argument":"--id","version":"1.0","description":"id command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["id"]}
{"name":"ifconfig","argument":"--ifconfig","version":"1.5","description":"ifconfig command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using ifconfig-parser package from https://github.com/KnightWhoSayNi/ifconfig-parser","compatible":["linux","aix","freebsd","darwin"],"magic_commands":["ifconfig"]}
{"name":"ini","argument":"--ini","version":"1.0","description":"INI file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using configparser from the standard library","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]}
{"name":"iptables","argument":"--iptables","version":"1.1","description":"iptables command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["iptables"]}
{"name":"jobs","argument":"--jobs","version":"1.0","description":"jobs command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["jobs"]}
{"name":"last","argument":"--last","version":"1.0","description":"last and lastb command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"],"magic_commands":["last","lastb"]}
{"name":"ls","argument":"--ls","version":"1.3","description":"ls command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["ls"]}
{"name":"lsblk","argument":"--lsblk","version":"1.3","description":"lsblk command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsblk"]}
{"name":"lsmod","argument":"--lsmod","version":"1.1","description":"lsmod command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsmod"]}
{"name":"lsof","argument":"--lsof","version":"1.0","description":"lsof command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["lsof"]}
{"name":"mount","argument":"--mount","version":"1.1","description":"mount command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin"],"magic_commands":["mount"]}
{"name":"netstat","argument":"--netstat","version":"1.2","description":"netstat command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["netstat"]}
{"name":"ntpq","argument":"--ntpq","version":"1.0","description":"ntpq -p command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["ntpq"]}
{"name":"passwd","argument":"--passwd","version":"1.0","description":"/etc/passwd file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]}
{"name":"pip_list","argument":"--pip-list","version":"1.0","description":"pip list command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["pip list","pip3 list"]}
{"name":"pip_show","argument":"--pip-show","version":"1.0","description":"pip show command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","win32","aix","freebsd"],"magic_commands":["pip show","pip3 show"]}
{"name":"ps","argument":"--ps","version":"1.1","description":"ps command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["ps"]}
{"name":"route","argument":"--route","version":"1.0","description":"route command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["route"]}
{"name":"shadow","argument":"--shadow","version":"1.0","description":"/etc/shadow file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","aix","freebsd"]}
{"name":"ss","argument":"--ss","version":"1.0","description":"ss command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["ss"]}
{"name":"stat","argument":"--stat","version":"1.0","description":"stat command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["stat"]}
{"name":"systemctl","argument":"--systemctl","version":"1.0","description":"systemctl command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl"]}
{"name":"systemctl_lj","argument":"--systemctl-lj","version":"1.0","description":"systemctl list-jobs command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-jobs"]}
{"name":"systemctl_ls","argument":"--systemctl-ls","version":"1.0","description":"systemctl list-sockets command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-sockets"]}
{"name":"systemctl_luf","argument":"--systemctl-luf","version":"1.0","description":"systemctl list-unit-files command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["systemctl list-unit-files"]}
{"name":"timedatectl","argument":"--timedatectl","version":"1.0","description":"timedatectl status command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux"],"magic_commands":["timedatectl","timedatectl status"]}
{"name":"uname","argument":"--uname","version":"1.1","description":"uname -a command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin"],"magic_commands":["uname"]}
{"name":"uptime","argument":"--uptime","version":"1.0","description":"uptime command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["uptime"]}
{"name":"w","argument":"--w","version":"1.0","description":"w command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["w"]}
{"name":"who","argument":"--who","version":"1.0","description":"who command parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","compatible":["linux","darwin","cygwin","aix","freebsd"],"magic_commands":["who"]}
{"name":"xml","argument":"--xml","version":"1.0","description":"XML file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the xmltodict library at https://github.com/martinblech/xmltodict","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]}
{"name":"yaml","argument":"--yaml","version":"1.0","description":"YAML file parser","author":"Kelly Brazil","author_email":"kellyjonbrazil@gmail.com","details":"Using the ruamel.yaml library at https://pypi.org/project/ruamel.yaml","compatible":["linux","darwin","cygwin","win32","aix","freebsd"]}
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-l', '_.parsers']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_parsers_18(self):
        """
        Test jc -a | jello '_["parsers"][18]'
        """
        self.expected = '''\
{
  "name": "id",
  "argument": "--id",
  "version": "1.0",
  "description": "id command parser",
  "author": "Kelly Brazil",
  "author_email": "kellyjonbrazil@gmail.com",
  "compatible": [
    "linux",
    "darwin",
    "aix",
    "freebsd"
  ],
  "magic_commands": [
    "id"
  ]
}
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '_["parsers"][18]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_parsers_18_dot(self):
        """
        Test jc -a | jello _.parsers[18]
        """
        self.expected = '''\
{
  "name": "id",
  "argument": "--id",
  "version": "1.0",
  "description": "id command parser",
  "author": "Kelly Brazil",
  "author_email": "kellyjonbrazil@gmail.com",
  "compatible": [
    "linux",
    "darwin",
    "aix",
    "freebsd"
  ],
  "magic_commands": [
    "id"
  ]
}
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '_.parsers[18]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_s_parsers_18_dot(self):
        """
        Test jc -a | jello -s _.parsers[18]
        """
        self.expected = '''\
.name = "id";
.argument = "--id";
.version = "1.0";
.description = "id command parser";
.author = "Kelly Brazil";
.author_email = "kellyjonbrazil@gmail.com";
.compatible[0] = "linux";
.compatible[1] = "darwin";
.compatible[2] = "aix";
.compatible[3] = "freebsd";
.magic_commands[0] = "id";
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-s', '_.parsers[18]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_parsers_18_name(self):
        """
        Test jc -a | jello '_["parsers"][18]["name"]'
        """
        self.expected = '"id"\n'

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '_["parsers"][18]["name"]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_parsers_18_name_dot(self):
        """
        Test jc -a | jello _.parsers[18].name
        """
        self.expected = '"id"\n'

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '_.parsers[18].name']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_l_parsers_18_name(self):
        """
        Test jc -a | jello -l '_["parsers"][18]["name"]'
        """
        self.expected = '"id"\n'

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-l', '_["parsers"][18]["name"]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_l_parsers_18_name_dot(self):
        """
        Test jc -a | jello -l _.parsers[18].name
        """
        self.expected = '"id"\n'

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-l', '_.parsers[18].name']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_r_parsers_18_name(self):
        """
        Test jc -a | jello -r '_["parsers"][18]["name"]'
        """
        self.expected = 'id\n'

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-r', '_["parsers"][18]["name"]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_r_parsers_18_name_dot(self):
        """
        Test jc -a | jello -r _.parsers[18].name
        """
        self.expected = 'id\n'

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-r', '_.parsers[18].name']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_parsers_18_compatible(self):
        """
        Test jc -a | jello '_["parsers"][18]["compatible"]'
        """
        self.expected = '''\
[
  "linux",
  "darwin",
  "aix",
  "freebsd"
]
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '_["parsers"][18]["compatible"]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_parsers_18_compatible_dot(self):
        """
        Test jc -a | jello _.parsers[18].compatible
        """
        self.expected = '''\
[
  "linux",
  "darwin",
  "aix",
  "freebsd"
]
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '_.parsers[18].compatible']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_s_parsers_18_compatible_dot(self):
        """
        Test jc -a | jello -s _.parsers[18].compatible
        """
        self.expected = '''\
.[0] = "linux";
.[1] = "darwin";
.[2] = "aix";
.[3] = "freebsd";
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-s', '_.parsers[18].compatible']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_c_parsers_18_compatible(self):
        """
        Test jc -a | jello -c '_["parsers"][18]["compatible"]'
        """
        self.expected = '["linux","darwin","aix","freebsd"]\n'

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-c', '_["parsers"][18]["compatible"]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_c_parsers_18_compatible_dot(self):
        """
        Test jc -a | jello -c _.parsers[18].compatible
        """
        self.expected = '["linux","darwin","aix","freebsd"]\n'

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-c', '_.parsers[18].compatible']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_l_parsers_18_compatible(self):
        """
        Test jc -a | jello -l '_["parsers"][18]["compatible"]'
        """
        self.expected = '''\
"linux"
"darwin"
"aix"
"freebsd"
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-l', '_["parsers"][18]["compatible"]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_l_parsers_18_compatible_dot(self):
        """
        Test jc -a | jello -l _.parsers[18].compatible
        """
        self.expected = '''\
"linux"
"darwin"
"aix"
"freebsd"
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-l', '_.parsers[18].compatible']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_lr_parsers_18_compatible(self):
        """
        Test jc -a | jello -lr '_["parsers"][18]["compatible"]'
        """
        self.expected = '''\
linux
darwin
aix
freebsd
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-lr', '_["parsers"][18]["compatible"]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_lr_parsers_18_compatible_dot(self):
        """
        Test jc -a | jello -lr _.parsers[18].compatible
        """
        self.expected = '''\
linux
darwin
aix
freebsd
'''
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-lr', '_.parsers[18].compatible']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_c_list_comprehension(self):
        """
        Test jc -a | jello -c '[entry["name"] for entry in _["parsers"] if "darwin" in entry["compatible"]]'
        """
        self.expected = '["airport","airport_s","arp","crontab","crontab_u","csv","df","dig","du","env","file","group","history","hosts","id","ifconfig","ini","jobs","last","ls","mount","passwd","pip_list","pip_show","ps","shadow","uname","uptime","w","who","xml","yaml"]\n'

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-c', '[entry["name"] for entry in _["parsers"] if "darwin" in entry["compatible"]]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_jc_a_c_list_comprehension_dot(self):
        """
        Test jc -a | jello -c '[entry.name for entry in _.parsers if "darwin" in entry.compatible]'
        """
        self.expected = '["airport","airport_s","arp","crontab","crontab_u","csv","df","dig","du","env","file","group","history","hosts","id","ifconfig","ini","jobs","last","ls","mount","passwd","pip_list","pip_show","ps","shadow","uname","uptime","w","who","xml","yaml"]\n'

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-c', '[entry.name for entry in _.parsers if "darwin" in entry.compatible]']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.jc_a_output)
        self.assertEqual(f.getvalue(), self.expected)

    def test_twitter_jlines_to_json(self):
        """
        Test cat twitterdata.jlines | jello
        """
        self.expected = self.twitterdata_output

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello']
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.twitterdata)
        self.assertEqual(f.getvalue(), self.expected)

    def test_twitter_lines_table(self):
        """
        Test cat twitterdata.jlines | jello -l '\
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
        """
        self.query = '''\
user_ids = set()
result = []
for tweet in _:
    user_ids.add(tweet["user"]["id"])
for user in sorted(user_ids):
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
result
'''
        self.expected = self.twitter_table_output

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-l', self.query]
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.twitterdata)
        self.assertEqual(f.getvalue(), self.expected)

    def test_twitter_lines_table_schema(self):
        """
        Test cat twitterdata.jlines | jello -s '\
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
        """
        self.query = '''\
user_ids = set()
result = []
for tweet in _:
    user_ids.add(tweet["user"]["id"])
for user in sorted(user_ids):
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
result
'''
        self.expected = self.twitter_table_output_schema

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-s', self.query]
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.twitterdata)
        self.assertEqual(f.getvalue(), self.expected)

    def test_twitter_lines_table_dot(self):
        """
        Test cat twitterdata.jlines | jello -l '\
                                      user_ids = set()
                                      result = []
                                      for tweet in _:
                                          user_ids.add(tweet.user.id)
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
                                          user_profile.tweet_ids = ";".join(tweet_ids)
                                          result.append(user_profile)
                                      result'
        """
        self.query = '''\
user_ids = set()
result = []
for tweet in _:
  user_ids.add(tweet.user.id)
for user in sorted(user_ids):
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
result
'''
        self.expected = self.twitter_table_output

        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            testargs = ['jello', '-l', self.query]
            with patch.object(sys, 'argv', testargs):
                _ = jello.cli.main(data=self.twitterdata)
        self.assertEqual(f.getvalue(), self.expected)


if __name__ == '__main__':
    unittest.main()
