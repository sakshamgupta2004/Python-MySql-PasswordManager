from tkinter import *
import tkinter as tk
from tkinter import messagebox
import hashlib
import mysql.connector

root = Tk()
conn = mysql.connector.connect(host="localhost", port=3306, user="root", passwd="password_here")

def goToMainPage():
    root.destroy()
    import MainPage
    pass


def createUser(username, passHash):
    if not conn.is_connected():
        conn.connect()
    conn.database = "projectdb"
    conn.cursor().execute("INSERT into pm_users (username, password) VALUES ('" + username + "', '" + passHash + "')")

    conncursor = conn.cursor()
    conncursor.execute("SELECT EXISTS(SELECT * from pm_users where username='" + username + "' and password='" + passHash + "')")
    data = conncursor.fetchone()
    if data[0] == 1:
        return True
    else:
        return False


def LoginButtonPress():
    username = str(usernameBox.get())
    password = str(passwordBox.get())
    if len(username) > 2000:
        tk.messagebox.showerror(title="Error", message="Username too long")
    elif username.lower() == "guest":
        tk.messagebox.showerror(title="Invalid Username", message="Username cannot be guest")
    elif len(password) > 40:
        tk.messagebox.showerror(title="Error", message="Password too long")
    elif len(password) < 8:
        tk.messagebox.showerror(title="Error", message="Password too short")
    else:
        result = hashlib.sha512(password.encode())
        passHash = result.hexdigest()
        if not conn.is_connected():
            conn.connect()
        conn.database = "projectdb"
        myCursor = conn.cursor()
        myCursor.execute("SELECT EXISTS(SELECT * from pm_users where username='" + username + "');")
        data = myCursor.fetchone()
        if int(data[0]) == 1:
            myCursor1 = conn.cursor()
            myCursor1.execute("SELECT password from pm_users where username='" + username + "'")
            data1 = myCursor1.fetchone()
            if str(data1[0]) == passHash:
                username_save_file = f'username.cred'
                with open(username_save_file, 'w') as f:
                    f.write(username)
                password_save_file = f'password.cred'
                with open(password_save_file, 'w') as f:
                    f.write(password)

                goToMainPage()
            else:
                tk.messagebox.showerror(title="Wrong password!", message="Either username or password is wrong")
        else:
            result = tk.messagebox.askquestion(title="Create User", message="User not found. Create new user?")
            if result == 'yes':
                if createUser(username, passHash):
                   username_save_file = f'username.cred'
                   with open(username_save_file, 'w') as f:
                       f.write(username)
                   password_save_file = f'password.cred'
                   with open(password_save_file, 'w') as f:
                       f.write(password)
                   goToMainPage()
                else:
                    tk.messagebox.showerror(title="Failed", message="Failed to create account. \n"
                                                                    "Please make sure your PC is connected to the internet and try again.")
    pass


user_prefill = ""
pass_prefill = ""

try :
   user_file = f'username.cred'
   pass_file = f'password.cred'
   with open(user_file, 'r') as f:
       user_prefill = f.read()
   with open(pass_file, 'r') as f:
       pass_prefill = f.read()
except :
    pass



loginFrame = LabelFrame(root, pady = 20, padx = 20, borderwidth = 0, highlightthickness = 0)
loginFrame.pack(pady = 20, padx = 20)
loginFrame.configure(bg="white")
head = Label(loginFrame, text="Register/Login", pady=5, padx = 5)
head.config(font=("Ariel", 20))
head.configure(bg = "white")
head.pack()
usernameFrame = LabelFrame(loginFrame, text = "Email Id", padx = 5, pady = 5)
usernameFrame.configure(bg="white")
usernameBox = Entry(usernameFrame, width = 40, borderwidth = 2)
usernameBox.insert(0, user_prefill)
usernameBox.pack()
usernameFrame.pack()
passwordFrame = LabelFrame(loginFrame, text = "Password", padx = 5, pady = 5)
passwordFrame.configure(bg="white")
passwordBox = Entry(passwordFrame, show="*", width = 40, borderwidth = 2)
passwordBox.insert(0, pass_prefill)
passwordBox.pack()
passwordFrame.pack(pady=10)

loginButtonFrame = LabelFrame(loginFrame, borderwidth = 0, highlightthickness = 0, pady = 10)
loginButtonFrame.configure(bg="white")
loginButtonFrame.pack()
loginButton = Button(loginButtonFrame, text = "Login", padx=2, command = LoginButtonPress)
loginButton.pack()

loginFrame.update()
root.update()
maxwidth=root.winfo_width()




root.wm_title("Password Manager : Login")
root.update()
root.wm_minsize(maxwidth, root.winfo_height())
root.wm_maxsize(maxwidth, root.winfo_height())
root.configure(bg="#FFFFFF")
root.lift()
root.mainloop()