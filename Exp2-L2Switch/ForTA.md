# Assignment 2

### Self-learning Switch

The self-learning switch is already implemented in of_tutorial and can be tested as following:

```shell
#Start controller
#Supposing you are already in my assignment folder
$ cd pox
$ ./pox.py misc.of_tutorial
```

```shell
#Start network in another terminal
$ sudo mn --topo=single,3 --mac --controller=remote --switch=ovsk
mininet> ......
#On my virtual machine, iperf is about 52Gbps
```

### Assignment 1 Retest

I have copied my adtopo.py and start.sh from assignment 1 into the assignment 2 folder, and changed controller from ovsc to remote (nothing else was changed). Test as following:

```shell
#Start controller
$ ./pox.py misc.CustomController
```

```shell
#Start network in another terminal
$ ./start.sh
mininet> ......
#On my virtual machine, pingall has 0%-2% loss and iperf has around 25Mbps
```

### STP

You can directly test my STP implementation with of_tutorial.py. The implementation is not complete yet, but it should be able to pass the loop.py that we were given.

```shell
#Start three controllers in three terminals
$ ./pox.py openflow.of_01 --port=6632 misc.of_tutorial
$ ./pox.py openflow.of_01 --port=6633 misc.of_tutorial
$ ./pox.py openflow.of_01 --port=6634 misc.of_tutorial
```

```shell
#Run loop.py in another terminal
$ sudo python loop.py
```

