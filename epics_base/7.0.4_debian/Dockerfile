# ========================================================================
# Start with an intermediate image only for downloading / extracting / ...
# ========================================================================
FROM --platform=$TARGETPLATFORM debian:10-slim AS download-extract
SHELL ["/bin/bash", "-c"]
RUN apt-get update && apt-get install -yq wget git
WORKDIR /var/cache
RUN wget -q --show-progress https://epics.anl.gov/download/base/base-7.0.4.tar.gz \
 && mkdir /epics/ \
 && tar -xf base-7.0.4.tar.gz -C /epics \
 && rm base-7.0.4.tar.gz

## Adding PCAS library (not part of EPICS 7.x by default anymore)
RUN wget -q --show-progress https://github.com/epics-modules/pcas/archive/v4.13.2.tar.gz \
 && mkdir /epics/base-7.0.4/modules/pcas \
 && tar -xf v4.13.2.tar.gz --strip-components=1 -C /epics/base-7.0.4/modules/pcas/ \
 && echo -e "SUBMODULES += pcas\npcas_DEPEND_DIRS = libcom" > /epics/base-7.0.4/modules/Makefile.local \
 && echo '-include $(TOP)/../RELEASE.$(EPICS_HOST_ARCH).local' >> /epics/base-7.0.4/modules/pcas/configure/RELEASE \
 && rm v4.13.2.tar.gz

# The release base-7.0.4.tar.gz already contains
# https://github.com/epics-base/epics-base/archive/R7.0.4.tar.gz
# and all of the following modules:
# https://github.com/epics-base/pvDataCPP/archive/8.0.2.tar.gz
# https://github.com/epics-base/pva2pva/archive/1.2.3.tar.gz
# https://github.com/epics-base/pvAccessCPP/archive/7.1.1.tar.gz
# https://github.com/epics-base/pvDatabaseCPP/archive/4.5.2.tar.gz
# https://github.com/epics-base/pvaClientCPP/archive/4.7.1.tar.gz
# https://github.com/epics-base/normativeTypesCPP/archive/6.0.1.tar.gz

RUN git clone --single-branch --depth 1 https://github.com/epics-base/exampleCPP.git /exampleCPP \
 && rm -rf /exampleCPP/.git

# ============================
#  Now start the final image
# ============================

# We need to set ENV EPICS_HOST_ARCH according to the $TARGETARCH
# To do so, the following hack was used:
# https://github.com/docker/buildx/issues/157#issuecomment-538048500
FROM --platform=$TARGETPLATFORM debian:10-slim AS base

FROM base AS base-amd64
ENV EPICS_HOST_ARCH=linux-x86_64

FROM base AS base-386
ENV EPICS_HOST_ARCH=linux-x86

FROM base AS base-arm64
ENV EPICS_HOST_ARCH=linux-arm

FROM base AS base-arm
ENV EPICS_HOST_ARCH=linux-arm

# Now finally choose the right base image:
FROM base-$TARGETARCH AS final
SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install --no-install-recommends -yq \
  build-essential \
  ca-certificates \
  curl \
  libreadline-dev \
  telnet \
 && apt-get clean && rm -rf /var/lib/apt/lists/* && rm -rf /var/cache/apt

### add user "scs"
RUN useradd \
      --create-home \
      --home /epics \
      --gid users \
      --groups users \
      --shell /bin/bash \
      scs

# Set user/working directory, copy source files & compile
USER scs
ENV USER=scs
WORKDIR /epics
COPY --from=download-extract --chown=scs:users /epics /epics
RUN ln -s base-7.0.4 base
RUN cd /epics/base && make -j$(nproc)
ENV EPICS_ROOT=/epics
ENV EPICS_BASE=${EPICS_ROOT}/base
ENV EPICS_BASE_BIN=${EPICS_BASE}/bin/${EPICS_HOST_ARCH} \
    EPICS_BASE_LIB=${EPICS_BASE}/lib/${EPICS_HOST_ARCH} \
    LD_LIBRARY_PATH=${EPICS_BASE_LIB}:${LD_LIBRARY_PATH}
ENV PATH=${PATH}:${EPICS_BASE_BIN}
RUN echo -e "#!/bin/sh\necho ${EPICS_HOST_ARCH}" > /epics/base/startup/EpicsHostArch \
 && chmod +x /epics/base/startup/EpicsHostArch

# Example IOCs
# ============

# classic example IOC:
EXPOSE 5064-5065 5064-5065/udp
RUN mkdir -p /epics/iocs/example \
 && cd /epics/iocs/example \
 && makeBaseApp.pl -t example EXAMPLE \
 && make \
 && makeBaseApp.pl -i -t example EXAMPLE \
 && make \
 && chmod +x iocBoot/iocEXAMPLE/st.cmd
# (to set the classic example IOC as default command:)
#WORKDIR /epics/iocs/example/iocBoot/iocEXAMPLE
#CMD ./st.cmd

# EPICS V4 / R7 example IOC:
EXPOSE 5075 5076/udp
COPY --from=download-extract --chown=scs:users /exampleCPP /epics/iocs/exampleCPP
WORKDIR /epics/iocs/exampleCPP
COPY RELEASE.local.exampleCPP configure/RELEASE.local
RUN make -j$(nproc)
RUN cd database/iocBoot/exampleDatabase/ \
 && sed -i "1i#!../../bin/${EPICS_HOST_ARCH}/exampleDatabase\n" st.cmd \
 && echo -e '\ndbl\npvdbl\n' >> st.cmd \
 && chmod +x st.cmd
# (to set the EPICS V4 / R7 exampleCPP IOC as default command:)
#WORKDIR /epics/iocs/exampleCPP/database/iocBoot/exampleDatabase
#CMD ./st.cmd

WORKDIR /epics
CMD /bin/bash
