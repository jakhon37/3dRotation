import numpy as np
import cv2
path_v = 'data/golf_v.mp4'
cap = cv2.VideoCapture(path_v)  # read video 
# cap = cv2.VideoCapture(0)
if (cap.isOpened()== False):   # Check if camera opened successfully
    print("Error opening video stream or file")

video_fps = cap.get(cv2.CAP_PROP_FPS),
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
print(f" Frame Per second: {video_fps } \n Total Frames: {total_frames} \n Height: {height} \n Width: {width}")

# Define the codec and create VideoWriter object
width, height = 1080, 1920   # assign nnew video width and height 
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # *'mp4v' *'XVID'
out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (width,height)) #(int(cap.get(3)),int(cap.get(4)))) # size (int(cap.get(3)),int(cap.get(4)))

while(cap.isOpened()):
    ret, frame = cap.read()            
    frame = cv2.flip(frame,0)

    if ret==True:
        frame = frame[0:height, 0:width]   # resize video
        # for iii in range(len(frame)):
        frlen = 0
        for iii in range(int(total_frames)):
            frlenn = frlen + 1
        x = 100+iii
        y = 200+(iii)
        center_coordinates = x,y
        radius = 10
        color = (0,255,0)
        thickness = 15
        image = cv2.circle(frame, center_coordinates, radius, color, thickness)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()