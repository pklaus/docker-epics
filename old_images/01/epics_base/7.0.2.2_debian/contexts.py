#!/usr/bin/env python

CONTEXTS = {
    # tag name:            template settings
    '7.0.2.2_debian':      {'base_img': 'debian:stretch', 'epics_host_arch': 'linux-x86_64', 'cross_build': False},
    '7.0.2.2_rpi_debian':  {'base_img': 'balenalib/raspberry-pi-debian:stretch', 'epics_host_arch': 'linux-arm', 'cross_build': True},
    '7.0.2.2_rpi3_debian': {'base_img': 'balenalib/raspberrypi3-debian:stretch', 'epics_host_arch': 'linux-arm', 'cross_build': True},
}
