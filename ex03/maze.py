import tkinter as tk
import maze_maker as mm

def key_down(event): #キーを押したら
    global key
    key =event.keysym #押したキーの取得

def key_up(event): #キーを離したら
    global key
    key = "" #リセット

def main_proc(): #メインの関数
    global mx, my
    global cx, cy
    global maze_list
    #上下左右の処理
    if key == "Up":
        my -= 1
    if key == "Down":
        my += 1
    if key == "Left":
        mx -= 1
    if key == "Right":
        mx += 1

    #もし壁だったら上記の処理を無かったことにする
    if maze_list[my][mx] == 1:
        if key == "Up":
            my += 1
        if key == "Down":
            my -= 1
        if key == "Left":
            mx += 1
        if key == "Right":
            mx -= 1

    #もしゴールだったらテキストを"GOAL"にし停止する
    elif maze_list[my][mx] == 3:
        cx, cy = mx*100+50, my*100+50 #こうかとんの場所の更新
        canv.coords("tori", cx, cy)
        text.set("GOAL") #テキストをゴールにする
        return #<-再起関数を呼び出させないようにする

    #それ以外ならこうかとんの場所を更新する
    else:
        cx, cy = mx*100+50, my*100+50

    #もし"r"を押したら
    if key == "r":
        canv.delete("tori")             #canv内のこうかとんの"tori"のタグを削除する
        #こうかとんの場所の初期化
        mx, my = 1, 1
        cx, cy = mx*100+50,my*100+50
        #迷路の再構築  
        maze_list = mm.make_maze(15,9)
        mm.show_maze(canv, maze_list)
        #こうかとんの描画
        canv.create_image(cx,cy,image=tori,tag="tori")

        
    #canvの更新
    canv.coords("tori", cx, cy)
    #再起
    root.after(100,main_proc)


if __name__ == "__main__":
    root = tk.Tk()
    #テキストの設定
    text = tk.StringVar()
    text.set("Play")

    root.title("迷えるこうかとん")
    #textvariableでテキストの更新を可能にする
    label = tk.Label(root,textvariable=text,font=("",100))
    label.pack()

    canv = tk.Canvas(root,width=1500,height=900,bg="black")
    canv.pack()

    maze_list = mm.make_maze(15,9)

    mm.show_maze(canv, maze_list)

    tori = tk.PhotoImage(file="fig/5.png")
    mx, my = 1,1
    cx,cy = mx*100+50, my*100+50
    canv.create_image(cx,cy,image=tori,tag="tori")

    key = ""

    root.bind("<KeyPress>",key_down)
    root.bind("<KeyRelease>",key_up)

    main_proc()

    root.mainloop()