import pygame as pg
import sys
import random

def main():
    pg.display.set_caption("逃げろ！こうかとん") # 練習１
    scrn_sfc = pg.display.set_mode((1600,900))
    scrn_rct = scrn_sfc.get_rect()

    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()

    clock = pg.time.Clock()

    # 練習３
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rect = tori_sfc.get_rect()
    tori_rect.center = 900, 400

    # 練習５
    bomb_sfc = pg.Surface((20,20))
    bomb_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb_sfc, (255, 0, 0), (10, 10), 10)
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.centerx = random.randint(0, scrn_rct.width)
    bomb_rct.centery = random.randint(0, scrn_rct.height)

    while True:
        scrn_sfc.blit(bg_sfc, bg_rct) # 練習２

        for event in pg.event.get():
            if event.type == pg.QUIT: return
        # 練習４
        key_states = pg.key.get_pressed()
        if key_states[pg.K_UP]: tori_rect.centery -= 1
        if key_states[pg.K_DOWN]: tori_rect.centery += 1
        if key_states[pg.K_LEFT]: tori_rect.centerx -= 1
        if key_states[pg.K_RIGHT]: tori_rect.centerx += 1

        scrn_sfc.blit(tori_sfc, tori_rect)

        scrn_sfc.blit(bomb_sfc, bomb_rct)
        
        pg.display.update()
        clock.tick(1000)
    
    

if __name__ == "__main__":
    pg.init() # 初期化
    main() # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()