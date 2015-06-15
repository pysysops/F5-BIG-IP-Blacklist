#!env/bin/python

import socket
import urllib
import urllib2
import bigsuds

# Set some variables.

f5ip = '<<IP of F5 device>>'
f5user = '<<Username to access device>>'
f5pass = '<<password to F5 device>>'
device_group = '<< F5 device group>>'
partition = '<<Partition>>'

# Leave this unless you also change the iRule
data_group = "ext_blocklist"

address_list = [{'name':'/' partition + '/' + data_group, 'members':[]}]

# Get IPs from the blocklist
iplisturl = "http://lists.blocklist.de/lists/all.txt"
data = {'ipv6':'0', 'export_type':'text', 'submit':'Export'}
data = urllib.urlencode(data)
req = urllib2.Request(iplisturl, data)
response = urllib2.urlopen(req)

list = response.read()
blocklist = set(list.splitlines())

for ip in blocklist:
  # Hacky way to test if it's an IP
  try:
    socket.inet_aton(ip)
    address_list[0]['members'].append({'netmask':'255.255.255.255', 'address':ip})    
  except socket.error:
    pass

# Make sure that the list contains some stuff
if len(address_list[0]['members']) > 0:
  b = bigsuds.BIGIP(hostname = f5ip, username = f5user, password = f5pass)
  bigtrans = b.with_session_id()
  bigtrans.System.Session.set_transaction_timeout(99)
  try:
    with bigsuds.Transaction(bigtrans):
      bigtrans.Management.Partition.set_active_partition(partition)
      try:
        bigtrans.LocalLB.Class.modify_address_class(address_list)
      except bigsuds.OperationFailed:
        try: 
          bigtrans.LocalLB.Class.add_address_class(address_list)
        except bigsuds.OperationFailed:
          try:
            bigtrans.LocalLB.Class.delete_class(data_group)
            bigtrans.LocalLB.Class.add_address_class(address_list)
          except bigsuds.OperationFailed, e: 
            print e   
    bigtrans.System.ConfigSync.synchronize_to_group(device_group)
  except bigsuds.OperationFailed, e:
    print e
