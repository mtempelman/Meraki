import meraki,sys,argparse,csv

# Defining your API key as a variable in source code is not recommended
API_KEY = '{enter API key here}'
# Instead, use an environment variable as shown under the Usage section
# @ https://github.com/meraki/dashboard-api-python/

dashboard = meraki.DashboardAPI(API_KEY)
# this script adds a VLAN to different networks with MX firewalls.
# the current script uses the 10.x.x.x RFC1918 range. The format used is 10.{location number}.{VLAN}.0/24
# in this case every location uses a /16 subnet split up into several /24 subnets
# 
# it uses a CSV file with the following columns
# id : Network ID
# ip : Location Number
# name : Network Name
# Example 
# id,ip,name
# L_1523672574,40,Amsterdam CS
#
# This script uses the Meraki API module and CSV module

# change the value below to the VLAN ID you want to add
vlan_id = '100'
with open ('networks.csv') as csv_file:
    csv_reader=csv.DictReader(csv_file,delimiter=',')
    line_count=0
    for row in csv_reader:
                try:
                    network_id=row['id']
                    subnet=row['ip']
                    location=row['name']
                    response = dashboard.appliance.createNetworkApplianceVlan(
                        network_id, vlan_id,
                        #change the name 
                        name='NEWVLAN',
                        subnet='10.'+str(subnet)+'.'+str(vlan_id)+'.0/24',
                        applianceIp='10.'+str(subnet)+'.'+str(vlan_id)+'.254',
                        groupPolicyId=None
                    )
                except meraki.APIError as e:
                    if "400 Bad Request" in str(e):
                        print('VLAN is already configured on network '+str(location))
csv_file.close()
