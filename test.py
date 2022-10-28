from ball_lauch_info import main_draw
from PIL import Image, ImageDraw, ImageFont


if __name__ =="__main__":
    im = Image.open("data/res/im2_test.jpg").convert("RGBA")
    im2 = Image.open("data/res/watermark/ci.png").convert("RGBA")
    # main_draw(im, im2, distance=0, velocity=0, angle=0, carry_d = 0, t_time = 0 , spin_rpm= 0, height_tr = 0, type_tr= " -------- ")
    main_draw(im, im2, distance=129, velocity=78, angle=20, carry_d = 121, t_time = 4.23 , spin_rpm= 3200, height_tr = 14, type_tr= "slice", angle_dif = 7.3)

