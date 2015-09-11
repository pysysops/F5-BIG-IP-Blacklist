# F5-BIG-IP-Blacklist
This is a quick script I threw together to update IP block lists on a couple of F5 BIG-IP 1600's I used to play with (manage and maintain).

I used the awesome blocklist from the guys over at: [blocklist.de](http://www.blocklist.de/en/index.html) - THANKS GUYS!

```
usage: update_blocklist.py [-h] -a HOST -u USERNAME -p PASSWORD -g DEVICEGROUP
                           [-d PARTITION]

Update blocklist.de data group on F5 BIG-IP device.

optional arguments:
  -h, --help            show this help message and exit
  -a HOST, --host HOST  ip address of an F5 BIG-IP device
  -u USERNAME, --username USERNAME
                        user to authenticate with
  -p PASSWORD, --password PASSWORD
                        password to authenticate with
  -g DEVICEGROUP, --devicegroup DEVICEGROUP
                        device group of the HA pair
  -d PARTITION, --partition PARTITION
                        partition to add the data group to
```
