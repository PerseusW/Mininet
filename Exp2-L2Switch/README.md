# Assignment 2: Datalink layer: Switch
## Due Oct. 09, 2019, 11:59PM (GMT+8)
### Intro

The following part is partly referenced from [openflow-tutorial](https://github.com/mininet/openflow-tutorial/wiki/Create-a-Learning-Switch).

### Part 1 ARP and MAC
#### 1.1 Wireshark
Wireshark is a free and open-source packet analyzer. It is used for network troubleshooting, analysis, software and communications protocol development, and education(Wikipedia).

In reality world the packet(IP packet) is very complex and hard-to-read for human beings.

i.e. IP packet:
````
9:31:19.422499 IP6 fe80::b023:b9ff:fe05:d2cc.5353 > ff02::fb.5353: 0 [9q]
PTR (QM)? _nfs._tcp.local. PTR (QM)? _ipp._tcp.local. PTR (QM)? _ipps._tcp.local.
PTR (QM)? _ftp._tcp.local. PTR (QM)? _webdav._tcp.local. PTR (QM)? _webdavs._tcp.local.
PTR (QM)? _sftp-ssh._tcp.local. PTR (QM)? _smb._tcp.local.
PTR (QM)? _afpovertcp._tcp.local. (141)
	0x0000:  3333 0000 00fb b223 b905 d2cc 86dd 600b  33.....#......`.
	0x0010:  fa12 0095 11ff fe80 0000 0000 0000 b023  ...............#
	0x0020:  b9ff fe05 d2cc ff02 0000 0000 0000 0000  ................
	0x0030:  0000 0000 00fb 14e9 14e9 0095 3a1b 0000  ............:...
	0x0040:  0000 0009 0000 0000 0000 045f 6e66 7304  ..........._nfs.
	0x0050:  5f74 6370 056c 6f63 616c 0000 0c00 0104  _tcp.local......
	0x0060:  5f69 7070 c011 000c 0001 055f 6970 7073  _ipp......._ipps
	0x0070:  c011 000c 0001 045f 6674 70c0 1100 0c00  ......._ftp.....
	0x0080:  0107 5f77 6562 6461 76c0 1100 0c00 0108  .._webdav.......
	0x0090:  5f77 6562 6461 7673 c011 000c 0001 095f  _webdavs......._
	0x00a0:  7366 7470 2d73 7368 c011 000c 0001 045f  sftp-ssh......._
	0x00b0:  736d 62c0 1100 0c00 010b 5f61 6670 6f76  smb......._afpov
	0x00c0:  6572 7463 70c0 1100 0c00 01              ertcp......
````

Wireshark will `Capture` the packet and analyze then it will translate the binary bit flow into easy-to-understand information.

1.2 ARP

You have already learn from class that ARP is a Datalink layer protocol which will transfer IP address into MAC address via flooding and spanning tree(broadcasting and caching).

And normally, the IP packet looks like this:

\######IP Header#########Datalink Header############DATA############

In the following part, ICMP is a IP layer(Network layer) Protocol. You may not know it but remember when we ping somebody we will use "simple packet"(ICMP) instead of "complex packet"(TCP socket).

1.3 How ARP works in practice

`ctrl+shift+t` to open your Terminal, let's first create a simple scenario(with 3 hosts star-like network),
````
$ sudo mn --topo single,3 --switch ovsk
````
Then in mininet, we need to send and receive packet on individual hosts,
````
mininet> xterm h1 h1 h2 h3
````
First we set h2 and h3 into receive && print packet mode(type the code in each BLACK Terminal/xterm), \
(you may find # instead of $ in xterm, but we still use $ to represent command in Ubuntu Terminal)
````
# In "Node:h2"
$ tcpdump -XX -n -i h2-eth0
# In "Node:h3"
$ tcpdump -XX -n -i h3-eth0
````
Then let h1 send packets
````
# In "Node:h1" and why we ping 10.0.0.2 is because 10.0.0.2 should be h2's IP address
# you can use $ ifconfig to check it
$ ping 10.0.0.2 -c5
````
You will see h3 capture one "ARP packet" and many "ICMP6 packet" whereas h2 capture two "ARP packet", many "ICMP6 packet" and many "ICMP packet". But it's very messy for us to understand what really happened there.

Now stop h2's and h3's `Capture` and use Wireshark to do this job,
````
# In "Node:h2"
ctrl+c
$ wireshark
double click h2-eth0 in Wireshark's UI

# In "Node:h3"
ctrl+c
$ wireshark
double click h3-eth0 in Wireshark's UI

# In one "Node:h1" (notice we open 2 "Node:h1" windows)
$ wireshark
double click h1-eth0 in Wireshark's UI

# In the other "Node:h1"
ping 10.0.0.2 -c5
````
Now rank the time starting from 0 and ignore ICMP6 Packet(ICMP for IPv6) and MDNS(Multiple-DNS) we will talk about DNS in Application layer), you will find 10 "ICMP packet" respect to 5 times ping commands(go + back = 2). You may wondering where is ARP, because we just type the IP address without MAC address(hardware address).

Now let's start over(close xterm, close mininet, close Terminal and start mininet again),

````
ctrl+shift+t to open your Terminal
$ sudo mn --topo single,3 --switch ovsk
mininet> xterm h1 h1 h2 h3

# In one "Node:h1"
$ wireshark
double click h1-eth0 in Wireshark's UI

# In "Node:h2"
$ wireshark
double click h2-eth0 in Wireshark's UI

# In "Node:h3"
$ wireshark
double click h3-eth0 in Wireshark's UI

# In the other "Node:h1"
ping 10.0.0.2 -c5
````

Rank based on Time and ignore ICMP6 and MDNS, now you will see h1 send a APR request with info "who has..." then h2 and h3 receive the ARP packet and h2 reply, then h1 receive the reply packet. Then following with 10 ICMP, 5 times `ping` is finished.

Please spend some time on finding how the binary bit flow(click each packet and watch below) is translated into line information above (Source+Destination+Protocol+Length+Info).

And why in the first time we see ICMP(ping destination directly) then ARP(find where destination is) instead of starting from ARP to ICMP?

 Because as h1 first ping and h2&&h3 capture it(`tcpdump -XX`), the ovsk(ovs-kernel mode) switch will record the process(self-learning: remember how switch works). Now you can use h1 to ping again`$ ping 10.0.0.2 -c5` you will find that h1 and h2 first ICMP then ARP to keep MAC information updated.

Once you have finished this part DO NOT close the mininet because we still need it in the second part.

### Part 2 Switch

#### 2.1 Hub and Switch

You may not know the [difference between hub and switch](https://www.diffen.com/difference/Hub_vs_Switch) and perhaps even don't know what [hub](https://en.wikipedia.org/wiki/Hub_(network_science)) is(Use search engine). Simply speaking, hub is just a physical connection component which will not interface any logical work(i.e. where to transfer next, who, where). However one switch(smarter hub) can perform as many hubs or hubs with controller(switch will learn and transmit to specific port).

Remember in section 1, we use `ovsk`, a smart self-learning-capable switch. In wireshark, you will find except the first time when h1 `ping` 10.0.0.2 when ARP will flood to h2 and h3, h3 will never receive any ARP because `ovsk` "knows" it should transmit ARP to h2(or to say the port connected to h2) instead of h3.

Now, let's see how hub works.
````
# First measure the bandwidth using ovsk(should be Gbit per seconds)
# Back to part 1 the mininet client Terminal
mininet> iperf

# Then close mininet and clean it
mininet> quit()
$ sudo mn -c

# Start over but with controller control ovsk perform like hubs
# First open your pox folder, should be the folder where /mininet /fox /openflow are all in.
# If you can't find where pox is you can git clone a new one,
# visit https://github.com/noxrepo/pox or $ git clone https://github.com/noxrepo/pox.git
$ cd pox/
$ ./pox.py log.level --DEBUG misc.of_tutorial
# This Terminal is marked as pox Terminal

# Now in other Terminal(ctrl+shift+t) open mininet
# and rerun what we do in section 1 but with a remote pox controller
$ sudo mn --topo single,3 --mac --controller remote --switch ovsk

# Then you will see something like this in the pox Terminal,
INFO:openflow.of_01:[Con 1/1] Connected to 00-00-00-00-00-01
DEBUG:misc.of_tutorial:Controlling [00-00-00-00-00-01 1]

# Check bandwidth(should be Mbps)
mininet> pingall
mininet> iperf
# And the RTT of ping is very unstable
mininet> h1 ping h2 -c 5

# In wireshark, you will find when h1 ping h2, ARP still will be sent to h3
mininet> xterm h1 h1 h2 h3

# In one "Node:h1"
$ wireshark
double click h1-eth0 in Wireshark's UI

# In "Node:h2"
$ wireshark
double click h2-eth0 in Wireshark's UI

# In "Node:h3"
$ wireshark
double click h3-eth0 in Wireshark's UI

# In the other "Node:h1"
ping 10.0.0.2 -c2 # do this many times and watch for ARP
ping 10.0.0.2 -c2
ping 10.0.0.2 -c2
````

After this, it's time to think the difference between hub and switch.

#### 2.2 Design a self learning switch

In my machine, the bandwidth with default controller `$ sudo mn --topo single,3 --switch ovsk` is about 64Gbps and bandwidth with our initial(of_tutorial.py) controller,
````
# One Terminal
$ ./pox.py log.level --DEBUG misc.of_tutorial

# The other one
$ sudo mn --topo single,3 --mac --controller remote --switch ovsk
````
is about 6.4Mbps, which means that switch run about 10000x faster than hub.

You may notice that we use [pox](https://github.com/noxrepo/pox) to work as [Openflow](https://github.com/mininet/openflow) controller and Openflow is a protocol which also support Mininet's many functions. Indeed pox has already built many parts of a switch and you just need to implement its self learn function.

##### 2.2.1 Requirment

Now you should design a self learning switch and whose bandwidth should be about 60Gbps or to say about at least 1000x more bandwidth than hub (70% scores).

The easiest way to do so is to use template provided by pox. Implement the `act_like_switch (self, packet, packet_in)` in `\pox\pox\misc\of_tutorial.py` and run it via `$ ./pox.py log.level --DEBUG misc.of_tutorial` (under \pox\pox folder)

Pox provides many psuedocode in `of_tutorial.py` and implements most of switch-need-functions which makes designing a switch quiet a easy job(within 10/100 lines codes).

Of course, you can design a switch with other ways like without pox and write controller directly in Mininet and if you do so, please `git push` your modification and a brief introduction about how to rerun it.

##### 2.2.2 Test

If you use pox as remote controller:

Test your switch with,
````
# In one Terminal with location at your /pox folder
$ ./pox.py log.level --DEBUG misc.of_tutorial

# In another Terminal
$ sudo mn --topo single,3 --mac --controller remote --switch ovsk
mininet> iperf
mininet> iperf
# If your switch works well, its bandwidth should be about 1000x-10000x than hub's
# In _handle_PacketIn (self, event), you can change its working mode from switch to hub(act_like_hub (self, packet, packet_in))
````

If you achieve switch with other way like ryu controller
````
# In one Terminal
$ ryu manager YOUR_Ryu_APP || or other command to wake up remote switch

# In another Terminal
$ sudo mn --topo single,3 --mac --controller remote --switch ovsk
mininet> iperf
mininet> iperf
# If your switch works well, its bandwidth should be about at least 1Gbps
````

**Notice that implementation with pox/ryu under only one controller is a centralized switching method(SDN(control plane) over all switch)**

##### 2.2.3 adtopo

Try your switch on your adtopo.py in Assignment1. You can modify your switch to better meet your topology, and if it works faster, come to let TAs update your score on Assignment1.

##### 2.2.4 Bonus(40%)

You may in class have learn STP(Spanning Tree Protocol) to break loops, and we wish you can implement it in your switch which should break loop via protocol like STP.

###### 2.2.4.1 Requirement

Use `loop.py` which will build a ring topology to test your switch(DO NOT modify `loop.py` and the command $ sudo python loop.py). And we hope your STP is distributed(one controller runs over only ONE switch), thus if you use remote controller to achieve STP please let them listen/control to `remote:6632`, `remote:6633` and `remote:6634` (open `loop.py` to see the topology).

You can use any method(I personally recommend search GitHub) to achieve this but remember to note the code sources. And in your STP-switch s2(second smallest bridge in loop.py) should be Root bridge(Google/baide/CSDN Spanning tree protocol to check the def) instead of s1, which is to say Your_STP_Switch should have the rule that second smallest bridge has highest priority instead of the first one.

And you will get full bonus if you can achieve 0% dropped rate within 3 times `pingall` and 1. Distributed, 2. With 2nd largest priority.

You may get less bonus using centralized instead distributed stp.

You may get less bonus if directly using given high-level switches/controllers.

Please provide related code with a startup introduction to let us rerun your code and test controllers via,
````
# You should open 3 controller response to 3 switches/ open one but can listen to 3 ports(less bonus)
# In your first "switch-controller" Terminal
$ Something_to_open_remote_controller

# In your second "switch-controller" Terminal
$ Something_to_open_remote_controller

# In your third "switch-controller" Terminal
$ Something_to_open_remote_controller

# In another Terminal
# You MUST only use controller to achieve breaking loops
# Thus DO NOT modify the following command and loop.py
$ sudo python loop.py
mininet> pingall
mininet> pingall
mininet> pingall
````

You can also choose to not use controller but to use SOCKET(Not recommended). For example something like [this](https://github.com/rivalak/stp), but keep in mind that DO NOT modify `loop.py`.

**You might need to backup your pox/ryu/other folder.**

###### Hints

There exists so many ways to achieve loops breaking. And we hope you can achieve distributed STP switch controller instead centralized switch controller(In centralized method, there is only one controller which manages every switch|link|host achieved via SDN-software defined network).

[Ryu](https://osrg.github.io/ryu/) Controller provides a [way to achieve stp centralized](https://osrg.github.io/ryu-book/en/html/spanning_tree.html), maybe give it a try. If you use ryu, you need first figure out how to [write a switch via ryu](https://osrg.github.io/ryu-book/en/html/switching_hub.html), then how [centralized stp works](https://osrg.github.io/ryu-book/en/html/spanning_tree.html)(which is quiet close to stp talked in class), then modify it to distributed(maybe write 3 diff controllers listening to diff ports or just use one but add some port_listen_argument in Terminal commands, after that we require you must use s2(second smallest bridge) as Root bridge-[def of Root bridge](https://osrg.github.io/ryu-book/en/html/spanning_tree.html).

We hope you can understand the whole spanning tree protocol instead of just following official guidance. Thus you must choose s2 as root bridge every time(which is to say your stp should have the rule that the second smallest bridge's priority is bigger than the smallest ones || we will test it via different switch names or numbers) otherwise you will get less bonus.

As for pox, DO NOT straggle in just implementing `of_tutorial.py`, and you are allowed to use all pox functions(maybe: visit /pox/pox/openflow/ and check what they do and find a way to use it)(pox uses a quiet different way to achieve loop breaking!!! We encourage you to use ryu which is more close to stp talked in class).

**If you directly use pox build in switch(L2/L3) to achieve stp you will get less bonus**

###### Test

In Assign-2, we provide a `loop.py` where every switch will listen to diff ports. Maybe you can test, for example, your [ryu application](https://ryu.readthedocs.io/en/latest/writing_ryu_app.html) via,
````
# In your first "ryu controller" Terminal
$ ryu-manager Your_stp_switch1.py # or maybe add some arguement instead of 3 diff .py or one ryu-manager(less bonus)

# In your second "ryu controller" Terminal
$ ryu-manager Your_stp_switch2.py

# In your third "ryu controller" Terminal
$ ryu-manager Your_stp_switch3.py

# In another Terminal
# DO NOT modify the following command and loop.py
$ sudo python loop.py
mininet> pingall
mininet> pingall
mininet> pingall
````

### How to submit your Assignment-2

We have solved the problem and you need to submit your assignment via git/GitHub
````
### Pull
# You will recieve a assign_link  
# like(https://github.com/NJU-CS-network-19-fall/assignment2-Your_Screen_Name)
$ git clone assign_link
$ cd Assignment2

# Enjoy coding

### Push
$ cd Assignment2
$ git add -A
$ git commit -m "marks/words"
$ git push origin master
````

### Notice

**Please send/push your modification on pox/ryu/others and MAKE SURE we can rerun your switch just use what sent/pushed.**

**Please submit your code before Oct 10.**

**Late submission of homeworks and assignments is not accepted.**
