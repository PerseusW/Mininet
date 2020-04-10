# from mininet. import 
from mininet.topo import Topo
# You may want to define a custom switch here
# class switch():

linkopts = dict(bw=1000,delay='10ms',loss=1)
hosts = []
switchs = []

class MaxLeafTopo(Topo):
    def __init__(self,**argv):
        Topo.__init__(self,**argv)
        for i in range(16):
            host = self.addHost('h' + str(i + 1))
            hosts.append(host)
        for i in range(7):
            switch = self.addSwitch('s' + str(i + 1))
            switchs.append(switch)
        for i in range(16):
            self.addLink(hosts[i],switchs[i/3],**linkopts)
        for i in range(3):
            self.addLink(switchs[i],switchs[6],**linkopts)
        for i in range(3,5):
            self.addLink(switchs[i],switchs[5],**linkopts)
        self.addLink(switchs[5],switchs[6],**linkopts)
            
class LoopTopo(Topo):
    def __init__(self,**argv):
        Topo.__init__(self,**argv)
        for i in range(16):
            host = self.addHost('h' + str(i + 1))
            hosts.append(host)
            switch = self.addSwitch('s' + str(i + 1))
            switchs.append(switch)
            self.addLink(host,switch,**linkopts)
        for i in range(15):
            self.addLink(switchs[i],switchs[i+1],**linkopts)
        self.addLink(switchs[0],switchs[15],**linkopts)
        for i in range(4):
            self.addLink(switchs[i],switchs[i+4],**linkopts)
        for i in range(8,12):
            self.addLink(switchs[i],switchs[i+4],**linkopts)
        
class SquareTopo(Topo):
    def __init__(self,**argv):
        Topo.__init__(self,**argv)
        for i in range(16):
            host = self.addHost('h' + str(i + 1))
            hosts.append(host)
        for i in range(8):
            switch = self.addSwitch('s' + str(i + 1))
            switchs.append(switch)
        for i in range(12):
            self.addLink(hosts[i],switchs[i/3],**linkopts)
        for i in range(4):
            self.addLink(switchs[i],switchs[i+4],**linkopts)
        self.addLink(switchs[4],switchs[5],**linkopts)
        self.addLink(switchs[5],switchs[6],**linkopts)
        self.addLink(switchs[6],switchs[7],**linkopts)
        self.addLink(switchs[7],switchs[4],**linkopts)
        for i in range(12,16):
            self.addLink(hosts[i],switchs[i-8],**linkopts)
        
                
class FatTreeTopo(Topo):
    def __init__(self,**argv):
        Topo.__init__(self,**argv)
        for i in range(16):
            host = self.addHost('h' + str(i + 1))
            hosts.append(host)
        for i in range(20):
            switch = self.addSwitch('s' + str(i + 1))
            switchs.append(switch)
        for i in range(16):
            self.addLink(hosts[i],switchs[i/2],**linkopts)
        for i in range(8):
            if i%2 == 0:
                self.addLink(switchs[i],switchs[i + 8],**linkopts)
                self.addLink(switchs[i],switchs[i + 9],**linkopts)
            else:
                self.addLink(switchs[i],switchs[i + 7],**linkopts)
                self.addLink(switchs[i],switchs[i + 8],**linkopts)
        for i in range(8,16):
            if i%2 == 0:
                self.addLink(switchs[i],switchs[16],**linkopts)
                self.addLink(switchs[i],switchs[17],**linkopts)
            else:
                self.addLink(switchs[i],switchs[18],**linkopts)
                self.addLink(switchs[i],switchs[19],**linkopts)
        
        
        
class BinaryTreeTopo(Topo):
    def __init__(self,**argv):
        Topo.__init__(self,**argv)
        for i in range(16):
            host = self.addHost('h' + str(i + 1))
            hosts.append(host)
        for i in range(13):
            switch = self.addSwitch('s' + str(i + 1))
            switchs.append(switch)
        for i in range(16):
            self.addLink(hosts[i],switchs[i/2],**linkopts)
        count = 0
        for i in range(8,12):
            self.addLink(switchs[i],switchs[count],**linkopts)
            count += 1
            self.addLink(switchs[i],switchs[count],**linkopts)
            count += 1
        for i in range(8,12):
            self.addLink(switchs[12],switchs[i],**linkopts)
        
class LinearTopo(Topo):
    def __init__(self,**argv):
        Topo.__init__(self,**argv)
        for i in range(16):
            host = self.addHost('h' + str(i + 1))
            hosts.append(host)
        for i in range(16):
            switch = self.addSwitch('s' + str(i + 1))
            switchs.append(switch)
            self.addLink(hosts[i],switch,**linkopts)
        for i in range(15):
            self.addLink(switchs[i],switchs[i+1],**linkopts)


topos = { 'LoopTopo': ( lambda: LoopTopo() )
        , 'SquareTopo': ( lambda: SquareTopo() )
        , 'FatTreeTopo': ( lambda: FatTreeTopo() )
        , 'MaxLeafTopo': ( lambda: MaxLeafTopo() )
        , 'BinaryTreeTopo': ( lambda: BinaryTreeTopo() )
        , 'LinearTopo': ( lambda: LinearTopo() ) }
