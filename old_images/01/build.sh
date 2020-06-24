#!/bin/bash

set -x
set -e

export PYTHONDONTWRITEBYTECODE=1

for flavour in epics_base/* epics_synapps/*
do
  cd $flavour
  repo=$(dirname $flavour)

  for tag in $(../../docker_template.py list-tags)
  do
    ../../docker_template.py build --squash --tag pklaus/$repo:$tag
  done

  cd -

done
