#!/usr/bin/bash

PROJECTPATH=/home/pi/projects/led3d
NLEDs=$(cat ./src/config.py | grep NLEDs | awk -F'=' '{print $2}' | xargs)
ANGLE=$1

source ./activate

echo "Calibration cycle will start in 10s ..."
sleep 10
echo "Starting calibration cycle for angle = $ANGLE deg at `date`"

for (( i = 0; i < $NLEDs; i++ )); do
  ssh pokke " source ${PROJECTPATH}/activate; \
              cd ${PROJECTPATH}/raspi; \
              sudo ./LED_ON.py $i "
  VALS=$(python3 take_photo.py -a $ANGLE -n $i)
  if (( $(echo $VALS | awk '{print $4}') > 150 )); then
    ssh pokke " source ${PROJECTPATH}/activate; \
                cd ${PROJECTPATH}/raspi; \
                ./pos2db.py $VALS; \
                sudo ./OFF.py "
  else
    ssh pokke " source ${PROJECTPATH}/activate; \
                sudo ${PROJECTPATH}/raspi/OFF.py "
  fi
  
done

echo "Finished at `date`"

