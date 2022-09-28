def draw_polylines(frame, coords_list, RGB):
    coords_list = np.array(coords_list)
    
    frame = cv2.polylines(
        frame, [coords_list],
        isClosed=False, color=(int(RGB[2]), int(RGB[1]), int(RGB[0])),
        thickness=10
    )
    
    coords_list = np.ndarray.tolist(coords_list)
    return coords_list, frame

import numpy as np
import cv2
import json
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

coords_list2 =[]
coords_list_cir2 =[]
jsonfile = path + "txt/json_file.json"
# jsonfile = "custom_json.json"

with open(jsonfile, "r") as f: 
    json_f = json.load(f)
    pr = json_f["parabola"]
    for i in (json_f["parabola"]):
        scale = 15
        coords_list2.append([int(i[0]*scale+420), int(i[1]*(-scale)+1300)]) #= [json_f["parabola"], json_f["parabola"]]
    
    for i in range(0, len(json_f["parabola"]), 20):
        scale2 = 20
        coords_list_cir2.append([int(pr[i][2]*scale2+420), int(pr[i][1]*(-scale2)+1300)]) #= [json_f["parabola"], json_f["parabola"]]


coords_list =[]
# coords_list_cir =[]

ts = 1  
cur = 3
cur_m = -1
while(cap.isOpened()):
    cur_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    ts = cur_frame
    ret, frame = cap.read()            
    frame = cv2.flip(frame,0)

    if ret==True:
        frame = frame[0:height, 0:width]   # resize video
        cur2 = 1
        if ts <30:
            coords_list.append([int(0*scale+420), int(0*(-scale)+1300)])

        if ts > 40 and len(pr)>cur:
            coords_list.append([int(pr[cur][0]*scale+420), int(pr[cur][1]*(-scale)+1300)])
            cur_m -1
            cur +=65 + cur_m
#             cur2 = 1
        coords_list, frame = draw_polylines(frame, coords_list, RGB)
        

    #         center_coordinates = coords_list_cir[ts][0],coords_list[ts][1]
        center_coordinates = 450, 1300

        radius = 10
        color = (0,255,0)
        thickness = 15
        image = cv2.circle(frame, center_coordinates, radius, color, thickness)


#         coords_list, frame = draw_polylines(frame, coords_list, RGB)
        # write the flipped frame
        out.write(frame)
        ts += 1
        cur2 +=5
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()