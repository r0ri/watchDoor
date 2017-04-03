"# watchDoor" 

Script for the Raspberry Pi that plays sound snippets when the motion detector,
which is connected to the GPIO pins, detects movement.
The motion detector is connected to GPIO pins

5V:		2<br />
Ground:	6<br />
Input:	15 (activates when motion is detected)

To automatically start this script on boot add 
"python /local/folder/door_script_minimal.py &"
at the end of /etc/rc.local