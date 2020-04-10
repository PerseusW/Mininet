from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()



class Tutorial (object):

  def __init__ (self, connection):
    self.connection = connection
    connection.addListeners(self)
    self.macToPort = {}

  def outputPacket (self, packetInfo, outputPorts):
    outputMsg = of.ofp_packet_out()
    outputMsg.data = packetInfo
    outputMsg.actions.append(of.ofp_action_output(port = outputPorts))
    self.connection.send(outputMsg)

  def actLikeHub (self, packet, packetInfo):
    if len(packetInfo.data) == packetInfo.total_len:
      self.outputPacket(packetInfo, of.OFPP_FLOOD)
    else:
      log.warning("Ignoring incomplete packet")

  def actLikeSwitch (self, packet, packetInfo):
    if packet.src not in self.macToPort:
      self.macToPort[packet.src] = packetInfo.in_port
      log.debug("Installing flow: %s -> %s",packet.src,packetInfo.in_port)
      flowMod = of.ofp_flow_mod()
      flowMod.match.dl_dst = packet.src
      flowMod.actions.append(of.ofp_action_output(port = packetInfo.in_port))
      flowMod.actions.append(of.ofp_action_output(port = packetInfo.in_port))
      self.connection.send(flowMod)    
    if packet.dst not in self.macToPort:
      self.outputPacket(packetInfo, of.OFPP_FLOOD)

  def _handle_PacketIn (self, event):
    packet = event.parsed
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return
    packetInfo = event.ofp
    #self.actLikeHub(packet, packetInfo)
    self.actLikeSwitch(packet, packetInfo)



def launch ():
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Tutorial(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
