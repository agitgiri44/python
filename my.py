import pygame as pg
import sys
import random

# ======================
# 初期設定
# ======================
pg.init()
pg.mixer.init()

# 画面設定
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Trap Game")

# ======================
# データ読み込み
# ======================
# プレイヤー
myimgR = pg.image.load("images/playerR.png")
myimgR = pg.transform.scale(myimgR, (40, 50))
myimgL = pg.transform.flip(myimgR, True, False)
myrect = pg.Rect(50, 200, 40, 50)

# 敵（オバケ）
enemyimgR = pg.image.load("images/obake.png")
enemyimgR = pg.transform.scale(enemyimgR, (50, 50))
enemyimgL = pg.transform.flip(enemyimgR, True, False)
enemyrect = pg.Rect(650, 200, 50, 50)

# 壁
walls = [
    pg.Rect(0, 0, 800, 20),
    pg.Rect(0, 0, 20, 600),
    pg.Rect(780, 0, 20, 600),
    pg.Rect(0, 580, 800, 20)
]

# ワナ（トラップ）
trapimg = pg.image.load("images/uni.png")
trapimg = pg.transform.scale(trapimg, (30, 30))
traps = []
for i in range(20):
    wx = 150 + i * 30
    wy = random.randint(20, 550)
    traps.append(pg.Rect(wx, wy, 30, 30))

# ゴール
goalrect = pg.Rect(750, 250, 30, 100)

# ボタン
replay_img = pg.image.load("images/replaybtn.png")
replay_img = pg.transform.scale(replay_img, (120, 60))
replay_rect = replay_img.get_rect(center=(400, 480))

# ======================
# 変数
# ======================
rightFlag = True
pushFlag = False
page = 1  # 1=start, 2=gameover, 3=clear, 4=game

# ======================
# 関数
# ======================
def button_to_jump(btn, newpage):
    """クリックでページ切り替え"""
    global page, pushFlag
    mdown = pg.mouse.get_pressed()
    (mx, my) = pg.mouse.get_pos()
    if mdown[0]:
        if btn.collidepoint(mx, my) and not pushFlag:
            pg.mixer.Sound("sounds/pi.wav").play()
            page = newpage
            pushFlag = True
    else:
        pushFlag = False


def gamereset():
    """データのリセット"""
    myrect.x = 50
    myrect.y = 100
    for d in range(20):
        traps[d].x = 150 + d * 30
        traps[d].y = random.randint(20, 550)
    enemyrect.x = 650
    enemyrect.y = 200


def gamestage():
    """メインゲームステージ"""
    global rightFlag, page, myrect, enemyrect

    screen.fill(pg.Color("deepskyblue"))

    vx = 0
    vy = 0

    # --- プレイヤー操作 ---
    key = pg.key.get_pressed()
    if key[pg.K_RIGHT]:
        vx = 2
        rightFlag = True
    if key[pg.K_LEFT]:
        vx = -2
        rightFlag = False
    if key[pg.K_UP]:
        vy = -4
    if key[pg.K_DOWN]:
        vy = 4

    # --- プレイヤー移動 ---
    myrect.x += vx
    myrect.y += vy

    # 壁衝突
    if myrect.collidelist(walls) != -1:
        myrect.x -= vx
        myrect.y -= vy

    # プレイヤー描画
    if rightFlag:
        screen.blit(myimgR, myrect)
    else:
        screen.blit(myimgL, myrect)

    # 壁描画
    for wall in walls:
        pg.draw.rect(screen, pg.Color("darkgreen"), wall)

    # ワナ描画
    for trap in traps:
        screen.blit(trapimg, trap)

    # ワナ衝突
    if myrect.collidelist(traps) != -1:
        pg.mixer.Sound("sounds/down.wav").play()
        page = 2  # game over

    # --- 敵(オバケ)の処理 ---
    ovx = 0
    ovy = 0
    # 敵スピードを調整（ゆっくり追う）
    speed = 1
    if enemyrect.x < myrect.x:
        ovx = speed
    else:
        ovx = -speed
    if enemyrect.y < myrect.y:
        ovy = speed
    else:
        ovy = -speed

    enemyrect.x += ovx
    enemyrect.y += ovy

    # 敵の描画
    if ovx > 0:
        screen.blit(enemyimgR, enemyrect)
    else:
        screen.blit(enemyimgL, enemyrect)

    # 敵に当たったらゲームオーバー
    if myrect.colliderect(enemyrect):
        pg.mixer.Sound("sounds/down.wav").play()
        page = 2

    # --- ゴール描画 ---
    pg.draw.rect(screen, pg.Color("gold"), goalrect)
    if myrect.colliderect(goalrect):
        pg.mixer.Sound("sounds/up.wav").play()
        page = 3


def gameover():
    """ゲームオーバー画面"""
    gamereset()
    screen.fill(pg.Color("navy"))
    font = pg.font.Font(None, 150)
    text = font.render("GAME OVER", True, pg.Color("red"))
    screen.blit(text, (100, 200))
    btn1 = screen.blit(replay_img, (320, 480))
    button_to_jump(btn1, 4)  # restart game


def gameclear():
    """ゲームクリア画面"""
    gamereset()
    screen.fill(pg.Color("gold"))
    font = pg.font.Font(None, 150)
    text = font.render("GAME CLEAR", True, pg.Color("red"))
    screen.blit(text, (60, 200))
    btn1 = screen.blit(replay_img, (320, 480))
    button_to_jump(btn1, 4)


def startpage():
    """スタートページ"""
    screen.fill(pg.Color("white"))
    font = pg.font.SysFont(None, 80)
    title = font.render("Trap Game", True, pg.Color("black"))
    screen.blit(title, (280, 200))
    btn1 = screen.blit(replay_img, (340, 400))
    button_to_jump(btn1, 4)


# ======================
# メインループ
# ======================
clock = pg.time.Clock()

while True:
    # イベント処理
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # ページごとに分岐
    if page == 1:
        startpage()
    elif page == 2:
        gameover()
    elif page == 3:
        gameclear()
    elif page == 4:
        gamestage()

    # 画面更新
    pg.display.update()
    clock.tick(60)
