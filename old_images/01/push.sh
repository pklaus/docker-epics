#!/bin/bash

set -x
set -e

for flavour in epics_base/* epics_synapps/*
do
  cd $flavour
  repo=$(dirname $flavour)

  for tag in $(../../docker_template.py list-tags)
  do
      docker push pklaus/$repo:$tag
  done

  cd -
done
