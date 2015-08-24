import subprocess
import os

my_env = os.environ
my_env["PATH"] = "C:\\usr\\bin;" + my_env["PATH"]


def performSNMPWalk(ip, oid):
    
    command = "snmpwalk -v 1 -c public {0} {1}".format(ip, oid)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, env=my_env, shell=True)
    return proc.communicate()

def performSNMPGet(ip, oid):
    command = "snmpget -v 1 -c public {0} {1}".format(ip, oid)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, env=my_env, shell=True)
    return proc.communicate()

def performSNMPSet(ip, oid, val, oidType='i'):
    # oidType values:    
    #  TYPE: one of i, u, t, a, o, s, x, d, b
    #    i: INTEGER, u: unsigned INTEGER, t: TIMETICKS, a: IPADDRESS
    #    o: OBJID, s: STRING, x: HEX STRING, d: DECIMAL STRING, b: BITS
    #    U: unsigned int64, I: signed int64, F: float, D: double

    command = "snmpset -v 1 -c private {0} {1} {3} {2}".format(ip, oid,val, oidType)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, env=my_env, shell=True)
    return proc.communicate()

def performSNMPGetNext(ip, oid):
    command = "snmpgetnext -v 1 -c public {0} {1}".format(ip,oid)
    print(command)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE,  stderr=subprocess.PIPE, env=my_env, shell=True)
    return proc.communicate()
    
def parseGetInteger(SNMPResponse):
    integer = SNMPResponse.split("INTEGER: ")
    assert (len(integer) >= 2)
    return int(integer[1])

def parseGetHex(SNMPResponse):
    hex = SNMPResponse.split("Hex-STRING: ")
    assert (len(hex) >= 2)
    resp = hex[1].replace("\n","")
    resp = resp.strip()
    return resp

