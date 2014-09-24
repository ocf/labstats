#!/usr/bin/env python

import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen

# Do NOT ask me why this is off from the amount displayed on the printer's own web page.
oidPagesPrinted = "1.3.6.1.2.1.43.10.2.1.4.1.1"

errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(
    cmdgen.CommunityData('my-agent', 'public', 0),
    cmdgen.UdpTransportTarget((sys.argv[1], 161)),
    oidPagesPrinted
    )

print "/".join([str(var[1]) for var in varBinds])
