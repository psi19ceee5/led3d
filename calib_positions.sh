#!/usr/bin/bash

PROJECTPATH=/home/pi/projects/led3d
NLEDs=$(cat ./src/config.py | grep NLEDs | awk -F'=' '{print $2}' | xargs)
ANGLE=$1

echo "Calibration cycle will start in 5s ..."
sleep 1
echo "Starting calibration cycle for angle = $ANGLE deg at `date`"

for (( i = 0; i < $NLEDs; i++ )); do
  ssh pokke " source ${PROJECTPATH}/activate; \
              cd ${PROJECTPATH}/raspi; \
              sudo ./LED_ON.py $i "
  VALS=$(python3 take_photo.py -a $ANGLE)
  ssh pokke " source ${PROJECTPATH}/activate; \
              ${PROJECTPATH}/testing/accept_args_for_writing.py $VALS; \
              sudo ${PROJECTPATH}/raspi/OFF.py "
done

echo "Finished at `date`"

