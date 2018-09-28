from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()
name = ''

errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.getCmd(
    cmdgen.CommunityData('public'),
    cmdgen.UdpTransportTarget(('localhost', 161)),
    '1.3.6.1.2.1.2.2.1.2.9'
)

if errorIndication or errorStatus:
    print(errorIndication)
else:
    for val in varBindTable:
        val = str(val)[str(val).index('=')+2:]
        if len(val) > 40:
            val = str(val)[str(val).index('x')+1:]
            val = str(bytes.fromhex(val).decode('utf-8'))
        name = val
print(name)
