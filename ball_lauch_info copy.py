import random
from PIL import Image, ImageDraw, ImageFont


def draw_line(im, start, end):
    x1,y1,x2,y2 = start[0], start[1], end[0], end[1]
    im1 = ImageDraw.Draw(im)
    im1.line((x1,y1,x2,y2), fill=(255, 255, 255, 128), width=1 )
    return im #out

def draw_rect(im, start, end, op):
    x1,y1,x2,y2 = start[0], start[1], end[0], end[1]
    im2 = Image.new("RGBA", im.size, (255, 255, 255, 0))
    im1 = ImageDraw.Draw(im2)
    im1.rectangle(((x1,y1),(x2,y2)), outline = (55, 55, 55, 0), fill=(0, 0, 20, op), width=10 )
    im2 = Image.alpha_composite(im, im2)
    return im2

def draw_arc(im, start_an, end_an, shape):
    # shape = [(40, 40), (145, 145)] start = 45, end = 135
    x1,y1,x2,y2 = start_an[0], start_an[1], end_an[0], end_an[1]
    im_copy = Image.new("RGBA", im.size, (255, 255, 255, 0))
    im = ImageDraw.Draw(im_copy)
    im.arc(shape, start_an, end_an, fill ="pink", width=200)
    out = Image.alpha_composite(im, im_copy)
    return out

def draw_txt(im, fnt_path, point, word, color, size, ops):
    # fnt_path = "/Users/jakhon37/pyProjects/3dRotation/data/res/font/Amble-Bold.ttf"
    fnt = ImageFont.truetype(fnt_path, size)
    x,y = point[0], point[1]
    im_copy = Image.new("RGBA", im.size, (255, 255, 255, 0))
    im1 = ImageDraw.Draw(im_copy)
    im1.text((x, y), word, font=fnt, fill=(color[0],color[1], color[1], ops))
    out = Image.alpha_composite(im, im_copy)
    return out

def put_img(im1, im2):
    im1.paste(im2, (37, 30), im2)
    return im1



def main_draw(im, im2, distance, velocity, angle, carry_d, t_time, spin_rpm, height_tr, type_tr, angle_dif):
#    im = Image.fromarray(im).convert("RGBA")
#    im2 = Image.fromarray(im2).convert("RGBA")
    height_tr = int(height_tr)
    velocity   = int(velocity)
    t_time   = round(t_time, 2)
    angle   = int(angle)
    carry_d   = int(carry_d)
    spin_rpm = str(int(spin_rpm))
    fnt = ("data/res/font/Amble-Bold.ttf")
    w, h = im.size                    #  image_5.jpg
                  #  image_5.jpg
    # w, h = 2080, 2920             #  image_5.jpg
    w, h = 1080, 1920             #  image_5.jpg
    ration = 1080/w
    # distance, velocity, angel = ["math_out"]["solutions"]["solution2_1"]["ddistance"], json_data["math_out"]["solutions"]["solution2_1"]["velocity"], json_data["math_out"]["solutions"]["solution2_1"]["angle"]
    
    ####  rectangle  ####(5, h-860)  (305, 5)
    start, end = (w*0.00463, h*0.552), (w*0.2824, h*0.0026)
    im = draw_rect(im, start, end, op=180)

    ####  put img  ####
    im = put_img(im, im2)

    ####  line  ####
    start, end = (w*0.0324, h*0.063), (w*0.255, h*0.063) # first top line  35, h-1800 (275, h-1800)
    im = draw_line(im, start, end)
    #### below the yard
    start, end = (w*0.0324, h*0.167), (w*0.255, h*0.167) # (w*0.0324, h-1600), (w*0.255, h-1600)
    im = draw_line(im, start, end)
    ### between carry / avg total
    start, end = (w*0.144, h*0.232), (w*0.144, h*0.169)   # (155, h-1475), (155, h-1595)
    im = draw_line(im, start, end)
    ### below carry / time
    start, end = (w*0.0324, h*0.234), (w*0.255, h*0.234)   # (w*0.0324, h-1470), (w*0.255, h-1470)
    im = draw_line(im, start, end)

    #### below the M/S
    start, end = (w*0.0324, h*0.339), (w*0.255, h*0.339) # (w*0.0324, h-1270), (w*0.255, h-1270)
    im = draw_line(im, start, end)
    ### between ANGEL / avg BACKSPIN
    start, end = (w*0.144, h*0.404), (w*0.144, h*0.341)  # (w*0.144, h-1145), (w*0.144, h-1265)
    im = draw_line(im, start, end)
    ### anle / spin 
    start, end = (w*0.0324, h*0.41), (w*0.255, h*0.41) # (w*0.0324, h-1140), (w*0.255, h-1140)
    im = draw_line(im, start, end)
    ### between BACK/UP SPIN / SIDE SPIN 
    start, end = (w*0.144, h*0.477), (w*0.144, h*0.409)   # (w*0.144, h-1005), (w*0.144, h-1135)
    im = draw_line(im, start, end)
    ### below the TIME
    start, end = (w*0.0324, h*0.482), (w*0.255, h*0.482) # (w*0.0324, h-995), (w*0.255, h-995)
    im = draw_line(im, start, end)
    
    ####  put txt  ####
    #### distance value 
    distance = int(carry_d * 1.09361)  # convert to yard from meter 
    if len(str(distance)) > 2:
        point = (w*0.042, h*0.073) # (45, h-1780)
    elif len(str(distance )) == 2:
        point = (w*0.074, h*0.073)
    elif len(str(distance )) <2:
        point = (w*0.111, h*0.073)
    point2, word, color, size, ops = (w*0.042, h*0.073), f'{distance}', (255, 255, 255), 120, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    #### total distance 
    distance = 'DISTANCE'
    point, word, color, size, ops = (w*0.102, h*0.0677), f'{distance}', (26, 198, 50), 20, 255 # (110, h-1790)
    im = draw_txt(im, fnt, point, word, color, size, ops)
    #### yards
    distance = 'YARDS'
    point, word, color, size, ops = (w*0.093, h*0.14), f'{distance}', (255, 255, 255), 35, 255 #  (100, h-1650),
    im = draw_txt(im, fnt, point, word, color, size, ops)
    
    #### velocity 
    distance = 'VELOCITY' 
    point, word, color, size, ops = (w*0.0435, h*0.172), f'{distance}', (26, 198, 50), 20, 255 # (47, h-1590)
    im = draw_txt(im, fnt, point, word, color, size, ops)
        ####  VELOCITY value
    distance = int(velocity * 2.23694 )# convert to mph  grom m/s
    if len(str(distance)) > 2:
        point = (w*0.037, h*0.185)
    elif len(str(distance )) == 2:
        point = (w*0.051, h*0.185)
    elif len(str(distance )) < 2:
        point = (w*0.0694, h*0.185)
    point2, word, color, size, ops = (w*0.0435, h-1555), f'{distance}', (255, 255, 255), 60, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    #### velocity  indicator
    distance = 'MPH'
    point, word, color, size, ops = (w*0.065, h*0.219), f'{distance}', (255, 255, 255), 20, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    
    
    ####  height 
    distance = 'APEX'
    point, word, color, size, ops = (w*0.176, h*0.172), f'{distance}', (26, 198, 50), 20, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    ####   apex height 
    distance =  int(height_tr * 3.28084) # convert to feet from meter 
    if len(str(distance)) > 1:
        point = (w*0.1694, h*0.185)
    elif len(str(distance )) <=1:
        point = (w*0.1824, h*0.185)
    point2, word, color, size, ops = (193, h-1550), f'{distance}', (255, 255, 255), 60, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    #### apex  indicator
    distance = 'FEET'
    point, word, color, size, ops = (w*0.18, h*0.219), f'{distance}', (255, 255, 255), 20, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    
    ####  TOTAL TIME 
    distance = 'TOTAL TIME'
    point, word, color, size, ops = (w*0.094, h*0.24), f'{distance}', (26, 198, 50), 20, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    ####  TOTAL TIME 
    distance = t_time
    if len(str(velocity)) >= 2:
        point = (w*0.046, h*0.245)
    elif len(str(velocity)) < 2:
        point = (w*0.116, h*0.245)
    word, color, size, ops = f'{distance}', (255, 255, 255), 100, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    #### total dime indicator
    distance = 'SEC'
    point, word, color, size, ops = (w*0.118, h*0.3), f'{distance}', (255, 255, 255), 35, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    
    #### laUnch angle 
    distance = 'ANGLE'
    point, word, color, size, ops = (w*0.053, h*0.349), f'{distance}', (26, 198, 50), 20, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    #### launch angle value
    distance = angle
    if len(str(distance)) > 1:
        point = (w*0.049, h*0.365)
    elif len(str(distance)) <= 1:
        point = (w*0.063, h*0.365)            # {"∠"}  {"°"}
    point2, word, color, size, ops = (w*0.049, h*0.365), f'{distance}{"°"}', (255, 255, 255), 60, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    
    #### DIRECTION angle 
    distance = 'DIRECTION'
    point, word, color, size, ops = (w*0.16, h*0.349), f'{distance}', (26, 198, 50), 20, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    ####  direction angle value
    distance = int(angle_dif)
    # if distance ==0:
    #     point_w, word_w = (170, h-1220),  f'--'
    #     point, word = (220, h-1205),  f'{distance}{"°"}'
    direct_l, direct_r, direct_st = 'L', 'R', 'SR'
    if distance >0:
        point_w, word_w = (w*0.157, h*0.365),  f'{direct_r}'
        point, word = (w*0.2, h*0.373),  f'{distance}{"°"}'
    if distance <0:
        point_w, word_w = (w*0.157, h*0.365),  f'{direct_l}'
        point, word = (w*0.2, h*0.373),  f'{abs(distance)}{"°"}'
    if distance == 0:
        point_w, word_w = (w*0.155, h*0.365),  f'{direct_st}'
        point, word = (w*0.22, h-h*0.373),  f'{distance}{"°"}'
    # if len(str(angle_dif))==3:
    #     print(len(str(angle_dif)))
        # word = abs(angle_dif)
       # word = angle_dif

    size_n, word2, color, size, ops = 43, f'{distance}{"°"}', (255, 255, 255), 60, 255
    im = draw_txt(im, fnt, point_w, word_w, color, size, ops) # direction 
    im = draw_txt(im, fnt, point, word, color, size_n, ops) # angle num
    
       #### angle 
    distance = 'BACK SPIN'
    point, word, color, size, ops = (w*0.037, h*0.41), f'{distance}', (26, 198, 50), 20, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
        ####  back spin value
    distance = spin_rpm[0]
    if len(str(spin_rpm)) > 1:
        point = (w*0.03, h*0.42)
    elif len(str(spin_rpm)) <= 1:
        point = (w*0.063, h*0.42)
    point2, word, color, size, ops = (w*0.049, h*0.427), f'{distance}', (255, 255, 255), 60, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)    
    # spin reamining little 
    distance = (f',{spin_rpm[1:]}')
    if len(str(spin_rpm[1:])) > 1:
        distance = (f',{spin_rpm[1:]}')
        point = (w*0.058, h*0.43)
    elif len(str(spin_rpm[1:])) <= 1:
        distance = (f' ')
    word, color, size, ops = f'{distance}', (255, 255, 255), 40, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    #### backspin indicator 
    distance = 'RPM'
    point, word, color, size, ops = (w*0.058, h*0.457), f'{distance}', (255, 255, 255), 25, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    
    #### side spin 
    distance = 'SIDE SPIN'
    point, word, color, size, ops = (w*0.16, h*0.41), f'{distance}', (26, 198, 50), 20, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    ####  side spin value
    # sp = [1, 3, 5, 8, 10, 13, 15, 18, 20, 22, 24,26]
    # in_nnum = angle_dif
    # list_in, q_range = sp, 10, 

    # n_nam = normalize_single_nnum(list_in, q_range, in_nnum)
    # print(n_nam)
    # distance = norml_vel(n_vel=in_nnum, prcnt=n_nam)
    # print(distance)
    # spin_rpm = int(angle_dif*velocity)#*0.1
    spin_rpm = int(angle_dif*100)#*0.1
    distance = spin_rpm#[0]
    # print('side spin direction ', distance)
    if spin_rpm > 950:
        distance = random.randint(900, 960) # 961
        
    # spin_rpm = str(round(int(spin_rpm)*0.3, 3)).split(".")[0]
    direct_l, direct_r, direct_st = 'L', 'R', 'SR'
    if distance >0:
        point_w, word_w = (w*0.157, h*0.423),  f'{direct_r}'
        point, word = (w*0.199, h*0.43),  f'{distance}'
    if distance <0:
        point_w, word_w = (w*0.157, h*0.423),  f'{direct_l}'
        point, word = (w*0.194, h*0.43),  f'{abs(distance)}'
    if distance == 0:
        point_w, word_w = (w*0.155, h*0.423),  f'{direct_st}'
        point, word = (w*0.22, h*0.43),  f'{distance}'
    # if len(str(angle_dif))==3:
    #     print(len(str(angle_dif)))
        
    size_nn, word2, color, size, ops = 43, f'{distance}', (255, 255, 255), 60, 255
    im = draw_txt(im, fnt, point_w, word_w, color, size, ops)    
    im = draw_txt(im, fnt, point, word, color, size_nn, ops)    


    #### side spin indicator 
    distance = 'RPM'
    point, word, color, size, ops = (w*0.18, h*0.457), f'{distance}', (255, 255, 255), 25, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)

    ####  type 
    distance = 'TYPE'
    point, word, color, size, ops = (w*0.12, h*0.484), f'{distance}', (26, 198, 50), 20, 255
    im = draw_txt(im, fnt, point, word, color, size, ops)
    ####  type 
    distance = type_tr
    point, word, color, size, ops = (w*0.0324, h*0.49), f'{distance}', (255, 255, 255), 70, 255
    # if "." in distance:
    #     point = (35, h-975)
    if len(distance) < 5:
        point = (w*0.083, h*0.49)
    elif len(distance) == 5:
        point = (w*0.074, h*0.49)
    elif len(distance) > 5:
        point = (w*0.042, h*0.49)
        
    # elif "slice" in distance:
    #     point = (80, h-975)
    # elif "stright" in distance:
    #     point = (w*0.042, h-975)
    # elif "hook" in distance:
    #     point = (70, h-975)
    im = draw_txt(im, fnt, point, word, color, size, ops)
    
    im.show()
#    im = numpy.array(im) 
    return im    

if __name__ =="__main__":
    im = Image.open("data/res/im2_test.jpg").convert("RGBA")
    im2 = Image.open("data/res/watermark/ci.png").convert("RGBA")
   # main_draw(im, im2, distance=0, velocity=0, angle=0, carry_d = 0, t_time = 0 , spin_rpm= 0, height_tr = 0, type_tr= "none")
    main_draw(im, im2, distance=129, velocity=78, angle=20, carry_d = 121, t_time = 4.23 , spin_rpm= 3200, height_tr = 34, type_tr= "stright", angle_dif = 7.3)


