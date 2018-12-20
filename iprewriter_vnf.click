// IP-Rewriter
// Author: Jose Flauzino


// Device declaration
from_eth0 :: FromDevice(h4-eth0, SNIFFER false);
to_eth0 :: Queue(200) -> ToDevice(h4-eth0);

// Packets Classifier
classifier_input :: Classifier(
    12/0800, 		 // [0] IP Packet
    -                // [1] Others packets
);

classifier_ip :: IPClassifier(
    dst 192.168.2.1 tcp port 80, // [0] HTTP request
    dst 192.168.2.1 and icmp,	 // [1] ICMP echo request
    dst 192.168.1.1 tcp,         // [2] HTTP response
    dst 192.168.1.1 and icmp,	 // [3] ICMP echo response
    -                            // [4] Others IP packets
);

ip_rewriter :: IPRewriter(ip_mapper);
ip_mapper :: RoundRobinIPMapper(
    -           // Don't change source address
    -           // Don't change source port
    192.168.3.1 // Change destination address to 192.168.3.1
    -           // Don't change destination port
    0 1         // Port 0 pass request packets, Port 1 pass response packets
);

//Note: the mac address are as follow.
//s1-eth1: 00:00:00:00:00:10 <-> h1-eth1:  00:00:00:00:00:01
//s1-eth2: 00:00:00:00:00:20 <-> h2-eth1:  00:00:00:00:00:02
//s1-eth3: 00:00:00:00:00:30 <-> h3-eth1:  00:00:00:00:00:03
//s1-eth4: 00:00:00:00:00:40 <-> h4-eth0:  00:00:00:00:00:50

// From h4-eth0 to s1-eth4
ether_encap :: EtherEncap(0x0800, 00:00:00:00:00:50, 00:00:00:00:00:40);

from_eth0 -> classifier_input;
classifier_input[0] -> Strip(14) -> CheckIPHeader -> IPPrint(IP_packet) -> classifier_ip;
classifier_input[1] -> Print(Droped) -> Discard;

classifier_ip[0] -> ip_rewriter[0] -> IPPrint(TCP_Request) -> ether_encap -> to_eth0;
classifier_ip[1] -> Print(ICMP_Request) -> ICMPPingResponder -> to_eth0;
classifier_ip[2] -> ip_rewriter[1] -> IPPrint(TCP_Response) -> ether_encap -> to_eth0;
classifier_ip[3] -> Print(ICMP_Response) -> ICMPPingResponder -> to_eth0;
classifier_ip[4] -> IPPrint(Droped) -> Discard;


