import yaml
import subprocess

class setups_list:

    path = '/Users/sczajkow/Perforce/sczajkow-p-cim-ful-caas-1672842335095/firepower/ims/IMS_7_3_0/feature-test-lib/testbeds/bqtbat_2_0/'
    with open ('/Users/sczajkow/Perforce/sczajkow-p-cim-ful-caas-1672842335095/firepower/ims/IMS_7_3_0/feature-test-lib/tests/system/cim_orchestrator/bqt_bat/setups.yaml') as file:
        tb = yaml.safe_load(file)
        for testbeds in tb['setups'].keys():
            print(testbeds)
            testbed = tb['setups'][testbeds]['testbed'].split('/')
            if len(testbed) == 5:
                print(testbed[4])
            else:
                print(testbed)
            for names in range(0,6):
                try:
                    host = tb['setups'][testbeds]['devices'][names]['name']
                    print(host)
                except:
                    continue
            for names in range(0,6):
                try:
                    host_file = tb['setups'][testbeds]['devices'][names]['testbed'].split('/')
                    output = subprocess.run([f"find {path} -name {host_file[4]}"], stdout=subprocess.PIPE, shell=True)
                    file = output.stdout.decode().splitlines()
                    file = file[0].rstrip().replace('//', '/')
                    split_bed = testbed[4].split('_')
                    if 'dst' in split_bed:
                        continue
                    else:
                        with open (f'{file}') as host:
                            host_list = []
                            test = yaml.safe_load(host)
                            for device in test['devices'].keys():
                                try:
                                    mgt_ip = test['devices'][device]['connections']['management']['ip']
                                    count = 1
                                    while count != 7:

                                        host_list.append((test['devices'][device]['custom']['chassis_software']['applications'][count]['logical_device']['ipv4']['ip']))
                                        count = count + 1

                                except:
                                    continue
                            if host_list:
                                print(host_file[4], 'MGMT',mgt_ip, 'FTD',*host_list)
                            else:
                                print(host_file[4], mgt_ip)


                except:
                    continue

            print("************************")
