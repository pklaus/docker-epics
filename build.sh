#!/bin/bash

set -x
set -e

export PYTHONDONTWRITEBYTECODE=1

for repo in epics_base epics_synapps
do

  cd $repo/debian-jessie

  for tag in $(../../docker_template.py list-tags)
  do
    ../../docker_template.py build --squash --tag pklaus/$repo:$tag
  done

  cd -

done
