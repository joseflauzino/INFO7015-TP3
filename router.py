#!/usr/bin/python

from pox.core import core
from pox.lib.addresses import IPAddr
from pox.lib.addresses import EthAddr
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str, str_to_bool
from pox.lib.packet.arp import arp
from pox.lib.packet.ethernet import ethernet, ETHER_BROADCAST
import json
log = core.getLogger()

#Switch ID
switch1 = 0000000000000001

def open_file():
    # Edit next line for choose flow file
    file=open('flow_rules1.json','r')
    data = file.read()
    file.close()
    return json.loads(data)

#rule_params
# [cookie, in_port, nw_src, nw_dst, out_port, srcMAC, dstMAC]
def build_flow_rule(rule_params):
    # Rule
    rule = of.ofp_flow_mod()
    rule.cookie = int(rule_params['cookie'])
    rule.match.in_port = int(rule_params['in_port'])
    rule.match.dl_type = 0x0800
    if rule_params['nw_src'] != 'none':
        rule.match.nw_src = IPAddr(rule_params['nw_src'])
    rule.match.nw_dst = IPAddr(rule_params['nw_dst'])

    # Actions
    ruleout = of.ofp_action_output (port = int(rule_params['out_port']))
    rulesrcMAC = of.ofp_action_dl_addr.set_src(EthAddr(rule_params['srcMAC']))
    ruledstMAC = of.ofp_action_dl_addr.set_dst(EthAddr(rule_params['dstMAC']))
    rule.actions = [rulesrcMAC, ruledstMAC, ruleout]  
    
    return rule


def install_flows():
    log.info("    *** Installing static flows... ***")
    f = open_file()
    for i in range(int(f['count'])):
        j = 'flow%s' % i
        # Push flows to switches
        core.openflow.sendToDPID(switch1, build_flow_rule(f['rules'][j]))

    log.info("    *** Static flows installed. ***")

def _handle_ConnectionUp (event):
    log.info("*** install flows ***")
    install_flows()


# msg_param = [mac_src, packet, a, dpid, inport]
def build_msg(msg_param):
    r = arp()
    r.hwtype = msg_param[2].hwtype
    r.prototype = msg_param[2].prototype
    r.hwlen = msg_param[2].hwlen
    r.protolen = msg_param[2].protolen
    r.opcode = arp.REPLY
    r.hwdst = msg_param[2].hwsrc
    r.protodst = msg_param[2].protosrc
    r.protosrc = msg_param[2].protodst
    r.hwsrc = EthAddr(msg_param[0])
    
    e = ethernet(type=msg_param[1].type, src=r.hwsrc, dst=msg_param[2].hwsrc)
    e.payload = r
    
    log.info("%s answering ARP for %s" % (dpid_to_str(msg_param[3]), str(r.protosrc)))
    msg = of.ofp_packet_out()
    msg.data = e.pack()
    msg.actions.append(of.ofp_action_output(port = of.OFPP_IN_PORT))                            
    msg.in_port = msg_param[4]
    
    return msg


def _handle_PacketIn (event):
    dpid = event.connection.dpid
    inport = event.port
    packet = event.parsed
    if not packet.parsed:
        log.warning("%i %i ignoring unparsed packet", dpid, inport)
        return

    a = packet.find('arp')
    if not a: return

    log.info("%s ARP %s %s => %s", dpid_to_str(dpid),
      {arp.REQUEST:"request",arp.REPLY:"reply"}.get(a.opcode,
      'op:%i' % (a.opcode,)), str(a.protosrc), str(a.protodst))
    
    if a.prototype == arp.PROTO_TYPE_IP and a.hwtype == arp.HW_TYPE_ETHERNET and a.opcode == arp.REQUEST:
        if str(a.protodst)=="192.168.1.254":
            msg_param = ["00:00:00:00:00:10", packet, a, dpid, inport]
            
        if str(a.protodst)=="192.168.2.254":
            msg_param = ["00:00:00:00:00:20", packet, a, dpid, inport]
            
        if str(a.protodst)=="192.168.3.254":
            msg_param = ["00:00:00:00:00:30", packet, a, dpid, inport]
        
        if 'msg_param' in locals():
            event.connection.send(build_msg(msg_param))
        else:
            log.info("%i %i ignoring unparsed packet", dpid, inport)    
 


def launch ():
    log.info("*** Starting... ***")
    log.info("*** Waiting for switches to connect.. ***")
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
   
