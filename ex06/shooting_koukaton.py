import pygame as pg
import sys
from random import randint, choice

# 湯口追加
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
        self.bg_flip_sfc = pg.transform.flip(self.bg_sfc, True, False)
        self.bg_rct = self.bg_sfc.get_rect()
        # 背景スクロール用
        self.bg_x = 0
        self.bgf_x =1600
        self.scroll_speed = 1
        self.scroll_count = 1

    def blit(self):
        # 背景スクロールするように貼り付け
        # self.bg_x = (self.bg_x-1)%1600
        # print(self.bg_x)
        # self.sfc.blit(self.bg_sfc,[self.bg_x-1600,0])
        # self.sfc.blit(self.bg_flip_sfc,[self.bg_x,0])
        self.sfc.blit(self.bg_sfc,[self.bg_x,0])
        self.sfc.blit(self.bg_flip_sfc,[self.bgf_x,0])
        self.bg_x -= self.scroll_speed
        self.bgf_x -= self.scroll_speed
        if abs(self.bg_x) > 1600:
            self.bg_x = 1600
        if abs(self.bgf_x) > 1600:
            self.bgf_x = 1600



class Image:
    def __init__(self, img, zoom, xy):
        """
        img:画像
        zoom:画像の拡大倍率
        xy:初期位置の座標のタプル
        """
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
    
    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)


class Bird(Image): # こうかとんクラス
    # こうかとん移動
    key_delta = {
        pg.K_UP:    [0, -3],
        pg.K_DOWN:  [0, +3],
        pg.K_LEFT:  [-3 , 0],
        pg.K_RIGHT: [+3, 0],
    }

    def __init__(self, img, zoom, xy):
        # こうかとん画像設定
        super().__init__(img, zoom, xy)

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


class Enemy(Image): # 敵クラス
    def __init__(self, img, zoom, xy, vxy):
        """
        vxy:敵のx,y移動の大きさのタプル
        """
        # 敵初期設定
        super().__init__(img, zoom, xy)
        self.vx, self.vy = vxy 
        
    def update(self,scr:Screen):
        self.rct.move_ip(self.vx, self.vy) # 敵の移動
        yoko, tate = check_bound(self.rct, scr.rct) # 壁判定（横はいらない）
        self.vy *= tate
        self.blit(scr)


class Attack(Image): # 攻撃クラス 
    def __init__(self,img ,zoom, vxy, xy):
        """
        vxy:玉の移動のタプル
        """
        # 卵設定
        super().__init__(img, zoom, xy)
        # 移動の変数
        self.vx, self.vy = vxy

    def update(self,scr:Screen):
        # 玉の移動
        self.rct.centerx += self.vx
        self.rct.centery += self.vy
        # 壁判定(横はいらない)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vy *= tate
        self.blit(scr)


class  Bomb: # 敵の攻撃クラス
    def __init__(self, color, radius, vxy, xy):
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
        self.rct.center = xy
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


class Item(Image): # 薬のクラス
    def __init__(self, img, zoom, xy):
        # 薬の設定
        super().__init__(img, zoom, xy)

    def update(self,scr:Screen):
        self.rct.move_ip(-1,0) # 薬の移動
        self.blit(scr)


class Heal(Image): # ハートのクラス
    def __init__(self, img, zoom, xy):
        # ハートの初期設定
        super().__init__(img, zoom, xy)

    def update(self,scr:Screen):
        self.rct.move_ip(-1,0) # ハートの移動
        self.blit(scr)

# 湯口の追加
class LastEnemy(Image): #ラスボスのクラス
    def __init__(self, img, zoom, xy, hp, ):
        """
        hp:ラスボスの体力
        """
        #ラスボスの初期設定
        super().__init__(img, zoom, xy)
        self.rct.centerx += self.rct.width #初期位置を右画面外に設定
        self.hp = hp 
        self.cha_hp = hp/2
        self.vx = -1 # 移動する量
        self.tossin = False # 突進攻撃をするかどうか
        self.turn = True # True:前突進, Fales:後退

    def update(self, scr:Screen):
        self.zensin(self.tossin)
        self.rct.move_ip(self.vx, 0)
        self.blit(scr)

    def zensin(self, hanntei):
        self.tossin = hanntei
        # 定位置につきかつ突進攻撃中ではない時
        if self.rct.centerx <= 1200 and not self.tossin:
            self.vx = 0
        # 突進攻撃中かつ前突進中
        if self.tossin and self.turn:
            self.vx = -4
            if self.rct.centerx<=800: # ラスボスの位置が800以下になったら
                self.turn = False # 後退するようにする
        # 突進攻撃中かつ後退中
        elif self.tossin and not self.turn:
            self.vx = 1
            if self.rct.centerx>=1199: # ラスボスの位置が1199異常になったら
                self.turn = True # 前突進するようにする
                self.tossin = False # 突進攻撃やめ


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

def gamen(scr, gamen_name:str, gamen_col:tuple, sentakusi:dict):
    clock = pg.time.Clock() # クロック
    state = 0 # 0:ゲームを始める, 1:ゲームをやめる
    title = pg.font.Font(None, 100) # タイトル
    choice = pg.font.Font(None, 70) # 選択肢
    title_render = title.render(gamen_name, True, gamen_col)
    while True:
        scr.blit() # 背景を描画
        for event in pg.event.get():
            # ✕が押されたら終了
            if event.type == pg.QUIT:
                return
            # キーが押されたら
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT and state<len(sentakusi)-1: # 左矢印を押した　かつ　stateが選択肢の数より小さければ
                    state += 1 # 1つ右を選択
                if event.key == pg.K_LEFT and state>0: # 右矢印を押した　かつ　stateが0より大きければ
                    state -= 1 # 1つ左を選択
                if event.key == pg.K_RETURN: # エンターを押したら
                    return state # stateを返す

        for index, (sentaku, sentaku_col) in enumerate(sentakusi.items()):
            if state == index:
                choice_render = choice.render(sentaku, True, (0, 0, 0), sentaku_col)
            else:
                choice_render = choice.render(sentaku, True, (255, 255, 255))

            width = choice_render.get_width()
            height = choice_render.get_height()

            haba = scr.rct.width/(len(sentakusi)+1)

            pos_x = haba*(index+1) - (width/2)
            pos_y = scr.rct.centery-(height/2)
            scr.sfc.blit(choice_render, (pos_x, pos_y))
            
        scr.sfc.blit(title_render, (scr.rct.centerx-(title_render.get_width())/2, scr.rct.height/3))

        clock.tick(1000)
        pg.display.update()



def main():
    smode = False # 攻撃無制限モードであるかの判定
    lene_flg = False # ラスボスを描画指せるかのフラグ(湯口)
    lene_aname_lit = ["big_bomb", "frea", "tossin", "tossin", "nasi"] # ラスボスの攻撃手段
    clock = pg.time.Clock() # クロック
    # スクリーンのインスタンス
    scr = Screen("よけろ！こうかとん", (1600,900), "fig/pg_bg.jpg")
    # こうかとんのインスタンス
    kkt = Bird("fig/6.png", 1.0, (900, 400))
    # ラスボスのインスタンス
    lene = LastEnemy("fig/last_enemy.png", 1.5, (1600, 450), 500)
    # 敵のインスタンス
    ene = [Enemy("fig/teki.png", 0.2, (1700,randint(0,900)), (randint(-3, -1),randint(-2,2)))]
    # 攻撃のインスタンス
    atk = []
    # 敵の攻撃のインスタンス
    bkd = []
    # 薬のインスタンス
    itm = []
    # ハートのインスタンス
    hrt = []
    # 一定時間でイベントを発生させる(湯口)
    pg.time.set_timer(31, 60000, 1) # ラスボスが出てくる時間になったら1回だけイベント31番を発生させる
    pg.time.set_timer(29, 5000) #敵を登場させる
    pg.time.set_timer(28, 40000) # アイテムを登場させる
    pg.time.set_timer(27, 40000) #  ハートを登場させる

    start = gamen(scr, "SHOOTING KOUKATON", (0, 0, 255), {"start":(0, 125, 125), "quit":(125, 125, 0), "about":(0, 0, 255)})
    if start == 1:
        return

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
                        # 攻撃リストに3方向追加(この様に書いた方がネストが少なくて良いのではと思った。あと実行時間的にこっちの方が速そう。大した差じゃないけど)
                        atk.extend([Attack("fig/egg_toumei.png" ,0.2,(3,i), kkt.rct.center)for i in range(-1, 2)]) 
                    # 画面上に6こ卵がなければ
                    elif len(atk) <  6:
                        # 攻撃リストに3方向追加
                        atk.extend([Attack("fig/egg_toumei.png" ,0.2,(3,i), kkt.rct.center)for i in range(-1, 2)])
            # 31イベントであったら
            if event.type == 31:
                lene_flg = True # ラスボスを描画スタート
                pg.time.set_timer(30, 10000) # ラスボスの攻撃を呼び出す。
            if event.type == 30:
                kougeki = choice(lene_aname_lit)
                if kougeki == "big_bomb":
                    bkd.append(Bomb((0,0,255), 50, (randint(-5,-3),randint(-5,-3)), lene.rct.center))
                elif kougeki == "frea":
                    bkd.extend([Bomb((255, 0, 0), 10, (-3,i), lene.rct.center) for i in range(-3, 4)])
                elif kougeki == "tossin":
                    lene.zensin(True)
                elif kougeki == "nasi":
                    continue
            if event.type == 29:
                ene.extend([Enemy("fig/teki.png", 0.2, (1700,randint(0,900)),(randint(-3,-1),randint(-2,2))) for _ in range(5)])
            if event.type == 28:
                itm.append(Item("fig/kusuri.png", 0.2,(1700,randint(0,900))))
            if event.type == 27:
                hrt.append(Heal("fig/heart.png", 0.2,(1700,randint(0,900))))

            if event.type == 26:
                smode = False

        if lene_flg: # ラスボスを描画するかどうか
            if kkt.rct.colliderect(lene.rct):
                end = gamen(scr, "GAME OVER", (255, 0, 0), {"restart":(0, 125, 125), "quit":(125, 125, 0)})
                if end == 0:
                    main()
                return
            lene.update(scr)

        kkt.update(scr)

        for attack in atk: # attackはAttackクラスインスタンス
            attack.update(scr)

            if lene.rct.colliderect(attack.rct): # ラスボスがattackに当たったら
                # ラスボスの体力を減らす
                atk.remove(attack)
                lene.hp -= 1
                if lene.hp <= lene.cha_hp: # 体力が半分になったら
                    lene_hp = lene.hp
                    lene_rct_x = lene.rct.centerx-lene.rct.width
                    lene_rct_y =  lene.rct.centery
                    # ラスボスが赤くなる　
                    lene = LastEnemy("fig/last_enemy_r.png", 2, (lene_rct_x, lene_rct_y), lene_hp)
                if lene.hp <= 0: # 体力が0以下になったら終了
                    comp = gamen(scr, "MISSION COMPLETE", (0, 0, 255), {"restart":(0, 125, 125), "quit":(125, 125, 0)})
                    if comp == 0:
                        main()
                    return

            if attack.rct.centerx >= 1550: # 卵が画面外へ移動した時
                atk.remove(attack) # リストから卵を消す


        for enemy in ene: # enemyはEnemyクラスインスタンス
            enemy.update(scr) # 敵の更新
            if kkt.rct.colliderect(enemy.rct):
                # もしこうかとんが敵とぶつかったら終了
                end = gamen(scr, "GAME OVER", (255, 0, 0), {"restart":(0, 125, 125), "quit":(125, 125, 0)})
                if end == 0:
                    main()
                return

            if randint(0,1000) == 0: # ランダムに
                # 爆弾を出す（敵の攻撃）
                bkd.append(Bomb((255,0,0), 10, (randint(-3,3),randint(-3,3)), enemy.rct.center))

            if enemy.rct.right <= 0:
                ene.remove(enemy)
                continue

            for attack in atk: # attackはAttackクラスインスタンス
                if enemy.rct.colliderect(attack.rct):
                    ene.remove(enemy)
                    atk.remove(attack)
                    break

        for bomb in bkd: # bombはBombクラスインスタンス
            bomb.update(scr) # 爆弾の更新

            if kkt.rct.colliderect(bomb.rct):
                end = gamen(scr, "GAME OVER", (255, 0, 0), {"restart":(0, 125, 125), "quit":(125, 125, 0)})
                if end == 0:
                    main()
                return

            if bomb.bound == 3: # もし3回跳ね返ったら
                # 爆弾が消える
                bkd.remove(bomb)
             
        for item in itm: # itemはItemクラスインスタンス
            item.update(scr) 
            if item.rct.right <= 0:
                itm.remove(item)
                continue

            if kkt.rct.colliderect(item.rct):
                smode = True
                pg.time.set_timer(26, 5000, 1) # 5秒後にイベント26を呼んで無制限モードを解除
                itm.remove(item)

        for heart in hrt: # heartはHEALクラスインスタンス
            heart.update(scr) 
            if heart.rct.right <= 0:
                hrt.remove(heart)
                continue

            # ハートを取ったら全部消える
            if kkt.rct.colliderect(heart.rct):
                ene.clear()
                atk.clear()
                bkd.clear( )
                hrt.remove(heart)

        clock.tick(1000)
        pg.display.update()
        

if __name__ == "__main__":
    pg.init() # 初期化
    main() # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()