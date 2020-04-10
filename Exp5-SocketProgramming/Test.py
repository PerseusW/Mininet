from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import time

class DirectLinkTopo(Topo):
    def build(self):
        h1 = self.addHost('h1', ip='10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.2')
        self.addLink(h1, h2, bw=100)

def perfTest():
    net = Mininet(topo=DirectLinkTopo(), link=TCLink)
    net.start()
    h1, h2 = net.getNodeByName("h1", "h2")
    net.iperf((h1, h2))
    h1.cmd("xterm -hold -e ./Bandwidth -s -p 10000&")
    time.sleep(1)
    h2.cmd("xterm -hold -e ./Bandwidth -c -h 10.0.0.1 -p 10000")
    net.stop()

if __name__ == "__main__":
    setLogLevel('info')
    perfTest()