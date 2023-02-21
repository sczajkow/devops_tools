import paramiko #needs to be install
import re #default python packaage
from colorama import Fore #needs to be install
from collections import defaultdict #default python packaage

username = "labuser"
password = "labuser"
output = ""
#qrack = list(range(2,9))
#rack_switches = list(range(1,4))
qrack = list(range(2,4)) # testing range single host test variable
rack_switches = list(range(1,2)) # testing range single host test variable
rows = ('q','r')

def create_ssh():
    global output
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=username, password=password, timeout=10)
    except:
        if ssh.get_transport() is None:
            failed_host.append(host)
    ssh_stdin, ssh_stdout, ssh_stderr=ssh.exec_command('show inter brief')
    output = ssh_stdout.readlines()
    ssh.close()
    
def get_all_vlans():
    global host
    global output
    for row in rows:
        for rack in qrack:
            for index in rack_switches:
                if (f'{row}{rack}' == 'r5') or (f'{row}{rack}' == 'r8'):
                    continue
                else:
                    host = f'ful01-130-{row}{rack}-tor-{index}.devit.ciscolabs.com'
                    print(Fore.GREEN + host + Fore.RESET )
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
                    sort_vlans()

def sort_vlans():
    for lines in output:
        if lines.startswith('Eth') and not lines.startswith('Ethernet'):
            lines = lines.rstrip().split()
            lines = lines[0:2]
            eth = lines[0]
            vlan = lines[1]
            port_vlan[host].append((vlan,eth))
            
failed_host = []
port_vlan = defaultdict(list)


def failed_hosts():
    print(Fore.RED + 'These hosts are either down or do no exist in the rack. Please check devit-rackman.cisco.com')
    if len(failed_host) == 0:
        print('No failed hosts')
    else:
        for fh in failed_host:
            print(fh)

def print_all_vlan():
    get_all_vlans()
    for key,val in port_vlan.items():
        lst = val
        print(Fore.BLUE + key + Fore.RESET)
        print("{:<10} {:5}".format('Port','VLAN'))
        for k,v in lst:
            print("{:<10} {:<5}".format(v,k))
    failed_hosts()

def find_single_vlan():
    get_all_vlans()
    vlan = None
    print("{:<40} {:<10} {:5}".format('Switch','Port','VLAN'))
    for key,val in port_vlan.items():
        lst = val
        for k,v in lst:
            if k == input_vlan:
               vlan = k
               host = key
               port = v
               print("{:<40} {:<10} {:<5}".format(host,port,vlan))
    if vlan == None:
        print(f'Vlan {input_vlan} is Not Assigned, or in a down switch')
    failed_hosts()

def find_range_vlan():
    vlan = None
    get_all_vlans()
    print("{:<40} {:<10} {:5}".format('Switch','Port','VLAN'))
    frv = re.split(',|\s|-|\D+', input_vlan)
    frv = list(frv)
    r1 = int(frv[0])
    r2 = int(frv[1]) + 1
    vrange = list(range(r1,r2))
    for check in vrange:
        vr = str(check)
        for key,val in port_vlan.items():
            lst = val
            for k,v in lst:
                if k == vr:
                    port = v
                    vlan = k
                    host = key
                    print("{:<40} {:<10} {:5}".format(host,port,vlan))
    if vlan is None:
        print(f'Vlan {input_vlan} are Not Assigned, or in a down switch')
    failed_hosts()

def single_switch():
    global host
    host = host_input
    print(Fore.GREEN + host + Fore.RESET )
    create_ssh()
    sort_vlans()
    for key,val in port_vlan.items():
        lst = val
        print(Fore.BLUE + key + Fore.RESET)
        print("{:<10} {:5}".format('Port','VLAN'))
        for k,v in lst:
            print("{:<10} {:<5}".format(v,k))
    failed_hosts()


print(Fore.RED + "For a single VLAN Just enter the VLAN number")
print("To Check a single switch enter single and follow prompt")
print("For a range of VLANs enter VLAN,VLAN" + Fore.RESET)
input_vlan = input('Enter Vlan or range of VLANs to Check for: ')
input_vlan = input_vlan.lower().strip()
pattern = re.compile(r"(\d+)(,|\s|-|\D+)(\d+)")
if input_vlan == 'all':
#this will print out all vlans on the swtichs if 'all' is entered
   print_all_vlan()
elif input_vlan == 'single':
    host_input = input('Enter Hostname or IP address: ')
    host_input = host_input.lower().strip()
    single_switch()
elif input_vlan != 'all' or input_vlan != 'single':
    if input_vlan.isdigit():
        find_single_vlan()
    elif pattern.match(input_vlan):
        find_range_vlan()
    else:
        print('Enter Valid data, For all vlans: all, for a single vlan: 534, for a range of vlans: 2153,2156')
