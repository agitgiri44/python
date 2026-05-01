# 1. Prepare
import pygame as pg, sys

pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("かみしばい")  # title

# 2. Load background images
img1 = pg.image.load("images/root1.png")
img2 = pg.image.load("images/root2.png")
img3 = pg.image.load("images/root3.png")
img4 = pg.image.load("images/root4.png")
img5 = pg.image.load("images/root5.png")

# 3. Load button images
next_img = pg.image.load("images/nextbtn.png")
replay_img = pg.image.load("images/replaybtn.png")

# 4. Initialize variables
page = 1
pushFlag = False

# 5. Button function (jump to new page when clicked)
def btn_to_jump(btn, newpage):
    global page, pushFlag
    mdown = pg.mouse.get_pressed()
    (mx, my) = pg.mouse.get_pos()

    if mdown[0]:  # Left click pressed
        if btn.collidepoint(mx, my) and pushFlag == False:
            page = newpage
            pushFlag = True
    else:
        pushFlag = False


# --- Page functions ---
def page1():
    screen.blit(img1, (0, 0))
    btn1 = screen.blit(next_img, (90, 220))
    btn2 = screen.blit(next_img, (590, 220))
    btn_to_jump(btn1, 2)  # Go to page 2
    btn_to_jump(btn2, 3)


def page2():
    screen.blit(img2, (0, 0))
    btn1 = screen.blit(next_img, (600, 540))
    btn_to_jump(btn1, 3)  # Go to page 3


def page3():
    screen.blit(img3, (0, 0))
    btn1 = screen.blit(replay_img, (190, 320))
    btn2 = screen.blit(replay_img, (490, 320))
    btn_to_jump(btn1, 4)  # Go back to page 1
    btn_to_jump(btn2, 5)
    
def page4():
    screen.blit(img4, (0, 0))
    btn1 = screen.blit(replay_img, (600, 540))
    btn_to_jump(btn1, 1)
    
def page5():
    screen.blit(img5, (0, 0))
    btn1 = screen.blit(replay_img, (600, 540))
    btn_to_jump(btn1, 1)
 

# --- Main game loop ---
clock = pg.time.Clock()

while True:
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Page control
    if page == 1:
        page1()
    elif page == 2:
        page2()
    elif page == 3:
        page3()
    elif page == 4:
        page4()
    elif page == 5:
        page5()

    # Update screen
    pg.display.update()
    pg.time.Clock().tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
