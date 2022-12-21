#!/usr/bin/bash

PROJECTPATH=/home/pi/projects/led3d

source ./activate
./make_lengthcalib.py

FACTOR=$(cat /tmp/lengthcalib)

ssh pokke """ source ${PROJECTPATH}/activate;
              ${PROJECTPATH}/raspi/lencal2db.py $FACTOR """

rm /tmp/lengthcalib
