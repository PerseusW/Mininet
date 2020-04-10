from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from sys import argv
import time

class SingleSwitchTopo(Topo):
    def build(self, n=2, lossy=True):
        switch = self.addSwitch("s1")
        for h in range(n):
            host = self.addHost("h%s" % (h + 1), cpu=.3 / n)
            if lossy!=0:
                self.addLink(host, switch, bw=100, delay=0, loss=lossy, use_htb=True)
            else:
                self.addLink(host, switch, bw=100, delay=0, loss=0, use_htb=True)


def TMUDPTest(lossy=True):
    topo = SingleSwitchTopo(n=2, lossy=lossy)
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, autoStaticArp=True)
    net.start()
    h1, h2 = net.getNodeByName("h1", "h2")
    h1.cmd("xterm -hold -e ./server -d ./ -p 10000 -w 3&")
    time.sleep(1)
    h2.cmd("xterm -hold -e ./client -f alice.txt -h 10.0.0.1 -p 10000 -w 5")
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    TMUDPTest(lossy=(int(argv[1])))