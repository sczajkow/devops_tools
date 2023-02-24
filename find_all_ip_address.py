import os
import ipaddress
import re
import yaml

class find_all_address:
    subnet = 0
    addrr = []
    def __init__(self):
        print('starting program')
        self.addrr = addrr
        self.address = address
    def create_subnet_ip_list(self,subnet):
        self.address = dict()
        adr = list(ipaddress.ip_network(subnet).hosts())
        for ip in adr:  self.address[str(ip)] = self.address.get(str(ip), 0)
        return self.address

    def get_ips_from_yaml(self,offbox_cmd, offbox_dev_cmd, onbox_cmd):
#        global offbox_files, onbox_files, offbox_dev_files

        offboxc = offbox_cmd
        offbox_devc = offbox_dev_cmd
        onboxc = onbox_cmd
        offbox, offbox_files = [], []
        offbox_dev, offbox_dev_files = [],[]
        onbox, onbox_files = [], []
        offbox.append(os.listdir(f'{offboxc}'))
        offbox_dev.append(os.listdir(f'{offbox_devc}'))
        onbox.append(os.listdir(f'{onboxc}'))
        file_lst = [offbox, offbox_dev, onbox]
        r = re.compile('^(baseline).+|.+(baseline).+')
        for lst in file_lst:
            for dir in lst:
                if lst == offbox:
                    for files in dir:
                        if r.match(files):
                            offbox_files.append(files)
                elif lst == offbox_dev:
                    for files in dir:
                        if r.match(files):
                            offbox_dev_files.append(files)
                else:
                    for files in dir:
                        if r.match(files):
                            onbox_files.append(files)
        return offbox_files, offbox_dev_files, onbox_files

    def find_ip(self,cmd,files_lst):
        self.addrr = []
        tb = dict()
        for files in files_lst:
            with open (f'{cmd}{files}') as file:
                tb = yaml.safe_load(file)
                for device in tb['devices'].keys():
                    try:
                        addrr.append(tb['devices'][device]['connections']['management']['ip'])
                        count = 1
                        while count != 7:
                            self.addrr.append(tb['devices'][device]['custom']['chassis_software']['applications'][count]['logical_device']['ipv4']['ip'])
                            count = count + 1
                    except:
                        continue
        return self.addrr


find = find_all_address()
subnet_ip = find.create_subnet_ip_list('10.11.0.0/19')
path = '<removed by me>'
offbox_cmd = f'{path}<removed by me>'
offbox_dev_cmd = f'{path}removed by me>'
onbox_cmd = f'{path}<removed by me>'

#addrr = []
file_list = find.get_ips_from_yaml(offbox_cmd, offbox_dev_cmd, onbox_cmd)
addrr = find.find_ip(offbox_cmd, files_list[0]),find.find_ip(offbox_dev_cmd, files_list[1]),find.find_ip(onbox_cmd, files_list[2])
#addrr.append(find.find_ip(offbox_cmd, files_list[0]))
#addrr.append(find.find_ip(offbox_dev_cmd, files_list[1]))
#addrr.append(find.find_ip(onbox_cmd, files_list[2]))
print(addrr)


