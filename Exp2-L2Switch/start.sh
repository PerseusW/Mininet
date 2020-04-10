# Command used to start topo using OVS controller
 sudo mn --custom=TopoSet.py --topo=MaxLeafTopo --controller=remote --switch=ovs --link=tc

# Command used to start POX Controller (Enter POX directory first)
# $ ./pox.py openflow.discovery openflow.spanning_tree --no-flood --hold-down forwarding.l2_learning openflow.of_01 --port=6666

# Command used to start topo using POX Controller
# sudo mn --custom=TopoSet.py --topo=LoopTopo --controller=remote,ip=127.0.0.1,port=6666 --switch=ovsk --link=tc
