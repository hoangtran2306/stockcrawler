#!/bin/bash

# error & uninitialised variable checking
set -eu

LOGDIR='logs'
LOGEXT="log"

declare -a items=('market' 'hose' 'hnx' 'hnx30' 'vn30' 'upcom')
declare -a r=()

echo "start scripts..."
for item in ${items[@]}; do
    echo "--"$item
    nohup python vndirect.py ${item} 2>&1 >> $LOGDIR/vnds-${item}.$LOGEXT &
done
echo "done"