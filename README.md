# Virtual_Caliper
Use CV2 to Create a virtual camera-to-measuring device. 

# What it does
Displays a real-time distance measurement between two objects, that are determined (in order) by clicks. 

This project is specific to a in-lab set up, so the first click will identify the "tip" and the second will identify the "reflection" of a high-res inkjet. Additionally, with the in-lab setup, the user can guarantee a 5 micron movement of the tip, so the pixels-per-distance calibration is determined based on that assumption. 

# Installation
## Requirements
Python 3

Packages: 
- OpenCV 
- Numpy
- SciPy


# How it works 
RTMeasure.py acts as the main module that uses utils.py as well as a file tracker.py written by Sergio Canu to provide real-time
distance measuring between a tip object and the reflection of that tip through low-level object tracking and user filtering.

# Instructions for use:
## To edit settings
        The top half of the RTMeasure.py file contains settings for the thresholds of the background subtraction and the history length
        As well as the minimum area (in pixels) of objects and the binary threshold value to include for object detection.
        Additionally, the reference distance value is set by default to 5 (assuming the tip can be adjusted exactly 5 microns)
        Finally, the users can change their start and end keys for calibrating the pixels per distance value.
        display_bounding_rects can be set by the user to true if they want to see the bounding rectangles for the tip and
        the reflection. These settings can easily be accessed and changed for different applications of the program.
## To run
        In installation directory:
        run $python3 RTMeasure.py
        
        To use:
            Start by clicking on the tip to display it, followed by the reflection of the tip.
            Once both are detected, press b to store the x,y value for the tip at the beginning of calibration.
            Move the tip 5 microns and then press f to finish calibrating.

            If at all there is a mistake or an error in the display, press r to restart.

            Press q when ready to quit the program. 
