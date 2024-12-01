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

cursor = db.cursor()

def submitact():
    r = int(Rollno.get())
    cursor.execute("SELECT * FROM students WHERE rno=%d" %r)
    res = cursor.fetchone()
    newWindow = Toplevel(root)
    
    newWindow.title("New Window")
    newWindow.geometry("300x300")
    
    lblfstrow = tk.Label(newWindow, text="Name : ")
    lblfstrow.place(x=50, y=20)
    Name=tk.Entry(newWindow, width=35)
    Name.place(x=150, y=20, width=100)
    Name.insert(tk.END, res[1])
    
    lblsecrow = tk.Label(newWindow, text="Class : ")
    lblsecrow.place(x=50, y=50)
    Class=tk.Entry(newWindow, width=35)
    Class.place(x=150, y=50, width=100)
    Class.insert(tk.END, res[2])
    
    lbltrdrow = tk.Label(newWindow, text="College : ")
    lbltrdrow.place(x=50, y=80)
    College=tk.Entry(newWindow, width=35)
    College.place(x=150, y=80, width=100)
    College.insert(tk.END, res[3])
    
    SubmitBtn = tk.Button(newWindow, text="Update", bg='grey', command= lambda: update(r))
    SubmitBtn.place(x=150, y=135, width=55)
    
    def update(r):
        nm = Name.get()
        cls = Class.get()
        clg = College.get()
        
        qry = "UPDATE students SET name='%s', class='%s', college='%s' WHERE rno='%d'" %(nm, cls, clg, r)
        cursor.execute(qry)
        db.commit()
        
        messagebox.showinfo("Database Accessed", "Record Updated")
        newWindow.destroy()
        root.destroy()
        
root = tk.Tk()
root.geometry("300x300")

lbl = tk.Label(root, text="Roll no: ")
lbl.place(x=50, y=20)
Rollno = tk.Entry(root, width=55)
Rollno.place(x=150, y=20, width=100)

submitBtn = tk.Button(root, text="View", bg='grey', command=submitact)
submitBtn.place(x=150, y=80, width=55)

mainloop()