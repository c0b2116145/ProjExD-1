import pygame as pg
import sys
import random

def check_bound(obj_rct,scr_rct): # 画面外の判別
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

def check_bomb(rct,lst): # 爆弾増幅判定（ランダム）
    check = False # check：Trueなら増幅、Falseならそのまま
    if random.randint(0,1000) == 0: # 1/1000の確率で爆弾が増える
        check = True # checkをTrueにする
        now_x, now_y = rct.center
        create_bomb(now_x, now_y,lst)
    return check

def create_bomb(x,y,l): # 新しい爆弾の設定
    """
    x:爆弾の位置のx軸
    y:爆弾の位置のy軸
    l:爆弾のリスト
    """
    new_bomb_sfc = pg.Surface((20,20)) # Surface
    new_bomb_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(new_bomb_sfc, (255, 0, 0), (10, 10), 10)
    new_bomb_rct = new_bomb_sfc.get_rect() # Rect
    new_bomb_rct.centerx = x
    new_bomb_rct.centery = y
    # 爆弾の動きの設定
    move_x = random.randint(-5,5)
    move_y = random.randint(-5,5)
    l.append([new_bomb_sfc,new_bomb_rct,move_x,move_y]) # 爆弾のリストに追加
    


    



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

    bombs = [[bomb_sfc,bomb_rct,vx,vy]] # 爆弾のリスト作成

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
        # もし画面外なら中に入るように動く
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
        # それ以外はマウスの場所に移動
        else:    
            if event.type == pg.MOUSEMOTION:
                x, y = event.pos # マウスの座標
            
        tori_rct.center = (x,y) # こうかとんの座標更新

        # こうかとんの描画
        scrn_sfc.blit(tori_sfc, tori_rct)

        # 爆弾を増幅させるかの処理
        check_bomb(bomb_rct,bombs)
    
        for bomb in bombs: # すべての爆弾の動き
            yoko, tate = check_bound(bomb[1], scrn_rct) # 画面外判定

            # 画面外なら動きの符号を反転させる（反射する）
            if yoko == -1:
                bomb[2] *= yoko
            if tate == -1:
                bomb[3] *= tate

            # 爆弾を動かす
            bomb[1].move_ip(bomb[2], bomb[3])
            scrn_sfc.blit(bomb[0], bomb[1])

            #爆弾に当たったら終了
            if bomb[1].colliderect(tori_rct):
                return
        
        pg.display.update()
        clock.tick(1000)
    
    

if __name__ == "__main__":
    pg.init() # 初期化
    main() # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()