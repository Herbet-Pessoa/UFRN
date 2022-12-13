#!/usr/bin/env python

"""This example creates a simple network topology in which
   stations are equipped with batteries"""

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.term import makeTerm


def topology():
    "Create a network."
    net = Mininet_wifi(iot_module='fakelb')
    # iot_module: fakelb or mac802154_hwsim
    # mac802154_hwsim is only supported from kernel 4.18

    info("*** Creating nodes\n")
    s1 = net.addSensor('sensor1', ip6='2001::1/64', voltage=3.7, panid='0xbeef')
    net.addSensor('sensor2', ip6='2001::2/64', voltage=3.7, panid='0xbeef')
    net.addSensor('sensor3', ip6='2001::3/64', voltage=3.7, panid='0xbeef')

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Starting network\n")
    net.build()

    info("*** Starting Socket Server\n")
    net.socketServer(ip='127.0.0.1', port=12345)

    makeTerm(s1, title='sensor1', cmd="bash -c 'ping 2001::2;'")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
