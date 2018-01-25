#!/bin/bash

set -x
set -e

for repo in epics_base epics_synapps
do

  cd $repo/debian-jessie

  for tag in $(../../docker_template.py list-tags)
  do
    ../../docker_template.py build --tag pklaus/$repo:$tag
  done

  cd -

done
