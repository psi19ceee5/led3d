#!/usr/bin/bash

PROJECTPATH=/home/pi/projects/led3d
NLEDs=$(cat config.py | grep NLEDs | awk -F'=' '{print $2}')
ANGLE=$1

for (( i=0; i<$NLEDs; i++ )); do
  VALS=$(python3 take_photo.py -a $ANGLE)
  ssh pokke "python3 ${PROJECTPATH}/testing/accept_args_for_writing.py $VALS"
done

