// IPip_rewriteriter implementation

// AverageCounter
out_eth1 :: AverageCounter;
in_eth1 :: AverageCounter;

// Counter for classifier

// packets
pack_req_ex :: Counter;
pack_res :: Counter;

// arp
arp_req_ex :: Counter;
arp_res_ex :: Counter;

// Service
service_count :: Counter;
service_count2 :: Counter;
// ICMP
icmp_count :: Counter;

// Dropped
drop_ex :: Counter;

// Device declaration
da_eth1 :: FromDevice(s1-eth1, SNIFFER false);
para_eth1 :: Queue(200) -> out_eth1 -> pack_res -> ToDevice(s1-eth1);

da_eth2 :: FromDevice(s1-eth2, SNIFFER false);
para_eth2 :: Queue(200) -> out_eth1 -> pack_res -> ToDevice(s1-eth2);

da_eth3 :: FromDevice(s1-eth3, SNIFFER false);
para_eth3 :: Queue(200) -> out_eth1 -> pack_res -> ToDevice(s1-eth3);

// ARP Responder
//arpr_ext :: ARPResponder(10.0.0.2 fe:24:e2:fa:39:56);
//arpr_int :: ARPResponder(10.0.0.2 a2:fe:e8:7d:25:46);
arpr_ext :: ARPResponder(10.0.0.2 00:00:00:00:00:03);
//arpr_int :: ARPResponder(10.0.0.1 00:00:00:00:00:01);
// ARP Querier

arpq_ext :: ARPQuerier(10.0.0.3, 00:00:00:00:00:03);
arpq_int :: ARPQuerier(10.0.0.2, 00:00:00:00:00:03);

// Classifier internal and external
c_in :: Classifier(
    12/0806 20/0001, // [0] ARP Request
    12/0806 20/0002, // [1] ARP Response
    12/0800, 		 // [2] IP Packet
    -                // [3] Others packets
);

c_ip_in :: IPClassifier(
    dst 10.0.0.2 tcp port 80, // [0] http req
    dst 10.0.0.2 and icmp,	  // [1] icmp echo req
    -                         // [4] 
);

ip_rewriter :: IPRewriter(ip_mapper);
ip_mapper :: RoundRobinIPMapper(- - 10.0.0.3 - 0 1);

da_eth1 -> in_eth1 -> pack_req_ex -> c_in;
c_in[0] -> arp_req_ex -> arpr_ext[0] -> output_iface;
c_in[1] -> arp_res_ex -> [1]arpq_ext;
c_in[2] -> Strip(14) -> CheckIPHeader -> IPPrint(IP_packet)-> c_ip_in;
c_in[3] -> Discard;

c_ip_in[0] -> service_count -> ip_rewriter[0] -> IPPrint(request_tcp) -> [0]arpq_ext -> para_eth3;
c_ip_in[1] -> Print(icmp) -> icmp_count -> ICMPPingResponder -> [0]arpq_int -> para_eth1;
c_ip_in[4] -> IPPrint(Droped) -> drop_ex -> Discard;

da_eth3 -> in_eth2 -> pack_req_in -> c_ex;
c_ex[0] -> Print(www_ce_0) -> arp_req_in -> arpr_int[0] -> output_iface; 
c_ex[1] -> Print(www_ce_1) -> arp_res_in -> [1]arpq_int;
c_ex[2] -> Print(www_ce_2) -> Strip(14) -> CheckIPHeader -> ip_rewriter[0]-> IPPrint(***) -> [0]arpq_ext -> para_eth1;
c_ex[3] -> Print(www_ce_3) -> drop_in -> Discard;
