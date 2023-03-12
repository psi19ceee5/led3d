# Scripts for 3D LED Christmas tree decoration.

## prerequisites

### requirements:
 - Python >3.7 
 - portaudio19-dev (for portaudio.h header)

### python packages:

 - numpy
 - scipy
 - opencv-python
 - board (only on raspi)
 - neopixel (only on raspi)
 
(for convenience:)

 - (calibration system) pip install numpy scipy opencv-python
 - (raspi) pip install numpy scipy opencv-python board neopixel
 
### hardware:

 - raspberry pi (model 3B+ or higher recommended --  didn't yet try another model, though)
 - RGB LED chain WS2811, 5V (e.g. https://www.amazon.de/dp/B01NCAG8KV/ref=emc_bcc_2_i)
 - A power supply (PSU) that can handle the amount of LEDs you want to control (P = #LEDs X 3W), e.g. for 10 x 50 LEDs = 500 LEDs your PSU needs to provide at least P = 1.5kW.
 - A laptop, PC (or another raspi) with a webcam attached as calibration-machine.
 
## usage

### calibration procedure

1. **setup** Make sure you have a remote (ssh) connection to your raspberry pi. The calibration machine itself also needs an ssh connection to the raspi. A remote connection to the calibration machine is useful, but not necessary.
2. Connect your LED chain to the GPIO header of your raspi like shown in the following sketch for the GPIO configuration of model 3B+:  

  *[I should add a picture here someday]*
  
3. Distribute the LEDs on your christmas tree (or whatever object you want to decorate). Also attach the raspberry to the tree, since the tree has to be rotated during calibration and the LEDs must not alter their position relative to each other.
4. Make sure that the tree can be rotated about 360° without any cables limiting the rotation angle.
5. **position calibration** Bring the webcam of the calibration system in position. The ideal position is such, that the rotation axis (the trunk) is exactly vertical in the middle of the picture and all LEDs are contained within the picture under every rotation angle. The distance between camera and tree should be chosen such, that the tree is as large as possible on the picture. However, depending on the opening angle of your camera you might want to keep a certain distance to avoid perspective distortion (this effect could in principle be corrected for, but it hasn't been done yet). Also, make sure that there are no reflecting surfaces within the picture.
6. Turn off the light in the room (the darker the better) and start the first calibration cycle with 

  ```./calib_positions.py ANGLE NLEDS```

  on the calibration machine. Here, ```ANGLE``` is the rotation angle (in degree) between the original and the current orientation of the tree (for the first calibration cycle, you want to set this to ```0``` probably) and ```NLEDS``` is the total number of LEDs on your chain. If you start the script directly on the calibration machine and not in a remote-shell, you will have enough time to get out of the picture/room, since the calibration start is delayed by 10s. Now every LED is turned on and off, one by one. This might take a long time, depending on the number of LEDs and the responsiveness of your camera.
7. Once the calibration cycle is complete (good luck checking the execution status if you didn't start the calibration in a remote shell!), rotate the Tree around a certain ```ANGLE``` and repeat the previous step. Be careful not to shift the rotation axis relative to the camera! It should always be in the center of the image.
8. Repeat steps 6 and 7 as often as you like. I recommend making at least 3 calibrations runs with ```ANGLE```s 0°, 120° and 240°. Almost perfect results could be achieved with 4 runs (0°, 90°, 180° and 270°). But nothing keeps you from making more measurements with arbitrary angles.
9. **length calibration** Finally, an absolute length calibration has to be made. For this, turn on the lights and run

  ```./calib_length.py ```
  
 on the calibration machine (either directly or with X11-forwarding enabled). You have now 10s to position an object of known length (e.g. a folding rule -- the longer the better) perpendicular to the optical axis of the camera at the distance of the tree (log). A single picture will be taken and you have to click on two positions with known distance in the picture. Next, either close the window or wait until it closes automatically and enter the separation of the two positions in the real world (in meter). Press any key to finish the calibration.
 
10. **post processing calibration** On your raspberry pi, run 

  ```cd raspi && ./3dcoord2db.py && ./correction.py```
  
  Now, the calibration is complete and a complete 3d-model of your Christmas tree should exist in
  your database (```db/calibinfo.sql```).

11. Check the minimum and maximum values along the x, y and z axis (I recommend doing this with blender as described below) and enter them in ```src/config.py``` together with the total number of LEDs. Since this step is super annoying and redundant I have to get it done automatically someday..

12. **running programs** The different programs defined in the ```programs``` folder can be run (on raspi) with

  ```programs/run_on_pi.py PROGRAM```
  
  with PROGRAM being the program name without the .py extension (e.g. ```bottom_up_wave```).
13. Thats it for now. If you want to stop the program and turn all lights off, run (on raspi)

  ```raspi/OFF.py ```
   
### running with blender:

You can load your tree model into blender and run a simulation of a program. For this to work you have to run blender (tested for version 3.4.1) and load the script ```programs/run_on_blender.py``` in the scripting panel. Choose the program you want to simulate by importing it (and commenting out all other program imports) and run the script.
It might be convenient to run blender with the system python:

  ```PYTHONPATH=$(which python) blender --python-use-system-env```

if additional packages (like scipy, etc) are needed by the respective program.


## TODO
- A global configuration file for user config (add item in usage instruction)
- Automatic writing of config.py (change text in usage instruction)
- Automate running a sequence of programs with fixed time each (add item in usage instruction?)
- more programs (this is always a to-do ;))

## NICE2HAVES
- perspective distortion correction (change text in usage instructions)
- background-subtraction in calibration step
