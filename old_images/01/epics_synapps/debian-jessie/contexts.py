#!/usr/bin/env python

CONTEXTS = {
    # tag name:                          template settings
    'debian-jessie':                     {'base_img': 'pklaus/epics_base:debian-jessie', 'cross_build': False},
    'resin-raspberry-pi-debian-jessie':  {'base_img': 'pklaus/epics_base:resin-raspberry-pi-debian-jessie', 'cross_build': True},
    'resin-raspberrypi3-debian-jessie':  {'base_img': 'pklaus/epics_base:resin-raspberrypi3-debian-jessie', 'cross_build': True},
}
