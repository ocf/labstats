#!/usr/bin/env python3
from ocflib.lab.hours import Day

html_class = '' if Day.from_date().is_open() else 'night'

print("""Content-Type: text/html

<!doctype html>
<html class=\"""" + html_class + """\">
    <head>
        <meta http-equiv="refresh" content="30" />
        <style>
            .night { background-color: black; }
            .night * { display: none; }
            img { width: 100%; height: 100vh; }
        </style>
    </head>
    <body>
        <img src="/lab-usage-graph.png" />
    </body>
</html>
""")
