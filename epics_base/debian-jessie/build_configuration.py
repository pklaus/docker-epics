#!/usr/bin/env python

BUILDS = {
    # tag name:                          template settings
    'debian-jessie':                     {'base_img': 'debian:jessie', 'cross_build': False},
    'resin-raspberry-pi-debian-jessie':  {'base_img': 'resin/raspberry-pi-debian:jessie', 'cross_build': True},
    'resin-raspberrypi3-debian-jessie':  {'base_img': 'resin/raspberrypi3-debian:jessie', 'cross_build': True},
}
