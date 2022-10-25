import pygame as pg
import sys
import random

def check_bound(obj_rct,scr_rct):
    """
    obj_rect:こうかとんrct または 爆弾rct
    scr_rct:スクリーンrct
    領域内:+1/領域外:-1
    """
    yoko,tate = +1,+1
    if obj_rct.left < scr_rct.left or obj_rct.right > scr_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or obj_rct.bottom > scr_rct.bottom:
        tate = -1

    return yoko, tate

def check_bomb():
    check = False
    if random.randint(0,1000) == 0:
        check = True
    return check

def create_bomb(x,y,scrn,l):
    new_bomb_sfc = pg.Surface((20,20))
    new_bomb_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(new_bomb_sfc, (255, 0, 0), (10, 10), 10)
    new_bomb_rct = new_bomb_sfc.get_rect()
    new_bomb_rct.centerx = x
    new_bomb_rct.centery = y
    l.append([new_bomb_sfc,new_bomb_rct])
    


    



def main():
    pg.display.set_caption("逃げろ！こうかとん") # 練習１
    scrn_sfc = pg.display.set_mode((1600,900))
    scrn_rct = scrn_sfc.get_rect()

    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()

    clock = pg.time.Clock()

    # 練習３
    x, y = 900, 400
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = x,y

    # 練習５
    bomb_sfc = pg.Surface((20,20))
    bomb_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb_sfc, (255, 0, 0), (10, 10), 10)
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.centerx = random.randint(0, scrn_rct.width)
    bomb_rct.centery = random.randint(0, scrn_rct.height)

    # 練習６
    vx, vy = +5, +5

    bomb = [[bomb_sfc,bomb_rct]]

    while True:
        scrn_sfc.blit(bg_sfc, bg_rct) # 練習２

        for event in pg.event.get():
            if event.type == pg.QUIT: return
        # # 練習４
        # key_states = pg.key.get_pressed()
        # if key_states[pg.K_UP]: tori_rct.centery -= 1
        # if key_states[pg.K_DOWN]: tori_rct.centery += 1
        # if key_states[pg.K_LEFT]: tori_rct.centerx -= 1
        # if key_states[pg.K_RIGHT]: tori_rct.centerx += 1

        # if yoko == -1:
        #     if key_states[pg.K_LEFT]:
        #         tori_rct.centerx += 1
        #     if key_states[pg.K_RIGHT]:
        #         tori_rct.centerx -= 1

        # if tate == -1:
        #     if key_states[pg.K_UP]:
        #         tori_rct.centery += 1
        #     if key_states[pg.K_DOWN]:
        #         tori_rct.centery -= 1


        # マウスの場所にこうかとんを移動させる
        yoko, tate = check_bound(tori_rct, scrn_rct)
        if yoko == -1:
            if x < scrn_rct.width/2:
                x += 1
            if x > scrn_rct.width/2:
                x -= 1
        elif tate == -1:
            if y < scrn_rct.height/2:
                y += 1
            if y > scrn_rct.height/2:
                y -= 1
        else:    
            if event.type == pg.MOUSEMOTION:
                x, y = event.pos # マウスの座標
            
        tori_rct.center = (x,y) # こうかとんの座標更新

        




        scrn_sfc.blit(tori_sfc, tori_rct)

        yoko, tate = check_bound(bomb_rct, scrn_rct)

        if yoko == -1:
            vx *= yoko
        if tate == -1:
            vy *= tate

        bom = check_bomb()
        if bom:
            now_x, now_y = bomb_rct.center
            create_bomb(now_x,now_y,scrn_sfc,bomb)
        else:

            bomb_rct.move_ip(vx, vy)
            
        for bombs in bomb:
            scrn_sfc.blit(bombs[0], bombs[1])

            if bombs[1].colliderect(tori_rct):
                return
        
        pg.display.update()
        clock.tick(1000)
    
    

if __name__ == "__main__":
    pg.init() # 初期化
    main() # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()