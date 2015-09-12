# F5-BIG-IP-Blacklist
This is a quick script I threw together to update IP block lists on a couple of F5 BIG-IP 1600's I used to play with (manage and maintain).

I used the awesome blocklist from the guys over at: [blocklist.de](http://www.blocklist.de/en/index.html) - THANKS GUYS!

## Requirements
You'll need to install the bigsuds python package:
```
sudo pip install bigsuds
```
You'll also need to add an irule that checks the client IP against the "ext_blocklist" data group, a very simple example:
```
when HTTP_REQUEST {
    if { [class match [IP::client_addr] equals "ext_blocklist" ] } {
        drop
    }
}

```
I recently updated the utility to accept command line arguments. This makes it easy to run against multiple devices and schedule a regular update task as a cron job.

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
The script itself is probably offensive to Python gurus but it does / did the job I had to get done at the time.
