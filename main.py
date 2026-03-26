############################
# Import libraries
############################

import cv2
import numpy as np
import time
import HandTrackingModule as htm
from pycaw.pycaw import AudioUtilities

############################
# Camera Settings
############################
wCam , hCam = 640 , 480


############################
# Initialize Variables
############################
previous_time = 0

# Default volume values
vol = 0
volBar = 400
volPer = 0

# Hand distance range
min_length = 30
max_length = 250

############################
# Initialize the hand detector with the detection confidence
############################
detector = htm.handDetector(detectionCon=0.7)


############################
# Initialize Audio Control using pycaw
############################
device = AudioUtilities.GetSpeakers()
volume = device.EndpointVolume

# Get the volume range in dB
volume_range = volume.GetVolumeRange() 
min_volume = volume_range[0]
max_volume = volume_range[1]

############################
# Initialize Camera
############################

# 0--> Turn on the main camera of the computer)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Set the camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH , wCam) # cv2.CAP_PROP_FRAME_WIDTH = 3 --> the video width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT , hCam) # cv2.CAP_PROP_FRAME_HEIGHT = 4 --> the video height

############################
# Main Loop
############################
while True:
    success , img = cap.read()
    
    # check if camera frame is captured
    if not success:
        print("Failed to read from camera ❌")
        continue
    
    # Detect the hand and draw the landmarks
    img = detector.findHands(img)
    
    """
    # The hand consists of 21 landmarks, each landmark has an ID:
    # 0  -> Wrist (base of the hand)
    # 4  -> Thumb tip 
    # 8  -> Index finger tip 
    # 12 -> Middle finger tip
    # 16 -> Ring finger tip
    # 20 -> Pinky finger tip
    """
    
    # Get the position of the landmarks
    LandmarksList = detector.findPosition(img, draw=False)
    
    # Check if the landmarks are detected
    if len(LandmarksList) != 0:
        # Get thumb & index finger positions
        x1, y1 = LandmarksList[4][1], LandmarksList[4][2]
        x2, y2 = LandmarksList[8][1], LandmarksList[8][2]
        
        # Draw a circle on the selected landmarks
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        
        # Draw a line between the two fingers
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        
        # Calculate the distance between the two fingers
        length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        # Map distance to volume range
        vol = np.interp(length, [min_length, max_length], [min_volume, max_volume])
        
        # Clamp volume to valid range
        vol = np.clip(vol, min_volume, max_volume)
        
        # Set system volume based on the calculated volume
        volume.SetMasterVolumeLevel(vol, None)        
        
        
        # Find the center point of the line
        cx , cy = (x1 + x2) // 2 , (y1 + y2) // 2
        # Change color if fingers are very close (mute zone)
        if length < 50:
            cv2.circle(img, (cx, cy), 12, (0, 255, 0), cv2.FILLED)
        else:
            cv2.circle(img, (cx, cy), 12, (255, 0, 255), cv2.FILLED)
    
    ############################
    # Volume Bar + Percentage
    ############################   
    
    volBar = np.interp(vol, [min_volume, max_volume], [400, 150])
    volPer = np.interp(vol, [min_volume, max_volume], [0, 100])
    
    # Draw volume bar
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    
    # Display volume percentage
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
    
    
    ############################
    # FPS Calculation
    ############################
    
    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    
    # Display the FPS on the screen
    cv2.putText(img , f'FPS:{int(fps)}' , (40 , 70) , cv2.FONT_HERSHEY_PLAIN , 3 , (255 , 0 , 0) , 3)
    
    # Show Image
    ############################
    cv2.imshow("Volume Control", img)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

############################
# Release Resources
############################
cap.release()
cv2.destroyAllWindows()
    