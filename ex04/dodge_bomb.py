import pygame as pg
import sys

def main():
    pg.display.set_caption("逃げろ！こうかとん") # 練習１
    scrn_sfc = pg.display.set_mode((1600,900))

    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()

    while True:
        scrn_sfc.blit(bg_sfc, bg_rct) # 練習２

        pg.display.update()

        clock = pg.time.Clock()
        clock.tick(1000)

        for event in pg.event.get():
            if event.type == pg.QUIT: return

    
    

if __name__ == "__main__":
    pg.init() # 初期化
    main() # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()