from pysnmp.entity.rfc3413.oneliner import cmdgen
import json
import time

def write_file(value, filename, mode):
    file = open(filename, mode)
    file.write(value+"\n")
    file.close()
    print(value)

def get_name(community_name, ip, port, interface_uid):
    cmdGen = cmdgen.CommandGenerator()
    name = ''

    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.getCmd(
        cmdgen.CommunityData(community_name),
        cmdgen.UdpTransportTarget((ip, port)),
        interface_uid
    )

    if errorIndication or errorStatus:
        print(errorIndication)
    else:
        for val in varBindTable:
            val = str(val)[str(val).index('=') + 2:]
            if str(val).startswith('0x'):
                val = str(val)[str(val).index('x') + 1:]
                val = str(bytes.fromhex(val).decode('utf-8'))
            name = val
    return (name)

def get_network_traffic(filename, direction):
    octets = []
    cmdGen = cmdgen.CommandGenerator()

    with open(filename) as json_data:
        file = json.load(json_data)

    for host in file['hosts']:
        errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.getCmd(
            cmdgen.CommunityData(host['community_name']),
            cmdgen.UdpTransportTarget((host['ip_addr'], host['port'])),
            host['int_'+direction+'_traffic_oui']
        )

        time.sleep(2)

        errorIndication, errorStatus, errorIndex, varBindTable_1 = cmdGen.getCmd(
            cmdgen.CommunityData(host['community_name']),
            cmdgen.UdpTransportTarget((host['ip_addr'], host['port'])),
            host['int_'+direction+'_traffic_oui']
        )

        if errorIndication or errorStatus:
            print(errorIndication)
        else:
            for val in varBindTable:
                val = str(val)[str(val).index('=') + 1:]
                octets.append(int(val))
            for val_1 in varBindTable_1:
                val_1 = str(val_1)[str(val_1).index('=') + 1:]
                octets.append(int(val_1))
        kbps = ((octets[1] - octets[0])) * 8 / 120000
        hostnames = get_name(host['community_name'], host['ip_addr'], host['port'], host['hostname_oui'])
        intnames = get_name(host['community_name'], host['ip_addr'], host['port'], host['int_names_oui'])
        ifpct = kbps/(int(get_name(host['community_name'], host['ip_addr'], host['port'], host['ifspeed_oui']))/1000)
        write_file(str(hostnames)+','+str(intnames)+','+str(kbps)+','+str(direction)+','+str(ifpct*100),'network_traffic.csv', 'a')
        octets = []
    return ()
