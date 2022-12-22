#!/usr/bin/bash

PROJECTPATH=/home/pi/projects/led3d

echo "Calibration picture will be taken in 10 s."
sleep 10

source ./activate
./make_lengthcalib.py

FACTOR=$(cat /tmp/lengthcalib)

ssh pokke "source ${PROJECTPATH}/activate; \
              ${PROJECTPATH}/raspi/lencal2db.py $FACTOR"

rm /tmp/lengthcalib
