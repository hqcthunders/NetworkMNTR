########################################################################
#


import time
from pysnmp.entity.rfc3413.oneliner import cmdgen
import MySQLdb
import nmap


db = MySQLdb.Connection("localhost", "network", "123456789", "networkmntr")
SNMP_PORT = 161
SNMP_COMMUNITY = 'abc'


def get_result(ip, oid):
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(SNMP_COMMUNITY),
        cmdgen.UdpTransportTarget((ip, SNMP_PORT)),
        *oid
    )
    result = [varBind.prettyPrint().split("= ")[1] for varBind in varBinds]
    return result


def calculate_bandwidth(idx, ip):
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData(SNMP_COMMUNITY),
    cmdgen.UdpTransportTarget((ip, SNMP_PORT)),
    ".1.3.6.1.2.1.2.2.1.10.{}".format(idx),
    ".1.3.6.1.2.1.2.2.1.16.{}".format(idx),
    ".1.3.6.1.2.1.2.2.1.5.{}".format(idx)
    )
    ifinOctets, ifoutOctets, ifspeed = list(map(int, [value.prettyPrint().split("= ")[1] for value in varBinds]))
    times = 1
    time.sleep(1)
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData(SNMP_COMMUNITY),
    cmdgen.UdpTransportTarget((ip, SNMP_PORT)),
    ".1.3.6.1.2.1.2.2.1.10.{}".format(idx),
    ".1.3.6.1.2.1.2.2.1.16.{}".format(idx),
    ".1.3.6.1.2.1.2.2.1.5.{}".format(idx)
    )
    ifinOctets2, ifoutOctets2, ifspeed2 = list(map(int, [value.prettyPrint().split("= ")[1] for value in varBinds]))
    inbound = ifinOctets2 - ifinOctets
    outbound = ifoutOctets2 - ifoutOctets
    return ((inbound/times) * 8)/1024, ((outbound/times) * 8)/1024


def find_list_ip(network, exclude):
    nm = nmap.PortScanner()
    arguments = "-T5 --exclude {},192.168.2.254,192.168.3.254".format(exclude)
    scanip = nm.scan(network, "161", arguments=arguments)["scan"]
    return [ip for ip in scanip]


def check_use_bandwidth(inbound, outbound):
    if inbound > 0.8984375 or outbound > 0.9921875:
        return True
    return False


def check_connected(idx, ip):
    oid = [".1.3.6.1.2.1.2.2.1.7.{}".format(idx)]
    result = get_result(ip, oid)
    return result


def save_information(ip):
    oid = [".1.3.6.1.2.1.1.5.0", ".1.3.6.1.2.1.1.1.0", ".1.3.6.1.2.1.2.1.0"]
    result = get_result(ip, oid)
    return result


def auto_find_connection():
    conn = db.cursor()
    conn.execute("""SELECT MaPB, network from phongban WHERE MaPB!=\"MNG\";""")
    list_network = conn.fetchall()
    conn.execute("""SELECT ipaddv4 from interfaces;""")
    list_ip = [ip[0] for ip in conn.fetchall()[1:]]
    exclude = ",".join(list_ip)
    for MaPB, network in list_network:
        ips = find_list_ip(network, exclude)
        for ip in ips:
            MaTB, TenTB, socong = save_information(ip)
            if "Linux" in TenTB:
                TenTB = "Linux "+ ip
            elif "Windows" in TenTB:
                TenTB = "Windows "+ip
            else:
                TenTB = TenTB.split(",")[0]
            sql = """INSERT INTO thietbi values (\"{}\", \"{}\", \"{}\", {}, {})""".format(MaTB, MaPB, TenTB,
                                                                                           socong, 1)
            conn.execute(sql)
            db.commit()
            idx = get_result(ip, [".1.3.6.1.2.1.4.20.1.2.{}".format(ip)])[0]
            oid = [".1.3.6.1.2.1.2.2.1.2.{}".format(idx), ".1.3.6.1.2.1.2.2.1.6.{}".format(idx)]
            tenif, mac = get_result(ip, oid)
            mac = mac[2:].upper()
            mac = '-'.join(mac[i:i+2] for i in range(0,12,2))
            sql = """INSERT INTO interfaces values (\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", null, null, \"{}\")""".format(mac, MaTB, tenif, idx, ip, "Up")
            conn.execute(sql)
            db.commit()


def auto_update_bandwidth():
    conn = db.cursor()
    conn.execute("""SELECT matb, idx, ipaddv4 FROM interfaces;""")
    list_idx_ip = conn.fetchall()
    rs = []
    for matb, idx, ip in list_idx_ip:
        chc = check_connected(idx, ip)
        try:
            rs.append(chc[0])
        except IndexError:
            sql = """UPDATE interfaces SET trangthai=\"Down\" WHERE ipaddv4=\"{}\";""".format(ip)
            conn.execute(sql)
            db.commit()
            rs = rs
            continue
        if chc == ['1']:
            inbound, outbound = calculate_bandwidth(idx, ip)
            sql = """UPDATE interfaces SET inbound={}, outbound={}, trangthai=\"Up\" WHERE ipaddv4=\"{}\";""".format(inbound, outbound, ip)
            conn.execute(sql)
            db.commit()

    if not rs:
        sql = """UPDATE thietbi SET trangthai=0 WHERE Matb=\"{}\"""".format(matb)
        conn.execute(sql)
        db.commit()
    else:
        sql = """UPDATE thietbi SET trangthai=1 WHERE Matb=\"{}\"""".format(matb)
        conn.execute(sql)
        db.commit()


def main():
    auto_find_connection()
    #auto_update_bandwidth()


if __name__ == "__main__":
    main()