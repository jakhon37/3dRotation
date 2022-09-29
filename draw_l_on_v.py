import os
import numpy as np
import cv2
import json

def draw_polylines(frame, coords_list, RGB):
    coords_list = np.array(coords_list)
    
    frame = cv2.polylines(
        frame, [coords_list],
        isClosed=False, color=(int(RGB[2]), int(RGB[1]), int(RGB[0])),
        thickness=10
    )
    coords_list = np.ndarray.tolist(coords_list)
    return coords_list, frame

def draw_circle(frame, center_coordinate):
    frame = cv2.circle(frame, center_coordinate, radius=5, color=(0,255,250), thickness=15)
    
    


path = 'data/'
path_v = path + 'vid/vid1.mp4'


cap = cv2.VideoCapture(path_v)  # read video 
# cap = cv2.VideoCapture(0)
if (cap.isOpened()== False):   # Check if camera opened successfully
    print("Error opening video stream or file")
    
RGB = np.random.randint(0, 256, size=3)  # 0~255 의 숫자 3개를 랜덤하게 가져옴
RGB = (0, 256, 3)
video_fps = cap.get(cv2.CAP_PROP_FPS),
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
print(f" Frame Per second: {video_fps } \n Total Frames: {total_frames} \n Height: {height} \n Width: {width}")

# Define the codec and create VideoWriter objeact
width, height = 1080, 1920   # assign nnew video width and height 
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # *'mp4v' *'XVID'
out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (width,height)) #(int(cap.get(3)),int(cap.get(4)))) # size (int(cap.get(3)),int(cap.get(4)))

jsonfile = path + "txt/json_file.json"
with open(jsonfile, "r") as f: 
    json_f = json.load(f)
    pr = json_f["parabola"] # list of coordinates in format [[x,y,z],[x,y,z],...]

scale = 13 # scale coordinates to normalize line projectile on video / find it from pose estimation 

cur = 1
cur_m = 20
coords_list =[]
center_coordinates = 536, 1053 # 450, 1300
initaial_pos = 62
while(cap.isOpened()):
    cur_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    ret, frame = cap.read()            
    frame = cv2.flip(frame,0)

    if ret==True:
        frame = frame[0:height, 0:width]   # resize video
        if cur_frame <initaial_pos:
            cord_x, cord_y = int(pr[0][0]*scale+center_coordinates[0]), int(pr[0][1]*(-scale)+center_coordinates[1])
            coords_list.append([cord_x, cord_y] )
            center_coord = cord_x, cord_y
        if cur_frame > initaial_pos and len(pr)>cur:
            cord_x, cord_y = int(pr[cur][0]*scale+center_coordinates[0]), int(pr[cur][1]*(-scale)+center_coordinates[1])
            coords_list.append([cord_x, cord_y] )
            center_coord = cord_x, cord_y
            # cur_m = 35
            cur = int(cur + cur_m)
            cur_m = cur_m/1.002
            print(cur)

        coords_list, frame = draw_polylines(frame, coords_list, RGB)
        image = draw_circle(frame, center_coord)


        out.write(frame)
        sc = 0.4 # rezie ratio for video out display 
        frame = cv2.resize(frame,(int(width*sc), int(height*sc)),fx=0,fy=0, interpolation = cv2.INTER_CUBIC) 
        cv2.imshow('frame',frame)
        img_path = f'{path}img{path_v.split("/")[-1]}'
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        cv2.imwrite((img_path + "/image_{}.jpg".format(cur_frame)), frame)  # Save image localy 

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()