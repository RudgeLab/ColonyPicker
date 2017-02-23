# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 13:48:30 2017

@author: Prosimio

this program is to  click and count colonies from agar plates pictures

First:
    - create a 2.7 python environment on anaconda
    - install OpenCV 2.4.X on the environment
      ( i open the terminal on anaconda and put: conda install -c https://conda.binstar.org/menpo opencv)
      (in this page you can find some advice:http://stackoverflow.com/questions/23119413/how-to-install-python-opencv-through-conda)
    - install wxpyhton package on the environment (actually is on the anaconda cluod)

*how to execute:
    python colonyPicker.py --image coloniashoy.tif
    
*i get the base code from here: http://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/
"""

# import the necessary packages

import argparse
import cv2
import ctypes  # An included library with Python install, to display msgs
import wx

# initialize the list of reference points, summary values and groups
refPt = []
counts= []
groups = []

#Define msjBox input window
app = wx.App()
 
frame = wx.Frame(None, -1, 'win.py')
frame.SetDimensions(0,0,200,50)

#

def click_and_mark(event, x, y, flags, param):
    #event: The event that took place (left mouse button pressed, left mouse button released, mouse movement, etc).
    #x: The x-coordinate of the event.
    #y: The y-coordinate of the event.
    #flags: Any relevant flags passed by OpenCV.
    #params: Any extra parameters supplied by OpenCV.
      
    # grab references to the global variables
    global refPt
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append([(x, y)])
        
        # draw a circle on the presed point
        cv2.circle(image, (x,y), 7, (255, 255, 255), 2)
        cv2.imshow("image", image)
       #refPt2 = refPt = [(x+5, y+5)]

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())
imname=args['image'].split('.')[0]

# load the image, clone it, and setup the mouse callback function
image = cv2.imread(args["image"])
clone = image.copy()
cv2.namedWindow("image",cv2.WINDOW_NORMAL)
cv2.setMouseCallback("image", click_and_mark)

# keep looping until the 'q' key is pressed
ctypes.windll.user32.MessageBoxA(0, 'Press "c" to create a new group \nPress "e" to exit' , "Instructions!", 0)
aux=True #to define the first group name

while True:
    global counts
	# display the image and wait for a keypress
    cv2.imshow("image", image)
    key = cv2.waitKey(1) & 0xFF
    
    #ask for the first group name
    if aux:
        aux = False
        dlg = wx.TextEntryDialog(frame, 'Enter group name','Text Entry')
        dlg.SetValue("")
        if dlg.ShowModal() == wx.ID_OK:
            ctypes.windll.user32.MessageBoxA(0, "Group "+str(dlg.GetValue())+" started", "Chan!", 0)
            groups.append(dlg.GetValue())
        dlg.Destroy()
        
	# if the 'c' key is pressed, start a new group
    if key == ord("c"):
        # Create text input
        dlg = wx.TextEntryDialog(frame, 'Enter group name','Text Entry')
        dlg.SetValue("")
        if dlg.ShowModal() == wx.ID_OK:
            ctypes.windll.user32.MessageBoxA(0, "Group "+str(dlg.GetValue())+" started", "Chan!", 0)
            groups.append(dlg.GetValue())
        dlg.Destroy()
        
        
        counts.append(refPt)   #save the counted category on counts
        refPt=[]   #Empty the reference list
		#image = clone.copy()

	# if the 'e' key is pressed, break from the loop
    elif key == ord("e"):
        ctypes.windll.user32.MessageBoxA(0, "See you  :)!", "Chan!", 0)
        counts.append(refPt)   #save the counted category on counts
        refPt=[]   #Empty the reference list        
        break

#count the picked colonies of each category
#i=0  #counter
resume=''
for i in range(len(counts)):
    #print('Group '+ str(groups[i]) + ' : '+str(len(counts[i])) + ' picked colonies')
    resume+=('Group '+ str(groups[i]) + ' : '+str(len(counts[i])) + ' picked colonies'+'\n')
    #i+=1
#display the results
print(resume)
ctypes.windll.user32.MessageBoxA(0, resume, "Result!", 0)
#save a copy of the image with the marks
cv2.imwrite('R_'+imname+'.png',image)

# close all open windows
cv2.destroyAllWindows()