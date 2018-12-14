// IP-Rewriter

// Device declaration
from_eth1 :: FromDevice(s2-eth1, SNIFFER false);
to_eth1 :: Queue -> ToDevice(s2-eth1);

from_eth2 :: FromDevice(s2-eth2, SNIFFER false);
to_eth2 :: Queue -> ToDevice(s2-eth2);

// Classifier internal and external
classifier_input, classifier_output :: Classifier(
    12/0800, 		 // [0] IP Packet
    -                // [1] Others packets
);

classifier_ip :: IPClassifier(
    dst 192.168.2.1 tcp port 80, // [0] HTTP request
//    dst 192.168.2.1 and icmp,	 // [1] ICMP echo request
    -                            // [4] Others IP packets
);

classifier_ip2 :: IPClassifier(
    dst 192.168.1.1 tcp, // [0] HTTP response
//    dst 192.168.2.1 and icmp,	 // [1] ICMP echo request
    -                            // [4] Others IP packets
);

ip_rewriter :: IPRewriter(ip_mapper);
ip_mapper :: RoundRobinIPMapper(- - 192.168.3.1 - 0 1);

// From s2-eth2 to s3-eth3
ether_encap1 :: EtherEncap(0x0800, d6:b4:d8:55:3f:b0, b6:b1:5d:e0:53:f7);
// From s2-eth1 to s1-eth2
ether_encap2 :: EtherEncap(0x0800, 52:4b:fc:c8:12:db, e2:7e:80:21:f1:ce);

from_eth1 -> classifier_input;
classifier_input[0] -> Strip(14) -> CheckIPHeader -> classifier_ip;
classifier_input[1] -> Print(Others1) -> to_eth2;

classifier_ip[0] -> ip_rewriter[0] -> ether_encap1 -> to_eth2;
classifier_ip[1] -> IPPrint(Others2) -> ether_encap1 -> to_eth2;

from_eth2 -> classifier_output;
classifier_output[0] -> Strip(14) -> CheckIPHeader -> classifier_ip2;
classifier_output[1] -> Print(Others3) -> to_eth1;

classifier_ip2[0] -> ip_rewriter[1] -> ether_encap2 -> to_eth1;
classifier_ip2[1] -> Print(Others4) -> ether_encap2 -> to_eth1;

