
### epics\_docker

This repository contains the source files (Dockerfiles, ...) to create the images:

* [pklaus/epics\_base][] on Docker Hub
    * **EPICS Base** 3.x / 7.x in a Docker container
    * source in folder [`./epics_base`](./epics_base)
* [pklaus/epics\_contapps][] on Docker Hub
    * **contApps**: a distribution of many frequently needed EPICS modules
      (a counterpart of synApps tailored to the container world)
    * source in folder [`./epics_contapps`](./epics_contapps)
* [pklaus/epics\_synapps][] on Docker Hub (*deprecated!*)
    * **synApps**, a common distribution of EPICS modules
    * now moved to the subfolder [`./old_images/01/epics_synapps`](./old_images/01/epics_synapps)

#### epics\_base

The epics\_base image contains a the EPICS base installation.
It also comes with a ready-to-use example IOC, which can be handy for
quick testing.

To start the example IOC in background (-d), run:

    docker run \
      -d -i -t \
      --rm \
      -p 5064-5065:5064-5065 \
      -p 5064-5065:5064-5065/udp \
      -w /epics/iocs/example/iocBoot/iocEXAMPLE \
      pklaus/epics_base:7.0.4_debian \
      ./st.cmd

To attach to the IOC shell, run:

    docker attach $(docker ps -q)

Enter <kbd>Ctrl + p</kbd> <kbd>Ctrl + q</kbd> to detach from the shell or <kbd>Ctrl + d</kbd> to quit the IOC.

[pklaus/epics\_base]: https://hub.docker.com/r/pklaus/epics_base/
[pklaus/epics\_contapps]: https://hub.docker.com/r/pklaus/epics_contapps/
[pklaus/epics\_synapps]: https://hub.docker.com/r/pklaus/epics_synapps/
