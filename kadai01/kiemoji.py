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