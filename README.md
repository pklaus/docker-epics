
### epics\_docker

This repository contains Dockerfiles to create docker images for a
distribution of epics base as well as the synApps modules collection.

See the following repositories on the Docker hub:

* [pklaus/epics\_base](https://hub.docker.com/r/pklaus/epics_base/)
* [pklaus/epics\_synapps](https://hub.docker.com/r/pklaus/epics_synapps/)

#### epics\_base

The epics\_base image contains a the EPICS base installation.
It also comes with a ready-to-use example IOC, which can be handy for
quick testing.

The following example makes use of an environment variable `TAG`.
Set it according to the Docker image tag you want to use:

    export TAG=debian-jessie

To start the example IOC in background (-d), run:

    docker run \
      -d -i -t \
      --rm \
      -p 5064-5065:5064-5065 \
      -p 5064-5065:5064-5065/udp \
      -w /epics/iocs/example/iocBoot/iocEXAMPLE \
      pklaus/epics_base:$TAG \
      ./st.cmd

To attach to the IOC later on, you may run

    docker attach $(docker ps -q)

Enter `^d` (Ctrl-d) to quit.
