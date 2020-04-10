from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import Switch

import os
import time

class Router(Switch):
    def __init__(self, name, **kwargs):
        kwargs['inNamespace'] = True
        Switch.__init__(self, name, **kwargs)

    @staticmethod
    def setup():
        return

    def start(self, controller):
        return

    def stop(self):
        self.deleteIntfs()

def main():
    net = Mininet(switch=Router)

    r1 = net.addSwitch('r1')
    r2 = net.addSwitch('r2')
    r3 = net.addSwitch('r3')
    r4 = net.addSwitch('r4')
    r5 = net.addSwitch('r5')

    h1 = net.addHost('h1',ip='10.1.0.2/21',defaultRoute="via 10.1.0.1")
    h2 = net.addHost('h2',ip='10.2.0.2/21',defaultRoute="via 10.2.0.1")
    h3 = net.addHost('h3',ip='10.3.0.2/21',defaultRoute="via 10.3.0.1")
    h4 = net.addHost('h4',ip='20.1.0.2/21',defaultRoute="via 20.1.0.1")
    h5 = net.addHost('h5',ip='30.1.0.2/21',defaultRoute="via 30.1.0.1")

    net.addLink(r1,r2)
    net.addLink(r2,r3)
    net.addLink(r3,r1)

    net.addLink(r1,h1)
    net.addLink(r2,h2)
    net.addLink(r3,h3)

    net.addLink(r1,r4)
    net.addLink(r1,r5)
    net.addLink(r4,r5)
    net.addLink(r4,h4)
    net.addLink(r5,h5)

    r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r4.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
    r5.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    r1.cmd("zebra -f r1_IP.conf -d -i /tmp/r1_IP.pid")
    r1.cmd("ospfd -f r1_OSPF.conf -d -i /tmp/r1_OSPF.pid")
    r1.cmd("bgpd -f r1_BGP.conf -d -i /tmp/r1_BGP.pid")

    r2.cmd("zebra -f r2_IP.conf -d -i /tmp/r2_IP.pid")
    r2.cmd("ospfd -f r2_OSPF.conf -d -i /tmp/r2_OSPF.pid")

    r3.cmd("zebra -f r3_IP.conf -d -i /tmp/r3_IP.pid")
    r3.cmd("ospfd -f r3_OSPF.conf -d -i /tmp/r3_OSPF.pid")

    r4.cmd("zebra -f r4_IP.conf -d -i /tmp/r4_IP.pid")
    r4.cmd("bgpd -f r4_BGP.conf -d -i /tmp/r4_BGP.pid")

    r5.cmd("zebra -f r5_IP.conf -d -i /tmp/r5_IP.pid")
    r5.cmd("bgpd -f r5_BGP.conf -d -i /tmp/r5_BGP.pid")

    net.build()
    net.start()
    print("Waiting 60 seconds for network to establish.")
    time.sleep(60)
    CLI(net)
    net.stop()
    os.system("rm -f /tmp/z*.pid /tmp/b*.pid /tmp/o*.pid /tmp/r*.pid")
    os.system("mn -c ")
    os.system("killall -9 zebra bgpd ospfd")

if __name__ == "__main__":
    main()

