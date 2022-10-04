import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    btn = event.widget
    num = btn["text"]
    entry.insert(tk.END,num)

def equal(event):
    siki = entry.get()
    ans = eval(siki)
    entry.delete(0,tk.END)
    entry.insert(tk.END,ans)

root = tk.Tk()
root.title("電卓")
root.geometry("300x580")

entry = tk.Entry(root, width=10,font=("Times New Roman",40),justify="right")
entry.grid(column=0,row=0,columnspan=3)


num = 9
for i in range(4):
    for j in range(3):
        button = tk.Button(root,text=f"{num}",height=2,width=4,font=("Times New Roman", 30))
        button.bind("<1>",button_click)
        if num >= 0:
            button.grid(column=j,row=i+1)
            num -= 1

button = tk.Button(root,text="+",height=2,width=4,font=("Times New Roman", 30))
button.bind("<1>",button_click)
button.grid(column=1,row=4)

button = tk.Button(root,text="=",height=2,width=4,font=("Times New Roman", 30))
button.bind("<1>",equal)
button.grid(column=2,row=4)

root.mainloop()