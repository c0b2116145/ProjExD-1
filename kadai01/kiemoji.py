import random,time

all_moji_num = 26
Q_num = 10
A_num = 2
user_ans_num = 2

def syutudai():
    global all_moji_num, Q_num, A_num
    all_moji = []
    for i in range(all_moji_num):
        all_moji.append(chr(65+i))

    Q = random.sample(all_moji,Q_num)
    
    taisyou = ""
    for moji in Q:
        taisyou += moji
    
    kessonn = ""
    for i in range(A_num):
        kessonn += Q.pop(random.randint(0,Q_num-(i+1)))
    
    random.shuffle(Q)
    hyouji = ""
    for moji in Q:
        hyouji += moji

    

    return taisyou, kessonn, hyouji


def main_qize():
    global user_ans_num
    time_s = time.time()
    for i in range(user_ans_num):
        T,K,H = syutudai()
        print(f"対象文字：{T}")
        print(f"欠損文字：{K}")
        print(f"表示文字：{H}")
        print()

        user_kessonn_num = int(input("欠損文字はいくつあるでしょうか？："))
        if user_kessonn_num == len(K):
            print("正解です。では、具体的に欠損文字を入力してください。")
            user_ans = []
            for j in range(len(K)):
                ans = input(f"{j+1}文字目は：")
                user_ans.append(ans)

            check_ans = True
            for u in K:
                if u in user_ans:
                    continue
                else:
                    check_ans = False
                    break

            if check_ans:
                print("正解！")
                time_e = time.time()
                break
            else:
                print("不正解です。またチャレンジしましょう")
                print("------------------------------------")
                time_e = time.time()
        else:
            print("不正解です。またチャレンジしましょう")
            print("-------------------------------------")
            time_e = time.time()

    total_time = time_e-time_s
    print(f"所要時間は{round(total_time)}秒です。")


if __name__ == "__main__":
    main_qize()

#第１回
##消えたアルファベットを探すゲーム
###遊び方
#コマンドラインで"kiemoji.py"を入力して起動する。
#対象文字と表示文字を見比べ、消えたアルファベットを探す。
#まず、消えた文字の個数を回答する。
#次に、消えたアルファベットを入力する（消えた文字数分回答）。
#ユーザの回答がすべてあっていた時、ゲームを終了する。
#不正解だった場合はその時点でやり直す。
#なお、最大やり直し数が決まっている。
#ユーザのやり直し回数が上限を超えた時、その時点でゲームを終了する。
#ゲーム終了時にこの問題にかかった時間を表示する。
###プログラムの内容
#main_quiz関数はユーザの回答の合否と、それに応じたコメント、所要時間の計測と表示をする。
#↳その際にsyutudai関数を呼び出す。
#syutudai関数は対象文字、欠損文字、表示文字の作成をする。