# contApps - porting EPICS synApps to the container world

*Pre-built Docker images on Docker Hub: [/r/pklaus/epics\_contapps][]!*

This project - contApps - is an effort to bring the synApps bundle
of EPICS modules to the container (Docker, podman) world.

The individual modules are compiled in individual RUN statements in this image,
as opposed to being compiled in a single monolithic shell script or `make` call.

The final Dockerfile is created from the Jinja2 template file `Dockerfile.jinja2`
with the help of the tool [jinja2-render](https://pypi.org/project/jinja2-render/)
using one of the build contexts loaded from the configuration file `contexts.py`.

*BTW: The script [`assemble_synApps.sh` script][] served as the first source
of information when putting together the list of EPICS modules for this project.*

[/r/pklaus/epics\_contapps]: https://hub.docker.com/r/pklaus/epics_contapps
[`assemble_synApps.sh` script]: https://github.com/EPICS-synApps/support/blob/master/assemble_synApps.sh
