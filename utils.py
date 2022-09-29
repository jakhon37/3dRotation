import json
import math
import cv2
import os 






    

def draw_guide_line_points(pose_info):
    end_pointls = []
    start_pointls = []
    listt = []
    with open(pose_info, "r") as f: 
        json_f = json.load(f)

    for idx, i in enumerate(json_f):
        im3_path = path + i["image_id"]
        im3 = cv2.imread(im3_path)
        im3_shape = im3.shape
        ball_center = i["ball_center"]
        # pose infos 
        # person center: calculate middle x point between right and left ankles
        av_ank_point = abs(i["keypoints"][48] - i["keypoints"][45]) / 2 + min(i["keypoints"][45],i["keypoints"][48])
        # calculate distance between right knee and ankle for ratio
        difx = abs(i["keypoints"][42] - i["keypoints"][48]) # kneeX - ankleX 
        dify = abs(i["keypoints"][43] - i["keypoints"][49]) # kneeY - ankleY 
        dif_c = math.sqrt(difx**2+dify**2)
        org = 100
        ratio = org/dif_c
        # real size by ratio 
        toe_difx = (i["keypoints"][60] - i["keypoints"][63])
        real_toe_difx = toe_difx * ratio
        # find angle to rotate centeral line
        angle_l = 25*(35-real_toe_difx)/51
        print('angle found: ',angle_l, 'with dif value ', real_toe_difx)
        # find line start and end points
        im_h , im_w = im3_shape[0] , im3_shape[1] # image hight width
        scale1 = 0.5#0.384 # used to set last y point for line 
        scale = dif_c
        listt.append(scale)
        # find x end point 
        y_point = i["keypoints"][52] #(ball_center[1]*scale1-(ball_center[1]*scale))*1.5
        b_line = ball_center[1] - y_point #  im_h*scale
        if angle_l>0:
            a_line = math.tan(math.radians(angle_l))*b_line
            end_point = int(ball_center[0] -a_line), int(y_point) # x, y end points 
        else: 
            a_line = math.tan(math.radians(-angle_l))*b_line
            end_point = int(ball_center[0] +a_line), int(y_point) # x, y end points 
        end_pointls.append(end_point)
        start_p_y = im_h*0.9 # used to set start y point by scaling 
        # start_p_y = (im_h - ball_center[0][1])*scale+ball_center[0][1]
        # find x start point 
        bs_line = start_p_y - ball_center[1]
        if angle_l>0:
            as_line = math.tan(math.radians(angle_l))*bs_line
            start_point = int(ball_center[0] + as_line), int(start_p_y) # x, y start points
        else:
            as_line = math.tan(math.radians(-angle_l))*bs_line
            start_point = int(ball_center[0] - as_line), int(start_p_y) # x, y start points
        start_point = ball_center# = [536, 1054]
        start_pointls.append(start_point)
            
    lst = []
    for idx, i in enumerate(json_f):
        Q, xi, x = 10, listt[idx], listt
        zi = (xi - min(x)) / (max(x) - min(x)) * Q
        lst.append(zi)
        end_pointl = end_pointls[idx][0], int(end_pointls[idx][1]+end_pointls[idx][1]*zi/100)
        
    return start_pointls[idx], end_pointl



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
    
    
def draw_tr_on_video(path_v, path_json):
    
    import os
    import numpy as np
    import cv2
    import json
    # path = 'data/'
    # path_v = path + 'vid/vid1.mp4'


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

    # jsonfile = path + "txt/json_file1.json"
    # jsonfile = "json_file.json"
    with open(path_json, "r") as f: 
        json_f = json.load(f)
        pr = json_f["parabola"] # list of coordinates in format [[x,y,z],[x,y,z],...]

    scale = 15 # scale coordinates to normalize line projectile on video / find it from pose estimation 

    cur = 1
    cur_n = 10
    cur_m = 1
    coords_list =[]
    center_coordinates = 536, 1053 # 450, 1300
    initaial_pos = 60
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
                if cur_n>cur_m:
                    cur_n = 50
                cur = abs(int(cur + cur_m+cur_n))
                cur_m = cur_m/1.025
                cur_n = cur_n*1.01
    #             print(cur)

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

