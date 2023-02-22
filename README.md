# devops_tools
Data from all files have been removed for specific reasons. But the functionality still works. 

find_all_ip_adddress.py

This is a tool to run through all of the baseline files that we have and grab the IP address from them. IP address per file can range from 1 to 7 management IP addresses within a dictionary the structure of the yaml output. After all the IP addresses have been grabbed, I compare the list with a dictionary of all the IP addresses within the subnet used. From there you can print out all the unused addresses, or make a call to grab several unused addresses, and then have the script update the dictionary. You can also print all used IP addresses. 

find_all_vlans_switched.py
This script will run through all of the switches in the racks for my team and ssh into them and run the show inter brief command to grab all of the VLANs assigned with the interface they are assigned to. if a switch can not be connected to it is either because the switch is down or does not exist as not all racks have the same amount of switches. The switches that could not be connected will be printed out at the end of the run for further investigation. 

Functionality:
1) You can have all data printed out for all switches. 
2) You can search for a single VLAN
3) You can search for a range of VLANs
4) You can also grab the output of a single switch

testbed_list.py

This script will run through our setups.yaml file and grab the testbed name, each host in the testbed, along with each baseline file and the testbed file. After which it will use the find command to find each testbed file and grab all the IP addresses for the hosts used in that testbed. I will be updating this to grab the TVM information and all of the VLANs used per HA pair. 
