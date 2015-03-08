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
cat /opt/stats/var/top_users
echo '</pre>'

echo -e "<pre>============================</pre>\n<pre>"
cat /opt/stats/var/top_users_alltime
echo '</pre>'

echo -e "<pre>============================</pre>\n<pre>"
cat /opt/stats/var/toner
echo '</pre>'

echo '<pre>'
cat /opt/stats/var/mystoracle
echo '</pre>'

echo -e "<pre>============================</pre>\n<pre>"
cat /opt/stats/var/utilization
echo '</pre>'

echo '<p><a href="/printing/oracle/">Historical Toner Levels</a> | <a href="/printing/historacle/">Historical Paper Counts</a></p>'

echo '
</font>
</body>
</html>'

