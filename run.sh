#!/bin/sh
# showIPandMAC.sh
 
s2Eth2=$(ip link show s2-eth2 | awk '/ether/ {print $2}')
s3Eth3=$(ip link show s3-eth3 | awk '/ether/ {print $2}')
s2Eth1=$(ip link show s2-eth1 | awk '/ether/ {print $2}')
s1Eth2=$(ip link show s1-eth2 | awk '/ether/ {print $2}')

echo "s2-eth2 MAC Address: $s2Eth2"
echo "s3-eth3 MAC Address: $s3Eth3"
echo "s2-eth1 MAC Address: $s2Eth1"
echo "s1-eth2 MAC Address: $s1Eth2"

sed -i "s/ether_encap1 :: EtherEncap(0x0800,.*/ether_encap1 :: EtherEncap(0x0800, $s2Eth2, $s3Eth3);/" vnf.click
sed -i "s/ether_encap2 :: EtherEncap(0x0800,.*/ether_encap2 :: EtherEncap(0x0800, $s2Eth1, $s1Eth2);/" vnf.click
