import pygame as pg
import sys

pg.init()

# 1. Screen setup
screen = pg.display.set_mode((800, 600))

# 2. Load images
img1 = pg.image.load("images/flower1.png")
img2 = pg.image.load("images/flower2.png")
next_img = pg.image.load("images/nextbtn.png")

# 3. Global variables
page = 1
pushFlag = False

# 4. Button function
def button_to_jump(btn_rect, newpage):
    global page, pushFlag
    mdown = pg.mouse.get_pressed()
    mx, my = pg.mouse.get_pos()
    if mdown[0]:  # 左クリック
        if btn_rect.collidepoint(mx, my) and not pushFlag:
            page = newpage
            pushFlag = True
    else:
        pushFlag = False

# 5. Pages
def page1():
    # 3.画面を初期化する
    screen.blit(img1, (0,0))
    btn1 = screen.blit(next_img, (600, 540))
    # 5.絵を描いたり、判定したりする
    button_to_jump(btn1, 2)

def page2():
    # 3.画面を初期化する
    screen.blit(img2, (0,0))
    btn1 = screen.blit(next_img, (600, 540))
    # 5.絵を描いたり、判定したりする
    button_to_jump(btn1, 1)

# 2.この下をずっとループする
clock = pg.time.Clock()
while True:
    # 7.閉じるボタンが押されたら、終了する
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    
    if page == 1:
        page1()
    elif page == 2:
        page2()
    
    # 6.画面を表示する
    pg.display.update()
    clock.tick(60)
