from tkinter import *
import tkinter as tk
from tkinter import messagebox
import mysql.connector

selected_index = 0
stored_passes_ids = []
username = ""

user_file = f'username.cred'
with open(user_file, 'r') as f:
    username = f.read()


def onselect(evt):
    global selected_index

    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    selected_index = index
    display_stored_pass(index, value)


options = [
    "Mail",
    "Social Media",
    "Other"
]
window = tk.Tk()
window.title("Password Manager")

top_left = tk.Frame(window)
top_right = tk.Frame(window)

options1 = [
    "All",
    "Mail",
    "Social Media",
    "Other"
]

tk.Label(top_left, text='Filter').pack(side=tk.TOP, padx=20, anchor="w")
clicked1 = StringVar()
clicked1.set("All")
drop1 = OptionMenu(top_left, clicked1, *options1, command=lambda x: refresh_list())
drop1.pack(side=tk.TOP, padx=20, anchor="w")

tk.Label(top_left, text='Search').pack(fill=tk.Y, padx=(30, 0), pady=(20, 0), anchor="w")
searchbar = tk.Entry(top_left, width=25, font="Helvetica 13")
searchbar.config(background="#F4F6F7", highlightbackground="grey")
searchbar.pack(side=tk.TOP, fill=tk.Y, padx=(10, 0), pady=(0, 10))
searchbar.bind('<Return>', lambda x: search())

list_stored_passes = Listbox(top_left, height=35, width=25, font="Helvetica 14")
list_stored_passes.bind('<<ListboxSelect>>', onselect)
list_stored_passes.pack(side=tk.TOP, fill=tk.Y, padx=(10, 0), pady=(10, 10))

scroll_list = tk.Scrollbar(top_left)
scroll_list.pack(side=tk.RIGHT, fill=tk.Y)
scroll_list.config(command=list_stored_passes.yview)
list_stored_passes.config(yscrollcommand=scroll_list.set, cursor="hand2", background="#fff5e6",
                          highlightbackground="grey", bd=0, selectbackground="#c9b922")

text_frame = tk.Frame(top_right)

clicked = StringVar()
clicked.set("Mail")
drop = OptionMenu(text_frame, clicked, *options)
drop.pack(side=tk.TOP, anchor="e")

tk.Label(text_frame, text='Username').pack(fill=tk.Y, padx=(0, 5), pady=(0, 0), anchor="w")
username_entry = tk.Entry(text_frame, width=52, font="Helvetica 13")
username_entry.config(background="#F4F6F7", highlightbackground="grey")
username_entry.pack(side=tk.TOP, pady=(0, 5), padx=(0, 10))

scroll_text = tk.Frame(text_frame)
scroll_text.pack(side=tk.RIGHT, fill=tk.Y)
tk.Label(text_frame, text='Password').pack(fill=tk.Y, padx=(0, 5), pady=(0, 0), anchor="w")
password_entry = tk.Entry(text_frame, width=52, font="Helvetica 13")
password_entry.config(background="#F4F6F7", highlightbackground="grey")
password_entry.pack(side=tk.TOP, fill=tk.Y, padx=(0, 5), pady=(0, 10))

text_frame.pack(side=tk.TOP)

button_frame = tk.Frame(top_right)
photo_add = PhotoImage(file="add.jpeg")
photo_edit = PhotoImage(file="edit.jpeg")
photo_delete = PhotoImage(file="delete.jpeg")

btn_save = tk.Button(button_frame, text="Add", command=lambda: save_stored_pass(), image=photo_add)
btn_edit = tk.Button(button_frame, text="Update", command=lambda: update_stored_pass(), state=tk.DISABLED,
                     image=photo_edit)
btn_delete = tk.Button(button_frame, text="Delete", command=lambda: delete_stored_pass(), state=tk.DISABLED,
                       image=photo_delete)

btn_save.grid(row=0, column=1)
btn_edit.grid(row=0, column=2)
btn_delete.grid(row=0, column=3)

button_frame.pack(side=tk.TOP)

top_left.pack(side=tk.LEFT)
top_right.pack(side=tk.RIGHT)

import db_conn_settings

conn = mysql.connector.connect(host=db_conn_settings.getHost(), port=db_conn_settings.getPort(),
                               user=db_conn_settings.getUser(), passwd=db_conn_settings.getPassword())


def db_insert_stored_pass(conn, user, key):
    conn.database = "projectdb"
    if not conn.is_connected():
        conn.connect()
    mycursor = conn.cursor()
    query = "INSERT INTO tb_keys (user, pass, type, email) VALUES (%s, %s, %s, %s)"
    val = (user, key, clicked.get(), username)
    mycursor.execute(query, val)
    conn.commit()
    return mycursor.lastrowid


def db_select_all_stored_passes(conn):
    conn.database = "projectdb"
    if not conn.is_connected():
        conn.connect()
    query = "SELECT key_id, user, pass, type from tb_keys where email='" + username + "'"
    mycursor = conn.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()


def db_select_specific_stored_pass(conn, key_id):
    conn.database = "projectdb"
    if not conn.is_connected():
        conn.connect()
    mycursor = conn.cursor()
    mycursor.execute("SELECT user, pass, type FROM tb_keys WHERE user = '" + key_id + "'")
    return mycursor.fetchone()


def db_update_stored_pass(conn, user, key, key_id):
    conn.database = "projectdb"
    if not conn.is_connected():
        conn.connect()
    mycursor = conn.cursor()
    print(clicked.get())
    query = "UPDATE tb_keys SET user = %s, pass = %s, type = %s WHERE key_id = %s"
    val = (user, key, clicked.get(), key_id)
    mycursor.execute(query, val)
    conn.commit()


def db_delete_stored_pass(conn, key_id):
    conn.database = "projectdb"
    if not conn.is_connected():
        conn.connect()
    mycursor = conn.cursor()
    query = "DELETE FROM tb_keys WHERE key_id = %s"
    adr = (key_id,)
    mycursor.execute(query, adr)
    conn.commit()


def search():
    refresh_list(searchbar.get())
    searchbar.delete(0, tk.END)


def refresh_list(search_str=""):
    global conn
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    clicked.set("Mail")
    list_stored_passes.delete(0, tk.END)
    stored_passes_ids.clear()
    init(conn, search_str)


def init(conn, search_str=""):
    notes = db_select_all_stored_passes(conn)

    for note in notes:
        if note[3] == clicked1.get() or clicked1.get() == 'All':
            if str(note[1]).__contains__(search_str) or str(note[2]).__contains__(search_str) or str(
                    note[3]).__contains__(search_str):
                list_stored_passes.insert(tk.END, note[1])
                stored_passes_ids.append(note[0])


init(conn)


def save_stored_pass():
    global conn
    username = username_entry.get()

    if len(username) < 1:
        tk.messagebox.showerror(title="Error", message="You must enter the username")
        return

    if len(username) > 200000:
        tk.messagebox.showerror(title="Error", message="Username too long. Unable to Save")
        return

    stored_pass = password_entry.get()
    if len(stored_pass.rstrip()) < 1:
        tk.messagebox.showerror(title="Error", message="You must enter the password")
        return
    if len(stored_pass) > 200000:
        tk.messagebox.showerror(title="Error", message="Password too long. Unable to Save")
        return

    username_exist = False
    existing_usernames = list_stored_passes.get(0, tk.END)

    for t in existing_usernames:
        if t == username:
            username_exist = True
            break

    if username_exist is True:
        tk.messagebox.showerror(title="Error", message="Username already exists. Please enter a unique username")
        return

    inserted_id = db_insert_stored_pass(conn, username, stored_pass)
    print("Last inserted id is: " + str(inserted_id))
    if clicked.get() == clicked1.get() or clicked1.get() == "All":
        list_stored_passes.insert(tk.END, username)

    stored_passes_ids.append(inserted_id)

    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    clicked.set("Mail")


def update_stored_pass():
    global selected_index, conn

    username = username_entry.get()

    if len(username) < 1:
        tk.messagebox.showerror(title="Error", message="You must enter the username")
        return

    if len(username) > 200000:
        tk.messagebox.showerror(title="Error", message="Username too long. Unable to Update")
        return

    stored_pass = password_entry.get()
    if len(stored_pass.rstrip()) < 1:
        tk.messagebox.showerror(title="Error", message="You must enter the password")
        return
    if len(stored_pass) > 200000:
        tk.messagebox.showerror(title="Error", message="Password too long. Unable to Update")
        return

    stored_pass_id = stored_passes_ids[selected_index]

    db_update_stored_pass(conn, username, stored_pass, stored_pass_id)

    try:
        list_stored_passes.delete(list_stored_passes.get(0, tk.END).index(username_entry.get()))
    except:
        pass
    if clicked.get() == clicked1.get() or clicked1.get() == "All":
        list_stored_passes.insert(selected_index, username)

    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    clicked.set("Mail")


def delete_stored_pass():
    global selected_index, conn, stored_passes_ids
    username = username_entry.get()
    stored_passes = password_entry.get()

    print("Selected stored_pass is: " + str(selected_index))

    if len(username) < 1 or len(stored_passes.rstrip()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="Please select a entry to delete")
        return

    result = tk.messagebox.askquestion("Delete", "Are you sure you want to delete the stored password?", icon='warning')

    if result == 'yes':
        stored_pass_id = stored_passes_ids[selected_index]
        db_delete_stored_pass(conn, stored_pass_id)
        del stored_passes_ids[selected_index]

        try:
            list_stored_passes.delete(list_stored_passes.get(0, tk.END).index(username_entry.get()))
        except:
            pass
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        clicked.set("Mail")


def display_stored_pass(index, value):
    global stored_passes_ids, conn
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    stored_pass = db_select_specific_stored_pass(conn, value)
    username_entry.insert(tk.END, stored_pass[0])
    password_entry.insert(tk.END, stored_pass[1])
    clicked.set(stored_pass[2])

    btn_delete.config(state=tk.NORMAL)
    btn_edit.config(state=tk.NORMAL)


window.update()
window.wm_maxsize(window.winfo_width(), 400)
window.wm_minsize(window.winfo_width(), 400)
window.lift()
window.mainloop()
