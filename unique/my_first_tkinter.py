from tkinter import *
from tkinter import messagebox
root = Tk()
def click():
    num1 = enter.get()
    num2 = enter2.get()
    num1 = int(num1)
    num2 = int(num2)
    result = num1 + num2
    messagebox.showinfo("Result", result)
root.title('Calculator')
root.geometry("400x200")
btn = Button(root, text='Print',background='#555', foreground='#ccc',command=click)
enter = Entry(root)
enter2 = Entry(root)
btn.place(x=50, y=80)
enter.place(x=10, y=10)
enter2.place(x=10, y=50)
root.mainloop()
