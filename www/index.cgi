#!/bin/bash
echo -e "Content-type: text/html\n\n"
echo '
<html>
<head>
<title>OCF Lab Stats</title>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
</head>
<body>
<font size=4>'

epoch_30d=$(($(date +%s) - 60*60*24*30))
epoch_90d=$(($(date +%s) - 60*60*24*90))
epoch_365d=$(($(date +%s) - 60*60*24*365))

echo '<p><a href="/printing/oracle/">Historical Toner Levels</a> ('
echo "<a href='/printing/oracle/?since=${epoch_30d}'>[30d]</a> "
echo "<a href='/printing/oracle/?since=${epoch_90d}'>[90d]</a> "
echo "<a href='/printing/oracle/?since=${epoch_365d}'>[365d]</a> "
echo ') | <a href="/printing/historacle/">Historical Paper Counts</a></p>'

echo '
</font>
</body>
</html>'
