import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    btn = event.widget
    txt = btn["text"]
    tkm.showinfo(txt, f"[{txt}]ボタンが押されました")

root = tk.Tk()
root.geometry("300x500")

num = 9
for i in range(4):
    for j in range(3):
        button = tk.Button(root,text=f"{num}",height=2,width=4,font=("Times New Roman", 30), command=button_click)
        button.bind("<1>",button_click)
        if num >= 0:
            button.grid(column=j,row=i)
            num -= 1


root.mainloop()