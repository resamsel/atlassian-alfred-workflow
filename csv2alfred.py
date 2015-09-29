#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv

ITEM_FORMAT = """
    <item>
        <title>{summary}</title>
        <subtitle>{key}</subtitle>
        <arg>{key}: {summary}</arg>
        <text type="copy">{key}: {summary}</text>
    </item>
"""

print "<items>"
with sys.stdin as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    first = True
    for row in reader:
        if first:
            first = False
        elif len(row) > 11:
            print ITEM_FORMAT.format(key=row[0], summary=row[11])
print "</items>"
