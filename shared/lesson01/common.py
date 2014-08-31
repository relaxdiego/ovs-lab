#!/usr/bin/python

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.topo import Topo
from mininet.util import dumpNodeConnections


def createTopology(switch, hosts):
    setLogLevel('info')
    topo = Topo()
    switch = topo.addSwitch(switch)

    for (hostname, opts) in hosts:
        host = topo.addHost(hostname, **opts)
        topo.addLink(host, switch)

    network = Mininet(topo, controller=None)
    network.start()
    print "*** Dumping host connections"
    dumpNodeConnections(network.hosts)
    CLI(network)
    network.stop()
