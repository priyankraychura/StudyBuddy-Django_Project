import tkinter as tk
import mysql.connector
from tkinter import *
from tkinter import messagebox

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb"
)

curosr = db.cursor()

def submitact():
    r = int(Rollno.get())
    curosr.execute("DELETE FROM students WHERE rno=%d" %r)
    db.commit()
    root.destroy()
    
root = tk.Tk()
root.geometry("300x300")
root.title("Delete Record")

lbl = tk.Label(root, text="Rollno: ")
lbl.place(x=50, y=20)
Rollno = tk.Entry(root, width=35)
Rollno.place(x=150, y=20, width=100)

submitBtn = tk.Button(root, text="Delete", bg='grey', command=submitact)
submitBtn.place(x=150, y=80, width=55)

mainloop()