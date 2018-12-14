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

def myNetwork():

    net = Mininet( topo=None, build=False)

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0', controller=RemoteController, ip='127.0.0.1', protocol='tcp', port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)


    info( '*** Add hosts\n')
    client_private_dir = [("/etc", "/tmp/h1/etc")]
    h1 = net.addHost('h1', cls=Host, ip='192.168.1.1/24', mac='00:00:00:00:00:01', defaultRoute='via 192.168.1.254', privateDirs=client_private_dir)

    h2_private_dir = [("/var", "/tmp/h2/var")]
    h2 = net.addHost('h2', cls=Host, ip='192.168.2.1/24', mac='00:00:00:00:00:02', defaultRoute='via 192.168.2.254', privateDirs=h2_private_dir)

    h3_private_dir = [("/var", "/tmp/h3/var"),("/etc", "/tmp/h3/etc")]
    h3 = net.addHost('h3', cls=Host, ip='192.168.3.1/24', mac='00:00:00:00:00:03', defaultRoute='via 192.168.3.254', privateDirs=h3_private_dir)


    info( '*** Add links\n')
    net.addLink( h1, s1)
    net.addLink( h2, s1)
    net.addLink( h3, s1)
    net.addLink( s2, s1)

    info( '*** Starting network\n')
    net.build()

    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    s1.start([c0])
    s1.cmd('ovs-vsctl set Bridge s1 protocols=OpenFlow13')

    s2.start([c0])
    s2.cmd('ovs-vsctl set Bridge s2 protocols=OpenFlow13')

    info( '*** Starting Ryu Controller\n')

    #c0.cmd('ryu-manager ryu.app.rest_router &')
    #c0.cmd('curl -X POST -d \'{\"address":"192.168.1.254/24\"}\' http://localhost:8080/router/0000000000000001')
    #c0.cmd('curl -X POST -d \'{\"address":"192.168.2.254/24\"}\' http://localhost:8080/router/0000000000000001')

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
