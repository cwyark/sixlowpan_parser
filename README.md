# 6lowpan parser

Here we explain all of the values calculation process based on the numbers retrieved:
First the values retrieved in the UDP data payload looks something like this:

3,150,17941,293098,3208,311025,307817,615,65535,483,8,65427,37,134

for example we can store in an array called values like this :

values[] = {3,150,17941,293098,3208,311025,307817,615,65535,483,8,65427,37,134};

each value is separated using a semicolon, and that line of data represent these values in the same order :

num_neighbors,parent_etx,cpu,lpm,transmit,radio,listen,temp,rh,rtmetric,beacon_interval,rss,lqi,bateria

Calculation :

Constants:

VOLTAGE = 3;

TICKS_PER_SECOND = 4096L;

POWER_CPU = 1.800 * VOLTAGE; /* mW */

POWER_LPM = 0.0545 * VOLTAGE; /* mW /
POWER_TRANSMIT = 17.7 * VOLTAGE; / mW /
POWER_LISTEN = 20.0 * VOLTAGE; / mW */

1- Number of neighbour : values[1] = 3 (no need to calculate)

2- ETX = values[2] / 8.0

3- CPUPower = values[3] * POWER_CPU) / (values[3] + values[4]) ------ example result look like this: 17941*3 /17941+293098

4- LPMPower = values[4] * POWER_LPM) / (values[3] + values[4]

5- TransmitPower = values[5] * POWER_TRANSMIT) / (values[3] + values[4])

6- Ignore radio for now

7-ListenRadioPower = values[7] * POWER_LISTEN) / (values[3] + values[4]

8- Temperature: value[8] = 615

9-Humidity: value[9]=-4.0 + 405.0 * values[9] / 10000.0 (if the result greater than 100 , return 100)

10- BeaconInterval = value[10] -- no need to change

11- RSSI: value[11] no need to change (dBm)

12- LQI = value[12] no need to change

13 = values[13] * 2 * 2.5 / 4096.0

if you have any further questions please let me know

## Reference

* [https://vnetman.github.io/pcap/python/pyshark/scapy/libpcap/2018/10/25/analyzing-packet-captures-with-python-part-1.html](https://vnetman.github.io/pcap/python/pyshark/scapy/libpcap/2018/10/25/analyzing-packet-captures-with-python-part-1.html)

* [https://github.com/secdev/scapy/blob/ef2dd57e6b5c6f0ad77818854bc6e5e56a1a492b/test/dot15d4.uts](https://github.com/secdev/scapy/blob/ef2dd57e6b5c6f0ad77818854bc6e5e56a1a492b/test/dot15d4.uts)
