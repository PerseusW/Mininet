#!/usr/bin/python
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
def main():
    net = Mininet( topo=None)
    # Create nodes
    h1 = net.addHost( 'h1')
    h2 = net.addHost( 'h2')
    h3 = net.addHost( 'h3')
    # Create switches
    s1 = net.addSwitch( 's1')
    s2 = net.addSwitch( 's2')
    s3 = net.addSwitch( 's3')
    # Add link
    net.addLink(h1, s1)
    net.addLink(h2, s2)
    net.addLink(h3, s3)   
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s3, s2)  
    # Add Controllers each listen to diff ports
    c0 = net.addController( 'c0', controller=RemoteController, port=6632)

    c1 = net.addController( 'c1', controller=RemoteController, port=6633)

    c2 = net.addController( 'c1', controller=RemoteController, port=6634)

    net.build()
    # Connect each switch to a different controller
    s1.start( [c0] )
    s2.start( [c1] )
    s3.start( [c2] )

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()