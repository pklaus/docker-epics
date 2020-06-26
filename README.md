
### epics\_docker

This repository contains Dockerfiles to create docker images for:

* A distribution of **epics base**
    * in the folder [`epics_base`](./epics_base/)
    * with pre-built images on Docker Hub: [pklaus/epics\_base][])
* a distribution of many frequently needed EPICS modules named **contApps**
  (counterpart of synApps tailored to the container world)
    * in the folder [`epics_contapps`](./epics_contapps/)
    * with pre-built images on Docker Hub: [pklaus/epics\_contapps][])
* a (**deprecated**) distribution of **synApps**
    * in the folder [`old_images/01/epics_synapps/`](old_images/01/epics_synapps/)
    * with pre-built images on Docker Hub: [pklaus/epics\_contapps][])

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

Enter `CTRL-p CTRL-q` to detach from the shell or `CTRL-d` to quit the IOC.

[pklaus/epics\_base]: https://hub.docker.com/r/pklaus/epics_base/
[pklaus/epics\_contapps]: https://hub.docker.com/r/pklaus/epics_contapps/
[pklaus/epics\_synapps]: https://hub.docker.com/r/pklaus/epics_synapps/
