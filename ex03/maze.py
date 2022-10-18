import tkinter as tk


if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")

    c = tk.Canvas(root,width=1500,height=900,bg="black")
    c.pack()
    
    root.mainloop()