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
    net = Mininet( controller=RemoteController, topo=None, build=False, link=TCLink)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, protocols='OpenFlow10', listenPort=6673) # Router
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, protocols='OpenFlow10', listenPort=6673) # VNF
    
    info( '*** Adding controller\n' )
    c0 = net.addController(name='c0', ip='127.0.0.1', port=6633) # Pox Controller

    info( '*** Add hosts\n')
    client_private_dir = [("/etc", "/tmp/h1/etc")]
    h1 = net.addHost('h1', cls=Host, ip='192.168.1.1/24', mac='00:00:00:00:00:01', defaultRoute='via 192.168.1.254', privateDirs=client_private_dir)

    h2_private_dir = [("/var", "/tmp/h2/var")]
    h2 = net.addHost('h2', cls=Host, ip='192.168.2.1/24', mac='00:00:00:00:00:02', defaultRoute='via 192.168.2.254', privateDirs=h2_private_dir)
    
    h3_private_dir = [("/var", "/tmp/h3/var")]
    h3 = net.addHost('h3', cls=Host, ip='192.168.3.1/24', mac='00:00:00:00:00:03', defaultRoute='via 192.168.3.254', privateDirs=h2_private_dir)


    info( '*** Add links\n')
    net.addLink( h1, s1, bw=10, delay='40ms')
    net.addLink( h2, s1, bw=10, delay='40ms')
    net.addLink( h3, s1, bw=10, delay='40ms')
    net.addLink( s1, s2, bw=10, delay='40ms')
    
    info( '*** Starting network\n')
    net.build()


    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()


    info( '*** Starting switches\n')
    s1.start([c0])
    s2.start([c0])
    

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
