#!/usr/bin/env python

import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen

# http://forums.cacti.net/about2771.html
oidTonerRemaining = "1.3.6.1.2.1.43.11.1.1.9.1.1"
oidTonerMax       = "1.3.6.1.2.1.43.11.1.1.8.1.1"


errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
    cmdgen.CommunityData('my-agent', 'public', 0),
    cmdgen.UdpTransportTarget((sys.argv[1], 161)),
    oidTonerRemaining,
    oidTonerMax
    )

print "/".join([str(var[1]) for var in varBinds])
