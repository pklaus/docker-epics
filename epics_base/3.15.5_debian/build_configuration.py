#!/usr/bin/env python

BUILDS = {
    # tag name:           template settings
    '3.15.5_debian':      {'base_img': 'debian:stretch', 'epics_host_arch': 'linux-x86_64', 'cross_build': False},
    '3.15.5_rpi_debian':  {'base_img': 'balenalib/raspberry-pi-debian:stretch', 'epics_host_arch': 'linux-arm', 'cross_build': True},
    '3.15.5_rpi3_debian': {'base_img': 'balenalib/raspberrypi3-debian:stretch', 'epics_host_arch': 'linux-arm', 'cross_build': True},
}
