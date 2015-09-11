#/usr/bin/env python

import sys, socket, urllib, urllib2, argparse, bigsuds

def main():

    parser = argparse.ArgumentParser(description='Update blocklist.de data group on F5 BIG-IP device.')
    parser.add_argument('-a', '--host', type=str, help='ip address of an F5 BIG-IP device', required=True)
    parser.add_argument('-u', '--username', type=str, help='user to authenticate with', required=True)
    parser.add_argument('-p', '--password', type=str, help='password to authenticate with', required=True)
    parser.add_argument('-g', '--devicegroup', type=str, help='device group of the HA pair', required=True)
    parser.add_argument('-d', '--partition', type=str, help='partition to add the data group to', default='Common')
    args = parser.parse_args()

    # Leave this unless you also change the iRule
    data_group = "ext_blocklist"

    # Create an empty data group to add IPs to block to
    address_list = [{'name':'/' + args.partition + '/' + data_group, 'members':[]}]

    # Get IPs from the blocklist
    iplisturl = "http://lists.blocklist.de/lists/all.txt"
    data = urllib.urlencode({'ipv6':'0', 'export_type':'text', 'submit':'Export'})
    req = urllib2.Request(iplisturl, data)
    response = urllib2.urlopen(req)

    blocklist = set(response.read().splitlines())

    for ip in blocklist:
        # Hacky way to test if it's a valid IP
        try:
            socket.inet_aton(ip)
            address_list[0]['members'].append({'netmask':'255.255.255.255', 'address':ip})
        except socket.error:
            pass

    # Make sure that the list contains some stuff
    if len(address_list[0]['members']) > 0:

        b = bigsuds.BIGIP(hostname = args.host, username = args.username, password = args.password)
        bigtrans = b.with_session_id()
        bigtrans.System.Session.set_transaction_timeout(10)

        try:
            with bigsuds.Transaction(bigtrans):
                bigtrans.Management.Partition.set_active_partition(args.partition)

                # So many try's
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
                            return 1

                # Make sure the updated config is synced between devices
                bigtrans.System.ConfigSync.synchronize_to_group(args.devicegroup)
                return 0

        except bigsuds.OperationFailed, e:
            print e
            return 1

if __name__ == "__main__":
    sys.exit(main())
