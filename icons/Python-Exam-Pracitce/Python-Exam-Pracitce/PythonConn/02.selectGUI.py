from tkinter import *
import mysql.connector

def showROll(r):
    print(r)
    Tk.update(self=root)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydb"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM students")
myresult = mycursor.fetchall()

total_rows = mycursor.rowcount
total_column = len(myresult[0])

root = Tk()

for i in range(total_rows):
    for j in range(total_column):
        e = Label(root, relief="groove", text=myresult[i][j], width=20, fg='blue', font=("Arial", 13, "bold"))
        e.grid(row=i, column=j)
        Del = Button(root, relief="groove", text=f"Delete", width=20,  fg='blue', font=("Arial", 13, "bold"), command= lambda: showROll(myresult[i][0]))
        Del.grid(row=i, column=j+1)
        
root.mainloop()

#  flat, groove, raised, ridge, solid, or sunken