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

    net = Mininet( topo=None, build=False, link=TCLink)

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0', controller=RemoteController, ip='127.0.0.1', protocol='tcp', port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)


    info( '*** Add hosts\n')
    client_private_dir = [("/etc", "/tmp/h1/etc")]
    h1 = net.addHost('h1', cls=Host, ip='192.168.1.1', mac='00:00:00:00:00:01', defaultRoute='via 192.168.1.254', privateDirs=client_private_dir)

    h2_private_dir = [("/var", "/tmp/h2/var")]
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.1', mac='00:00:00:00:00:02', defaultRoute='via 10.0.0.254', privateDirs=h2_private_dir)

    h3_private_dir = [("/var", "/tmp/h3/var"),("/etc", "/tmp/h1/etc")]
    h3 = net.addHost('h3', cls=Host, ip='192.168.3.1', mac='00:00:00:00:00:03', defaultRoute='via 192.168.3.254', privateDirs=h3_private_dir)


    info( '*** Add links\n')
    net.addLink( h1, s1, intfName2='s1-eth1',params2={ 'ip' : '192.168.1.254/24' } )
    net.addLink( h2, s1, intfName2='s1-eth2',params2={ 'ip' : '10.0.0.254/8' } )
    net.addLink( h3, s1, intfName2='s1-eth3',params2={ 'ip' : '192.168.3.254/24' } )
    net.addLink( s2, s1, intfName2='s1-eth4',params2={ 'ip' : '192.168.4.254/24' } )

    info( '*** Starting network\n')
    net.build()

    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')

    net.get('s1').start([c0])
    net.get('s2').start([c0])

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
