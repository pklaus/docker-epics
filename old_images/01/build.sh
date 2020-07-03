#!/bin/bash -ex

export DOCKER_BUILDKIT=1

for flavour in epics_base/* epics_synapps/*
do
  cd $flavour
  repo=$(dirname $flavour)

  for tag in $(jinja2-render)
  do
    jinja2-render $tag
    docker build --squash --tag pklaus/$repo:$tag .
  done

  cd -

done
