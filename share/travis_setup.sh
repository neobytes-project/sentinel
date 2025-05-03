#!/bin/bash
set -evx

mkdir ~/.neobytes

# safety check
if [ ! -f ~/.neobytes/.neobytes.conf ]; then
  cp share/neobytes.conf.example ~/.neobytes/neobytes.conf
fi
