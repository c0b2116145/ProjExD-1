import pygame as pg
import sys
from random import randint

class Screen: # スクリーンクラス
    def __init__(self, title, wh, bgimg):
        """
        title:スクリーンのタイトル
        wh:スクリーンサイズ
        bgimg:背景画像
        """
        # スクリーン設定
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)
        # レクト獲得
        self.rct = self.sfc.get_rect()
        # 背景画像
        self.bg_sfc = pg.image.load(bgimg)
        self.bg_rct = self.bg_sfc.get_rect()
        # 背景スクロール用
        self.bg_x = 0

    def blit(self):
        # 背景スクロールするように貼り付け
        self.bg_x = (self.bg_x-8)%1600
        self.sfc.blit(self.bg_sfc,[self.bg_x-1600,0])
        self.sfc.blit(self.bg_sfc,[self.bg_x,0])


class Bird: # こうかとんクラス
    # こうかとん移動
    key_delta = {
        pg.K_UP:    [0, -3],
        pg.K_DOWN:  [0, +3],
        pg.K_LEFT:  [-3 , 0],
        pg.K_RIGHT: [+3, 0],
    }

    def __init__(self, img, zoom, xy):
        # こうかとん画像設定
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def blit(self, scr:Screen):
        # こうかとん画像ブリット
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        # 矢印キー獲得
        key_states = pg.key.get_pressed()
        # 矢印キーに対応した移動
        for key, delta in Bird.key_delta.items():
            if key_states[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
                # 壁なら移動しない
                if check_bound(self.rct, scr.rct) != (+1, +1):
                    self.rct.centerx -= delta[0]
                    self.rct.centery -= delta[1]

        self.blit(scr)


class Enemy: # 敵クラス
    def __init__(self, img, zoom, xy, vxy):
        """
        img:敵画像
        zoom:敵画像の拡大倍率
        xy:初期位置の座標のタプル
        vxy:敵のx,y移動の大きさのタプル
        """
        # 敵初期設定
        sfc = pg.image.load(img)
        sfc.set_colorkey((255,255,255))
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect() 
        self.rct.center = xy
        self.vx, self.vy = vxy 
        

    def blit(self, scr:Screen):
        # 敵のブリット
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr:Screen):
        self.rct.move_ip(self.vx, self.vy) # 敵の移動
        yoko, tate = check_bound(self.rct, scr.rct) # 壁判定（横はいらない）
        self.vy *= tate
        self.blit(scr)


class Attack: # 攻撃クラス 
    def __init__(self,img ,zoom, vxy, fx, fy):
        """
        img:卵画像読み込み
        zoom:卵画像の拡大倍率
        vxy:玉の移動のタプル
        fx:玉のx軸初期位置
        fy:玉のy軸初期位置
        """
        # 卵設定
        self.sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        # 初期位置
        self.rct.centerx = fx
        self.rct.centery = fy
        # 移動の変数
        self.vx, self.vy = vxy[0]  , vxy[1]
        
    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr:Screen):
        # 玉の移動
        self.rct.centerx += self.vx
        self.rct.centery += self.vy
        # 壁判定(横はいらない)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vy *= tate
        self.blit(scr)


class  Bomb: # 敵の攻撃クラス
    def __init__(self, color, radius, vxy, fx, fy):
        """
        color:敵の攻撃の色
        radius:敵の攻撃の大きさ
        vxy:移動のタプル
        fx:x軸の初期位置
        fy:y軸の初期位置
        """
        # 敵の攻撃の設定
        self.sfc = pg.Surface((radius*2, radius*2))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (radius,radius), radius)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = fx
        self.rct.centery = fy
        self.vx, self.vy = vxy
        self.bound = 0 # 跳ね返りカウント

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr:Screen):
        # 敵の攻撃の移動
        self.rct.move_ip(self.vx, self.vy)
        # 跳ね返り
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        if yoko == -1 or tate == -1: # もし跳ね返ったら
            self.count_bound() # 跳ね返りカウントを呼び出す

        self.blit(scr)

    def count_bound(self): # 跳ね返りカウント関数
        self.bound += 1 # 跳ね返りのカウントを増やす


class Item: # 薬のクラス
    def __init__(self, img, zoom, xy):
        """
        img:薬の画像
        zoom:薬の画像の拡大倍率
        xy:薬の初期位置
        """
        # 薬の設定
        sfc = pg.image.load(img) 
        sfc.set_colorkey((255,255,255))
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom) 
        self.rct = self.sfc.get_rect() 
        self.rct.center = xy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr:Screen):
        self.rct.move_ip(-1,0) # 薬の移動
        self.blit(scr)

class Heal: # ハードのクラス
    def __init__(self, img, zoom, xy):
        """
        img:ハートの画像
        zoom:ハートの画像の拡大倍率
        xy:ハートの初期位置
        """
        # ハートの初期設定
        sfc = pg.image.load(img) 
        sfc.set_colorkey((255,255,255))
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom) 
        self.rct = self.sfc.get_rect() 
        self.rct.center = xy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr:Screen):
        self.rct.move_ip(-1,0) # ハートの移動
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
    smode = False # 攻撃無制限モードであるかの判定
    ult = 0 # 攻撃無制限モードの時間計測
    time = 0 # 時間計測
    clock = pg.time.Clock() # クロック
    # スクリーンのインスタンス
    scr = Screen("よけろ！こうかとん", (1600,900), "fig/pg_bg.jpg")
    # こうかとんのインスタンス
    kkt = Bird("fig/6.png", 1.0, (900, 400))
    # 敵のインスタンス
    ene = [Enemy("fig/teki.jpeg", 0.2, (1700,randint(0,900)), (randint(-3, -1),randint(-2,2)))]
    # 攻撃のインスタンス
    atk = []
    # 敵の攻撃のインスタンス
    bkd = []
    # 薬のインスタンス
    itm = []
    # ハートのインスタンス
    hrt = []

    while True:
        scr.blit() # スクリーンのブリット
        for event in pg.event.get():
            # ✕が押されたら終了
            if event.type == pg.QUIT:
                return
            # キーが押されたら
            if event.type == pg.KEYDOWN:
                # そのキーがスペースなら
                if event.key == pg.K_SPACE:
                    # 攻撃無制限モードなら
                    if smode == 1:
                        # 攻撃リストに3方向追加
                        for i in range(-1,2):
                            atk.append(Attack("fig/egg_toumei.png" ,0.2,(3,i), kkt.rct.centerx, kkt.rct.centery) ) 
                    # 画面上に6こ卵がなければ
                    elif len(atk) <  6:
                        # 攻撃リストに3方向追加
                        for i in range(-1,2):
                            atk.append(Attack("fig/egg_toumei.png" ,0.2,(3,i), kkt.rct.centerx, kkt.rct.centery) )

        kkt.update(scr)

        for attack in atk: # attackはAttackクラスインスタンス
            if attack.rct.centerx >= 1550: # 卵が画面外へ移動した時
                atk.remove(attack) # リストから卵を消す

            attack.update(scr)

        # 一定時間になったら薬とハートを追加
        if time%5000 == 0:
            itm.append(Item("fig/kusuri.jpg", 0.2,(1700,randint(0,900))))

        if time%5000 == 0:
            hrt.append(Heal("fig/heart.png", 0.2,(1700,randint(0,900))))

        # 一定時間たったら敵を5体追加
        if time%500 == 0:
            # 敵の追加
            for _ in range(5):
                ene.append(Enemy("fig/teki.jpeg", 0.2, (1700,randint(0,900)),(randint(-3,-1),randint(-2,2))))

        for enemy in ene: # enemyはEnemyクラスインスタンス
            enemy.update(scr) # 敵の更新
            if kkt.rct.colliderect(enemy.rct):
                # もしこうかとんが敵とぶつかったら終了
                return

            if randint(0,1000) == 0: # ランダムに
                # 爆弾を出す（敵の攻撃）
                bkd.append(Bomb((255,0,0), 10, (randint(-3,3),randint(-3,3)), enemy.rct.centerx, enemy.rct.centery))
        
            for attack in atk: # attackはAttackクラスインスタンス
                if enemy.rct.colliderect(attack.rct):
                    ene.remove(enemy)
                    atk.remove(attack)
                    break   

        for bomb in bkd: # bombはBombクラスインスタンス
            bomb.update(scr) # 爆弾の更新
            if bomb.bound == 3: # もし3回跳ね返ったら
                # 爆弾が消える
                bkd.remove(bomb)
                break

            if kkt.rct.colliderect(bomb.rct):
                return
             
        for item in itm: # itemはItemクラスインスタンス
            item.update(scr) 
            if item.rct.centerx <= 0:
                itm.remove(item)
                break

            if kkt.rct.colliderect(item.rct):
                smode = True
                itm.remove(item)
                break

        for heart in hrt: # heartはHEALクラスインスタンス
            heart.update(scr) 
            if heart.rct.centerx <= 0:
                hrt.remove(heart)
                break

            # ハートを取ったら全部消える
            if kkt.rct.colliderect(heart.rct):
                ene.clear()
                atk.clear()
                bkd.clear( )
                hrt.remove(heart)
                break

        # 攻撃無制限モードなら
        if smode:
            # 時間を追加
            ult += 1
            # 一定時間で終了
            if ult >= 1000:
                smode = False
                ult = 0


        clock.tick(1000)
        time += 1
        pg.display.update()
        

if __name__ == "__main__":
    pg.init() # 初期化
    main() # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()