// IP-Rewriter

// Device declaration
FromDevice(s2-eth1, SNIFFER false) -> ThreadSafeQueue -> ToDevice(s2-eth2);
FromDevice(s2-eth2, SNIFFER false) -> ThreadSafeQueue -> ToDevice(s2-eth1);


