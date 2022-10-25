import pygame as pg
import sys

def main():
    pg.display.set_caption("逃げろ！こうかとん") # 練習１
    scrn_sfc = pg.display.set_mode((1600,900))

    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()

    clock = pg.time.Clock()

    # 練習３
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rect = tori_sfc.get_rect()
    tori_rect.center = 900, 400

    while True:
        scrn_sfc.blit(bg_sfc, bg_rct) # 練習２

        for event in pg.event.get():
            if event.type == pg.QUIT: return

        key_states = pg.key.get_pressed()
        if key_states[pg.K_UP]: tori_rect.centery -= 1
        if key_states[pg.K_DOWN]: tori_rect.centery += 1
        if key_states[pg.K_LEFT]: tori_rect.centerx -= 1
        if key_states[pg.K_RIGHT]: tori_rect.centerx += 1

        scrn_sfc.blit(tori_sfc,tori_rect)
        
        pg.display.update()
        clock.tick(1000)
    
    

if __name__ == "__main__":
    pg.init() # 初期化
    main() # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()