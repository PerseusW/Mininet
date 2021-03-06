# Experiment 7: TMUDP

I have already implemented reliable transfer using UDP. The compile script and run script are integrated in `makefile`.

Compile via:

```shell
sudo make
```

Run via:

```shell
sudo make run
```

## Details

I will split my project into 4 modules to explain:

1. Test script
2. Base class `Host`
3. Sender end `Client`
4. Receiver end `Server`

### Test Script

The original script looks like this:

```makefile
run:
	sudo python test.py 0
	diff alice.txt test
	rm -rf test
	sleep 1
	sudo python test.py 1
	diff alice.txt test
	rm -rf test
	sleep 1
	sudo python test.py 5
	diff alice.txt test
```

First, I invoke a python script to test things.(I will come back to this later)

Second, I use the `diff` command to check if the output file is the same as the original one.

Third, I remove the output file so that files generated by further tests are not mistaken for this one.

Fourth, I let the system wait for a while so that you can see things and let `mininet` finish cleanup.

Now, we can take a look at the python script:

```python
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
    h1.cmd("xterm -hold -e ./server -d ./ -p 10000 -w 5&")
    time.sleep(1)
    h2.cmd("xterm -hold -e ./client -f alice.txt -h 10.0.0.1 -p 10000 -w 3")
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    TMUDPTest(lossy=(int(argv[1])))
```

It is a little different from the original test.py in these ways:

1. I have removed h3 and h4 from the topo.
2. I run commands directly from this script
3. There is no CLI process.

The commands run by h1 and h2 follow the template given in **README**, but I think it is necessary to explain a little:

1. `-d` argument has to be a directory that already exists and must end with `/`.
2. `-f` argument has to be a file that exists.
3. `-p` argument should be the same for client and server.

### Host

Halfway finished with my code, I found that client and server share some basic functions:

1. Sending messages
2. Receiving messages

So, to not repeat myself twice when changing a piece of code, I decided to write a base class directly providing these two functions.

### Client

The client has three stages:

1. Start
2. Data
3. End

The start stage is harder than I first imagined, because the client has to figure out which `IP:Port` it is on. It then sends out this message to the server until it receives an ACK. This is necessary because the server can't get the client's `IP:Port` from the command line, so the client has to notice the server of this.

The data process is a sliding window whose size is fixed.

The end process tells the server that the transmission is finished. It does this quite a few times to make sure that the server hears this.

### Server

The server also has three types of actions:

1. Start
2. Data
3. End

If a packet is labeled Start, then the server updates it's Client info so as to send ACKs back.

If a packet is labeled Data, then the server checks if it is the packet that it is expecting. If it is, then the server saves that packet and sends back an ACK, else it discards it. Notice that this is using GBN procedures and the window size for the receiver doesn't really work.

If a packet is labeled End, then the server jumps out of the loop and saves the packets into the disk.

## Questions

`Mininet's` loss mechanism doesn't corrupt packets, it drops them. So the CRC checksum portion for this experiment can't actually be tested.