import paramiko
import re
from colorama import Fore

username = "labuser"
password = "labuser"
output = ""
qrack = list(range(2,9))
rack_switches = list(range(1,4))
#qrack = list(range(2,4)) # testing range single host test variable
#rack_switches = list(range(1,2)) # testing range single host test variable
rows = ('q','r')


def get_vlan():
    for row in rows:
        for rack in qrack:
            for index in rack_switches:
                if (f'{row}{rack}' == 'r5') or (f'{row}{rack}' == 'r8'):
                    continue
                else:
                    host = f'ful01-130-{row}{rack}-tor-{index}.devit.ciscolabs.com'
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    try:
                        ssh.connect(host, username=username, password=password, timeout=10)
                    except:
                        if ssh.get_transport() is None:
                            failed_host.append(host)
                        continue
                    ssh_stdin, ssh_stdout, ssh_stderr=ssh.exec_command('show inter brief')
                    output = ssh_stdout.readlines()
                    ssh.close()
                    print(Fore.GREEN + host + Fore.RESET )
                    for lines in output:
                        if lines.startswith('Eth') and not lines.startswith('Ethernet'):
                            lines = lines.rstrip().split()
                            lines = lines[0:2]
                            eth = lines[0]
                            vlan = lines[1]
                            port_vlan[vlan] = port_vlan.get(vlan, eth)
                            switch_vlan[vlan] = switch_vlan.get(vlan, f'q{rack}-tor-{index}')
                            dup_vlan[vlan] = dup_vlan.get(vlan, 0) + 1

failed_host = []
port_vlan = dict()
switch_vlan = dict()
dup_vlan = dict()



def failed_hosts():
    print(Fore.RED + 'These hosts are either down or do no exist in the rack. Please check devit-rackman.cisco.com')
    if len(failed_host) == 0:
        print('No failed hosts')
    else:
        for fh in failed_host:
            print(fh)

def print_all_vlan():
    get_vlan()
    print("{:<10} {:<10} {:5}".format('Switch','Port','VLAN'))
    for key in zip(port_vlan, switch_vlan):
        key1 = key[0] #this sets key1 to the the keys in port_vlan dict
        key2 = key[0]
        ports = port_vlan[key1] #this ends up being the port
        host = switch_vlan[key2]
        print("{:<10} {:<10} {:5}".format(host,ports,key1))
    failed_hosts()


def find_single_vlan():
    get_vlan()
    print("{:<10} {:<10} {:5}".format('Switch','Port','VLAN'))
    host = None
    vlan = None
    port = None
    for v,p in port_vlan.items():
        if v == input_vlan:
            port = p
            vlan = v
    for v,h in switch_vlan.items():
        if v == input_vlan:
            host = h
    if vlan is None:
        print('This Vlan is Not Assigned, or in a down switch')
    else:
        print("{:<10} {:<10} {:5}".format(host,port,vlan))
    failed_hosts()

def find_range_vlan():
    host = None
    vlan = None
    port = None
    get_vlan()
    frv = input_vlan.split(',')
    r1 = int(frv[0])
    r2 = int(frv[1]) + 1
    vrange = list(range(r1,r2))
    for check in vrange:
        vr = str(check)
        for v,p in port_vlan.items():
            if v == vr:
                port = p
                vlan = v
        for v,h in switch_vlan.items():
            if v == vr:
                host = h
        if vlan is None:
            print('This Vlan is Not Assigned, or in a down switch')
        else:
            print("{:<10} {:<10} {:5}".format(host,port,vlan))
    failed_hosts()

print(Fore.RED + "For a single VLAN Just enter the VLAN number")
print("For a range of VLANs enter VLAN,VLAN" + Fore.RESET)
input_vlan = input('Enter Vlan or range of VLANs to Check for: ')
input_vlan = input_vlan.lower()
pattern = re.compile(r"(\d+),(\d+)")
if input_vlan == 'all':
#this will print out all vlans on the swtichs if 'all' is entered
   print_all_vlan()
elif input_vlan != 'all':
    if input_vlan.isdigit():
        find_single_vlan()
    elif pattern.match(input_vlan):
        find_range_vlan()
    else:
        print('Enter Valid data, For all vlans: all, for a single vlan: 534, for a range of vlans: 2153,2156')
