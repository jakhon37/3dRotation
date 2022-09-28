def find_start_end_point(angle_l, im3_shape, ball_center):

    # find line start and end points
    im_h , im_w = im3_shape[0] , im3_shape[1] # image hight width
    scale = 0.40 # used to set last y point for line 
    # find x end point 
    b_line = ball_center[1] - im_h*scale
    a_line = math.tan(math.radians(angle_l))*b_line
    if angle_l>0:
        end_point = (int(ball_center[0] -a_line), int(im_h*scale)) # x, y end points 
    else: 
        end_point = (int(ball_center[0] +a_line), int(im_h*scale)) # x, y end points 
    start_p_y = im_h*0.9 # used to set start y point by scaling 
    # start_p_y = (im_h - ball_center[0][1])*scale+ball_center[0][1]
    # find x start point 
    bs_line = start_p_y - ball_center[1]
    as_line = math.tan(math.radians(angle_l))*bs_line
    if angle_l>0:
        start_point = int(ball_center[0] + as_line), int(start_p_y) # x, y start points
    else:
        start_point = int(ball_center[0] - as_line), int(start_p_y) # x, y start points

    return start_point, end_point

