from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink

def topology():
    net = Mininet()# (controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
    # Add hosts and switches
    h1 = net.addHost('h1', ip="10.0.1.10/24", mac="00:00:00:00:00:01", defaultRoute = "via 10.0.1.1")
    h2 = net.addHost('h2', ip="10.0.2.10/24", mac="00:00:00:00:00:02", defaultRoute = "via 10.0.2.1" )
    r1 = net.addHost('r1')
    s1 = net.addSwitch('s2')
    s2 = net.addSwitch('s3')
    c0 = net.addController('c0')

    net.addLink( r1, s1 )
    net.addLink( r1, s2 )
    net.addLink( h1, s1 )
    net.addLink( h2, s2 )
    net.build()
    net.start()
    #Linux kernel functions/Terminal commands
    r1.cmd("ifconfig r1-eth0 hw ether 00:00:00:00:01:01")
    r1.cmd("ifconfig r1-eth1 hw ether 00:00:00:00:01:02")
    r1.cmd("ip addr add 10.0.1.1/24 brd + dev r1-eth0")
    r1.cmd("ip addr add 10.0.2.1/24 brd + dev r1-eth1")
    r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
