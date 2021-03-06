# ========================================================================
# Start with an intermediate image only for downloading / extracting / ...
# ========================================================================
FROM --platform=$TARGETPLATFORM debian:10-slim AS download-extract
RUN apt-get update && apt-get install -yq wget
WORKDIR /var/cache
RUN wget -q --show-progress https://epics.anl.gov/download/base/base-3.15.6.tar.gz \
 && mkdir /epics/ \
 && tar -xf base-3.15.6.tar.gz -C /epics \
 && rm base-3.15.6.tar.gz

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
EXPOSE 5064-5065 5064-5065/udp
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
RUN ln -s base-3.15.6 base
RUN cd /epics/base && make -j$(nproc)
ENV EPICS_ROOT=/epics
ENV EPICS_BASE=${EPICS_ROOT}/base
ENV EPICS_BASE_BIN=${EPICS_BASE}/bin/${EPICS_HOST_ARCH} \
    EPICS_BASE_LIB=${EPICS_BASE}/lib/${EPICS_HOST_ARCH} \
    LD_LIBRARY_PATH=${EPICS_BASE_LIB}:${LD_LIBRARY_PATH}
ENV PATH=${PATH}:${EPICS_BASE_BIN}
RUN echo -e "#!/bin/sh\necho ${EPICS_HOST_ARCH}" > /epics/base/startup/EpicsHostArch \
 && chmod +x /epics/base/startup/EpicsHostArch

# Example IOC
# ===========

# classic example IOC:
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

WORKDIR /epics
CMD /bin/bash
