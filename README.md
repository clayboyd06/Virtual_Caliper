# Virtual_Caliper
Use CV2 to Create a virtual camera-to-measuring device. 

RTMeasure.py acts as the main module that uses utils.py as well as a file tracker.py written by Sergio Canu to provide real-time
distance measuring between a tip object and the reflection of that tip through low-level object tracking and user filtering.

Instructions for use:
        The top half of the RTMeasure.py file contains settings for the thresholds of the background subtraction and the history length
        As well as the minimum area (in pixels) of objects and the binary threshold value to include for object detection.
        Additionally, the reference distance value is set by default to 5 (assuming the tip can be adjusted exactly 5 microns)
        Finally, the users can change their start and end keys for calibrating the pixels per distance value.
        display_bounding_rects can be set by the user to true if they want to see the bounding rectangles for the tip and
        the reflection. These settings can easily be accessed and changed for different applications of the program.

        To use:
            Start by clicking on the tip to display it, followed by the reflection of the tip.
            Once both are detected, press b to store the x,y value for the tip at the beginning of calibration.
            Move the tip 5 microns and then press f to finish calibrating.

            If at all there is a mistake or an error in the display, press r to restart.

            Press q when ready to quit the program. 
