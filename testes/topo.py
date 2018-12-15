#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
"""
Essa eh a topologia que provavelmente vai funcionar, mas nao eh a ideal.
Nessa topologia o trafego fica: h1 ... s1-eth1 ... s1-eth2 ... s2-eth1 ... s2-eth2 ... s3-eth1 ... s3-eth2 ... h2
"""
def myNetwork():

    net = Mininet( topo=None, build=False)

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0', controller=RemoteController, ip='127.0.0.2', protocol='tcp', port=6653) # Ryu
    #c1 = Controller( 'c1', port=6633 )
    #net.addController(c1)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch) # Router1
    #s3 = net.addSwitch('s3', cls=OVSKernelSwitch) # Switch with click function runnning
    #s3 = net.addSwitch('s3', cls=OVSKernelSwitch) # Router1

    info( '*** Add hosts\n')
    client_private_dir = [("/etc", "/tmp/h1/etc")]
    h1 = net.addHost('h1', cls=Host, ip='192.168.1.1/24', mac='00:00:00:00:00:01', defaultRoute='via 192.168.1.254', privateDirs=client_private_dir)

    h2_private_dir = [("/var", "/tmp/h2/var")]
    h2 = net.addHost('h2', cls=Host, ip='192.168.2.1/24', mac='00:00:00:00:00:02', defaultRoute='via 192.168.2.254', privateDirs=h2_private_dir)

    h3_private_dir = [("/var", "/tmp/h3/var"),("/etc", "/tmp/h3/etc")]
    h3 = net.addHost('h3', cls=Host, ip='192.168.3.1/24', mac='00:00:00:00:00:03', defaultRoute='via 192.168.3.254', privateDirs=h3_private_dir)
    
    h4 = net.addHost('h4')


    info( '*** Add links\n')
    #net.addLink( h1, s1)
    #net.addLink( h2, s3)
    #net.addLink( h3, s3)
    #net.addLink( s1, s2)
    #net.addLink( s2, s3)
    #net.addLink( s1, s3)
    net.addLink( h1, h4)
    net.addLink( h2, s1)
    net.addLink( h3, s1)
    net.addLink( h4, s1)

    info( '*** Starting network\n')
    net.build()

    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    s1.start([c0])
    s1.cmd('ovs-vsctl set Bridge s3 protocols=OpenFlow13')
    #s2.start([c0])
    #s2.cmd('ovs-vsctl set Bridge s2 protocols=OpenFlow13')
    #s2.start([c1])
    #s2.cmd('ovs-vsctl set Bridge s2 protocols=OpenFlow13')

    #s3.start([c0])
    #s3.cmd('ovs-vsctl set Bridge s3 protocols=OpenFlow13')

    info( '*** Starting Ryu Controller\n')
    c0.cmd('ryu-manager ryu.app.rest_router &')
    #c0.cmd('./set_ryu_router.sh')
    #c1.cmd('ryu-manager ryu.app.example_switch_13 &')
    info( '*** Starting web servers\n')
    h2.cmd('cd /var/www')
    h2.cmd('python -m SimpleHTTPServer 80 &')
    h3.cmd('cd /var/www')
    h3.cmd('python -m SimpleHTTPServer 80 &')

    info( '*** Post configure switches and hosts\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
