#!/usr/bin/bash

# usage ./calib_positions.sh ANGLE_DEG NLEDS

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
  if (( $(echo $VALS | awk '{print $5}') > 150 )); then
    echo $VALS
    ssh pokke " source ${PROJECTPATH}/activate; \
                cd ${PROJECTPATH}/raspi; \
                ./pos2db.py $VALS; \
                sudo ./OFF.py "
  else
    echo -e "\033[30;103;1m[WARNING]:\033[0m position of led number $i could not be determined." 
    ssh pokke " source ${PROJECTPATH}/activate; \
                sudo ${PROJECTPATH}/raspi/OFF.py "
  fi

done

echo "Finished at `date`"

