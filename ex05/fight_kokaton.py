from operator import index
import pygame as pg
import sys
from random import randint

class Screen:
    def __init__(self, title, wh, bgimg):
        # 練習1
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bg_sfc = pg.image.load(bgimg)
        self.bg_rct = self.bg_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.bg_sfc, self.bg_rct) # 練習2


class Bird:
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, img, zoom, xy):
        # 練習3
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_states = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_states[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
                # 練習7
                if check_bound(self.rct, scr.rct) != (+1, +1):
                    self.rct.centerx -= delta[0]
                    self.rct.centery -= delta[1]
        self.blit(scr)


class Bomb:
    def __init__(self, color, radius, vxy, scr:Screen, fx, fy):
        self.sfc = pg.Surface((radius*2, radius*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (radius,radius), radius) # 円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = fx
        self.rct.centery = fy
        self.vx, self.vy = vxy
        self.bound = 0

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        if yoko == -1 or tate == -1:
            self.count_bound()

        self.blit(scr)

    def count_bound(self):
        self.bound += 1

        

class Enemy:
    def __init__(self, img, zoom, xy):
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr:Screen):
        self.rct.centerx += 1
        self.blit(scr)



def check_bound(obj_rct, scr_rct):
    """
    obj_rct：こうかとんrct，または，爆弾rct
    scr_rct：スクリーンrct
    領域内：+1／領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate


def main():
    scr = Screen("逃げろ！こうかとん", (1600,900), "fig/pg_bg.jpg")

    kkt = Bird("fig/6.png", 2.0, (900, 400))

    bkd = []


    ene = [Enemy("fig/1.png", 1.0, (0,randint(0,900)))]


    clock = pg.time.Clock() # 練習1
    while True:
        scr.blit()
        for event in pg.event.get(): # 練習2
            if event.type == pg.QUIT:
                return

        kkt.update(scr)

        if randint(0,1000) == 0:
            ene.append(Enemy("fig/1.png", 1.0, (0,randint(0,900))))


        for enemy in ene:
            enemy.update(scr)
            if kkt.rct.colliderect(enemy.rct):
                return

            if randint(0,500) == 0:
                bkd.append(Bomb((255,0,0), 10, (randint(-2,2),randint(-5,5)), scr, enemy.rct.centerx, enemy.rct.centery))

        for bomb in bkd:
            if bomb.bound == 3:
                bkd.remove(bomb)
                break
            bomb.update(scr)
            if kkt.rct.colliderect(bomb.rct): # こうかとんrctが爆弾rctと重なったら
                return

        pg.display.update() #練習2
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main() # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()