#!/bin/bash
set -evx

mkdir ~/.neobytescore

# safety check
if [ ! -f ~/.neobytescore/.neobytes.conf ]; then
  cp share/neobytes.conf.example ~/.neobytescore/neobytes.conf
fi
