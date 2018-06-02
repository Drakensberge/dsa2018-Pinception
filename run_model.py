# run_model.py
from __future__ import print_function

import RPi.GPIO as GPIO
import time
import datetime
import json
import picamera

print('Loading Inception module...')
import inception_predict
print('WE MUST GO DEEPER!')

def timestamp():
    """
    Generate timestamps for the images
    Return:
        Date in the format YYYY-MM-DD-HH-MM-SS
    """
    current_time = datetime.datetime.now()
    timestamp_components = [str(current_time.year),
                            format(current_time.month, '02d'),
                            format(current_time.day, '02d'),
                            format(current_time.hour, '02d'),
                            format(current_time.minute, '02d'),
                            format(current_time.second, '02d')]                 
    return "_".join(timestamp_components)

motion_sensor_pin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(motion_sensor_pin, GPIO.IN)

image_directory = '/home/pi/pictures/'
prediction_directory = '/home/pi/predictions/'

use_motion_capture =  True

#if not use_motion_capture:
camera = picamera.PiCamera()

while True:

    if use_motion_capture:
        if (GPIO.input(motion_sensor_pin)):
            print('Motion detected at ', timestamp())
#            with picamera.PiCamera() as camera:
#                camera.resolution = (1024, 1024)
	    time.sleep(2)
            t = timestamp()
            fname = image_directory + t + '.jpg'
            camera.capture(fname)
            print('saved image', fname)
            topn, predstr = inception_predict.predict_from_local_file(fname, N=5)
            print(predstr)
            with open(prediction_directory+t+'.json','wa') as f:
                json.dump(predstr, f)

    else:
        # Take the jpg image from camera
        print("Capturing")
        filename = '/home/pi/cap.jpg'
        # Show quick preview of what's being captured
        camera.start_preview()
        camera.capture(filename)
        camera.stop_preview()
    
        # Run inception prediction on image
        print("Predicting")
        topn, _ = inception_predict.predict_from_local_file(filename, N=5)
    
        # Print the top N most likely objects in image (default set to 5, change this in the function call above)
        print('INFO:', topn)
