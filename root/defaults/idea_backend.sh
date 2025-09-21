#!/bin/bash

if [[ -d /config/clwb ]]; then
  idea serverMode /config/clwb
else
  echo "clwb is not mounted :c"
fi

