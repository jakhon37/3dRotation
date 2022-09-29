import json
import math
import cv2
import os 
# file = "./data/res/alphapose-results.json" #./data/txt/alphapose-results.json"
# path = './data/res/vis/'

def find_s_e_points(file):
        
    end_pointls = []
    start_pointls = []
    listt = []
    with open(file, "r") as f: 
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


