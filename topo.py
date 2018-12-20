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

    info( '*** Add switch\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, protocols='OpenFlow10', listenPort=6673) # Router
    
    info( '*** Adding controller\n' )
    c0 = net.addController(name='c0', ip='127.0.0.1', port=6633) # Pox Controller

    info( '*** Add hosts\n')
    for i in range(1,4):
        h = 'h%s' % i
        print "--> %s" % h
        etc_path = '/tmp/%s/etc' % h
        client_private_dir = [("/etc", etc_path)]
        IP_addr = '192.168.%s.1/24' % i
        Mac_addr = '00:00:00:00:00:0%s' % i
        Gw = 'via 192.168.%s.254' % i
        
        if i == 1:
            net.addHost(h, cls=Host, ip=IP_addr, mac=Mac_addr, defaultRoute=Gw, privateDirs=client_private_dir) #client
        else:
            var_path = '/tmp/h%s/var' % i
            server_private_dir = [("/var", var_path)]
            print "addhost(%s)" % h
            net.addHost(h, cls=Host, ip=IP_addr, mac=Mac_addr, defaultRoute=Gw, privateDirs=server_private_dir) # servers
    
    net.addHost('h4', cls=Host, ip='192.168.4.1/24', mac='00:00:00:00:00:50', defaultRoute='via 192.168.4.254') # VNF


    info( '*** Add links\n')
    for i in range(1,5):
        h = 'h%s' % i
        net.addLink( h, s1, bw=10, delay='40ms')
        
    info( '*** Starting network\n')
    net.build()


    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()


    info( '*** Starting switches\n')
    s1.start([c0])
        

    info( '*** Starting web servers\n')
    for i in range(2,4):
        h = 'h%s' % i
        net.getNodeByName(h).cmd('cd /var/www && python -m SimpleHTTPServer 80 &')


    info( '*** Post configure switches and hosts\n')
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
