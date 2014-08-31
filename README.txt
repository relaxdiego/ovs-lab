Open vSwitch Lab
================

This is a companion project to the Open vSwitch series of articles at
http://www.relaxdiego.com.


Requirements
------------

1. VirtualBox. Install from https://www.virtualbox.org/wiki/Downloads

2. Vagrant v1.6.3 or above. Install from http://www.vagrantup.com/downloads.html

3. The vagrant-vbguest plugin. Install with `vagrant plugin install vagrant-vbguest`


Installation
------------

Estimated time for the following steps including automated provisioning:
30 minutes. Time will vary depending on your connection speed.

1. Clone this repo and cd to it

2. Run `vagrant up`


Whoa! What Just Happened???
---------------------------

You just created two servers that can talk to each other over the "Internet!"

+-----------+                                                    +-----------+
|           |192.168.1.10/24    +------------+    192.168.2.20/24|           |
|  server1  |-------------------| "INTERNET" |-------------------|  server2  |
|           |                   +------------+                   |           |
+-----------+                                                    +-----------+

The two servers are Ubuntu VMs with mininet and OVS 2.x installed while the
"Internet" is really a VM with IP forwarding enabled. All networks above are
implemented as VirtualBox internal networks which are not directly accessible
from anywhere else including your local machine. However, you can SSH to any
of the three VMs using `vagrant ssh`. For example: `vagrant ssh internet`, or
`vagrant ssh server1` and then get to the internal networks from there.


Stopping and starting the VMs
-----------------------------

To suspend your VMs, run `vagrant suspend`. To shut them down, run
`vagrant halt`.


Viewing VM status
-----------------

`vagrant status`


Troubleshooting
---------------

PROBLEM: I'm getting an error about Vagrant not able to compile nokogiri

SOLUTION: You're missing developer tools needed to locally compile binaries
needed by nokogiri. In OS X, install the OS X Developer Tools for your OS X
version.
