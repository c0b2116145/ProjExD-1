import random, time

all_quiz = ["サザエの旦那の名前は？","カツオの妹の名前は？","タラオ䛿カツオから見てどんな関係？"]
all_answer = [["マスオ","ますお"], ["ワカメ","わかめ"], ["甥","おい","甥っ子","おいっこ"]]

QA = dict()
for Q, A in zip(all_quiz,all_answer):
    QA[Q] = A

quiz = random.choice(all_quiz)
print(f"問題：{quiz}")
print("正解するまで回答し続けよう。（やめたくなったら’q’と回答してください）")

user_ans_num = 0
time_start = time.time()

while True:
    user_ans_num += 1
    user_ans = input(f"{user_ans_num}回目の回答：")
    if user_ans in QA[quiz]:
        print("正解！")
        break
    elif user_ans == "q":
        print("チャレンジ失敗")
        break
    else:
        print("出直してこい")


time_end = time.time()

time_total = time_end-time_start

print(f"あなたは{user_ans_num}回答えたよ～")
print(f"所要時間は{round(time_total)}秒だね！")