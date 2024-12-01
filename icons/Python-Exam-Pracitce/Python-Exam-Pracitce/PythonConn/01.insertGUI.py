# insert record through form
import tkinter as tk
import mysql.connector
from tkinter import *
from tkinter import messagebox

def submitact():
    nm = Name.get()
    cls = Class.get()
    clg = College.get()
    insert(nm, cls, clg)
    
def insert(nm, cls, clg):
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "mydb"
    )
    
    cursor = db.cursor()
    
    qry = "INSERT INTO students (name, class, college) VALUES(%s, %s, %s)"
    val = (nm, cls, clg)
    cursor.execute(qry, val)
    db.commit()
    messagebox.showinfo("Database accessed", "Record inserted successfully")
    root.destroy()

root = tk.Tk()
root.geometry("300x300")
root.title("Insert Recored")

lblfstrow = tk.Label(root, text="Name = ")
lblfstrow.place(x = 50, y = 20)
Name = tk.Entry(root, width=35)
Name.place(x=150, y=20, width=100)

lblsecrow = tk.Label(root, text="Class = ")
lblsecrow.place(x=50, y=50)
Class = tk.Entry(root, width=35)
Class.place(x=150, y=50, width=100)

lbltrdrow = tk.Label(root, text="College")
lbltrdrow.place(x=50, y=80)
College = tk.Entry(root, width=35)
College.place(x=150, y=80, width=100)

submitbtn = tk.Button(root, text="Insert", bg='grey', command=submitact)
submitbtn.place(x=150, y=135, width=55)

root.mainloop()