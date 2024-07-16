from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException, AuthenticationException, SSHException
import datetime

def createConnection(host: str,username: str,password: str):
    device = {
        "device_type":"huawei",
        "host":host,
        "username":username,
        "password":password
    }
    try:
        connection = ConnectHandler(**device) 
    except (AuthenticationException):
        logItDown(f'Authentication Failure (Device IP is: {host})')
        return False
    except (NetMikoTimeoutException):
        logItDown(f'Timeout Failure (Device IP is: {host})')
        return False
    except (SSHException):
        logItDown(f'SSH Failure (Device IP is: {host})')
        return False
    else:
        return connection

def getMacLocation(net_connection: ConnectHandler, mac: str):
    output = net_connection.send_config_set([f"dis mac-add | inc {mac}"]).splitlines()
    output_line = [line for line in output[3:] if mac in line and "XGE" not in line]
    net_connection.disconnect()
    if output_line:
        return {"host_name":output[-1], "line": output_line}
    
def addVlan(net_connection: ConnectHandler, vlanID: int, vlan_desc: str, username: str):
    output = net_connection.send_config_set([f"vlan {vlanID}",f"name {vlan_desc}"])
    logItDown(f"Config set by ({username}) -> {output}")
    net_connection.disconnect()
    return output

def changeIntVlan(net_connection: ConnectHandler,interfaceID: int,vlanID: int, username: str):
    port_type = net_connection.send_command(f"dis int g 0/0/{interfaceID} | inc Link-type")
    if "access" in port_type:
        output = net_connection.send_config_set([f"int g 0/0/{interfaceID}","dis this", "port link-type access",f"port def vlan {vlanID}"])
        logItDown(f"Config set by ({username}) -> {output}")
    else:
        output = "Not allowed this interface is a trunk port might be an AccessPoint or a Server"
    net_connection.disconnect()
    return {"output":output,"port_type":port_type}

def changeIntDesc(net_connection: ConnectHandler,interfaceID: int,int_desc: int, username: str):
    output = net_connection.send_config_set([f"int g 0/0/{interfaceID}","dis this", f"description  {int_desc}"])
    logItDown(f"Config set by ({username}) -> {output}")
    net_connection.disconnect()
    return output

def logItDown(log:str):
    try:
        file = open("log.txt","a")
        file.write(f"{datetime.datetime.now()} {log} \n {'-'*30} \n")
    except Exception as e:
        print(f'File Writing Error (LOG: {log}) \n')
    finally:
        file.close()

         
    

