#!/bin/bash
export PYTHONPATH=/opt/stats/labstats

echo -e "Content-type: text/html\n\n"
echo '
<html>
<head>
<title>OCF Lab Stats</title>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
</head>
<body>
<font size=4>'

echo '<img src="/lab-usage-graph.svg"></img>'

echo -e "<pre>============================</pre>\n<pre>"
/opt/stats/labstats/labstats/stats/who.py
echo "</pre>"

echo -e "<pre>============================</pre>\n<pre>"
cat /opt/stats/top_users.txt
echo '</pre>'

echo -e "<pre>============================</pre>\n<pre>"
cat /opt/stats/toner
echo '</pre>'

echo '<pre>'
cat /opt/stats/mystoracle.txt
echo '</pre>'

echo -e "<pre>============================</pre>\n<pre>"
cat /opt/stats/utilization.txt
echo '</pre>'

echo '
</font>
</body>
</html>'

