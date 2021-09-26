from tkinter import *
import tkinter.font
import datetime
import tkinter.messagebox
from datetime import timedelta
import os
import hashlib
import binascii
from PIL import ImageTk, Image


def login_in():
    global id_input_login
    global password_input_login
    global login_menu

    login_menu = Tk()
    login_menu.wm_title("Login")
    login_menu.minsize(240, 180)
    login_menu.maxsize(240, 180)
    login_menu.resizable(0, 0)
    k_font = tkinter.font.Font(
        family='Times new roman', size=10, weight=tkinter.font.BOLD)

    id_label = Label(login_menu, text="Your ID")
    password_label = Label(login_menu, text="Password")
    id_input_login = Entry(login_menu)
    password_input_login = Entry(login_menu)
    loginbutton1 = Button(login_menu, command=login_check, text=" Login ",
                          bg='red', height=1, width=7, font=k_font)
    registerbutton = Button(login_menu, command=register_in, text=" Register ",
                            bg='pale turquoise', height=1, width=7, font=k_font)
    feedbackbutton = Button(login_menu, command=feedback_read,
                            text=" Feedback ", bg='red', height=1, width=7, font=k_font)
    adminbutton = Button(login_menu, command=admin_in, text=" Admin Login ",
                         bg='pale turquoise', height=1, width=10, font=k_font)
    password_input_login.config(show="*")

    id_label.grid(row=0, sticky=E)
    id_input_login.grid(row=0, column=1)
    password_label.grid(row=1, sticky=E)
    password_input_login.grid(row=1, column=1)
    loginbutton1.grid(columnspan=2)
    registerbutton.grid(columnspan=2)
    feedbackbutton.grid(columnspan=2)
    adminbutton.grid(columnspan=2)

    login_menu.mainloop()


def login_check():
    global id
    id = id_input_login.get()
    password = password_input_login.get()

    pos = binary_search('index.txt', id)
    if pos == -1:
        tkinter.messagebox.showinfo(
            "Login", " Username is incorrect.Please re enter")
        return(login_in)
    else:
        f2 = open('Userprofile.txt', 'r')
        f2.seek(int(pos))
        l = f2.readline()
        l = l.rstrip()
        word = l.split('|')
        if(verify_password(word[1], password)):
            tkinter.messagebox.showinfo("Login", "Login Successful!")
            login_menu.destroy()
            Main_Menu()
        else:
            tkinter.messagebox.showinfo(
                "Login", " Password that you have entered is incorrect.Please reenter")
            return(login_in)
        f2.close()


def register_in():
    global id_input
    global name_input
    global email_input
    global password_input
    global register_menu

    register_menu = Tk()
    register_menu.wm_title("Register")
    register_menu.minsize(250, 350)
    register_menu.maxsize(250, 350)
    register_menu.resizable(0, 0)
    k_font = tkinter.font.Font(
        family='Times new roman', size=10, weight=tkinter.font.BOLD)

    id_label = Label(register_menu, text="Your ID")
    name_label = Label(register_menu, text="Full Name")
    email_label = Label(register_menu, text="Email")
    password_label = Label(register_menu, text="Password")
    id_input = Entry(register_menu)
    name_input = Entry(register_menu)
    email_input = Entry(register_menu)
    password_input = Entry(register_menu)
    loginbutton1 = Button(register_menu, command=login_in, text=" Login ",
                          bg='red', height=1, width=7, font=k_font)
    registerbutton = Button(register_menu, command=register_check,
                            text=" Register ", bg='DarkSlateGray3', height=1, width=7, font=k_font)
    password_input.config(show="*")

    id_label.grid(row=0, sticky=E)
    id_input.grid(row=0, column=1)
    name_label.grid(row=1, sticky=E)
    name_input.grid(row=1, column=1)
    email_label.grid(row=2, sticky=E)
    email_input.grid(row=2, column=1)
    password_label.grid(row=3, sticky=E)
    password_input.grid(row=3, column=1)
    registerbutton.grid(columnspan=2)
    loginbutton1.grid(columnspan=2)

    register_menu.mainloop()


def register_check():
    global id

    id = id_input.get()
    name = name_input.get()
    email = email_input.get()
    password = password_input.get()

    if len(id) == 0 or len(name) == 0 or len(email) == 0 or len(password) == 0:
        tkinter.messagebox.showinfo(
            "Register", "You left one or more fields blank O_O")
        register_menu.lift()
        return(register_in)

    pos = binary_search('index.txt', id)
    if pos != -1:
        tkinter.messagebox.showinfo(
            "Register", "Already registered. Choose a different ID")
        register_menu.destroy()

    f2 = open('Userprofile.txt', 'a')
    pos = f2.tell()
    f3 = open('index.txt', 'a')
    buf = id + '|' + hash_password(password) + \
        '|' + name + '|' + email + '|' + '#'
    f2.write(buf)
    f2.write('\n')
    buf = id + '|' + str(pos) + '|' + '#'
    f3.write(buf)
    f3.write('\n')
    f3.close()
    f2.close()
    key_sort('index.txt')
    tkinter.messagebox.showinfo("Register", "Registration Successful!")
    register_menu.destroy()


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def admin_in():
    global id_admin
    global password_admin
    global admin_menu

    admin_menu = Tk()
    admin_menu.wm_title("Admin")
    admin_menu.minsize(250, 100)
    admin_menu.maxsize(250, 100)
    admin_menu.resizable(0, 0)
    k_font = tkinter.font.Font(
        family='Times new roman', size=10, weight=tkinter.font.BOLD)

    admin_label = Label(admin_menu, text="Admin ID")
    admin_password_label = Label(admin_menu, text="Password")
    id_admin = Entry(admin_menu)
    password_admin = Entry(admin_menu)
    loginbutton2 = Button(admin_menu, command=admin_check, text=" Login ",
                          bg='red', height=1, width=7, font=k_font)
    password_admin.config(show="*")

    admin_label.grid(row=0, sticky=E)
    id_admin.grid(row=0, column=1)
    admin_password_label.grid(row=3, sticky=E)
    password_admin.grid(row=3, column=1)
    loginbutton2.grid(columnspan=2)

    admin_menu.mainloop()


def admin_check():
    global admin_id

    admin_id = id_admin.get()
    admin_password = password_admin.get()

    if admin_id == "admin" and admin_password == "admin":
        tkinter.messagebox.showinfo("Login", "Admin Login Successful!")
        admin_menu.destroy()
        login_menu.destroy()
        Admin_Opt()
    else:
        tkinter.messagebox.showinfo(
            "Login", "Admin id or password INCORRECT. Please reenter")


def Admin_Opt():
    global opt_menu

    opt_menu = Tk()
    opt_menu.wm_title("Admin_menu")
    opt_menu.minsize(350, 120)
    opt_menu.maxsize(350, 120)
    opt_menu.resizable(0, 0)
    k_font = tkinter.font.Font(
        family='Times new roman', size=10, weight=tkinter.font.BOLD)

    addbutton = Button(opt_menu, command=add_clothes, text=" Add New Clothes ",
                       bg='pale green', height=1, width=12, font=k_font)
    delbutton = Button(opt_menu, command=del_clothes, text=" Remove Clothes ",
                       bg='steel blue', height=1, width=12, font=k_font)
    backbutton = Button(opt_menu, command=reopen_login, text=" Log out ",
                        bg='yellow', height=1, width=12, font=k_font)

    addbutton.grid(row=4, column=4)
    delbutton.grid(row=4, column=9)
    backbutton.grid(row=10, column=6)

    opt_menu.mainloop()


def reopen_login():
    tkinter.messagebox.showinfo("Login", "Admin Logout Successful!")
    opt_menu.destroy()

    f7 = open('clothIndex.txt', 'r')
    lines1 = f7.readlines()
    f7.close()
    f8 = open('clothIndex.txt', 'w')
    for line1 in lines1:
        if line1.startswith('*'):
            continue
        else:
            f8.write(line1)
    f8.close()

    login_in()


def key_sort(fname):
    t = list()
    fin = open(fname, 'r')
    for line in fin:
        line = line.rstrip('\n')
        words = line.split('|')
        t.append((words[0], words[1]))
    fin.close()
    t.sort()
    with open("temp.txt", 'w') as fout:
        for pkey, addr in t:
            pack = pkey+"|"+addr+"|#"
            fout.write(pack+'\n')
    os.remove(fname)
    os.rename("temp.txt", fname)


def binary_search(fname, search_key):
    t = []
    fin = open(fname, 'r')
    for lx in fin:
        lx = lx.rstrip()
        wx = lx.split('|')
        t.append((wx[0], wx[1]))
    fin.close()
    l = 0
    r = len(t) - 1
    while l <= r:
        mid = (l + r)//2
        if t[mid][0] == search_key:
            return int(t[mid][1])
        elif t[mid][0] <= search_key:
            l = mid + 1
        else:
            r = mid - 1
    return -1


def add_clothes():
    global clothes_id
    global clothes_name
    global brand_name
    global add_menu
    global image
    global image_lable

    add_menu = Tk()
    add_menu.wm_title("Add")
    add_menu.minsize(300, 250)
    add_menu.maxsize(300, 250)
    add_menu.resizable(0, 0)
    k_font = tkinter.font.Font(
        family='Times new roman', size=10, weight=tkinter.font.BOLD)

    clothes_id_label = Label(add_menu, text="Cloth ID (Should be 5 digit)")
    clothes_label = Label(add_menu, text="Brand Name")
    Model_label = Label(add_menu, text="Model Name")
    image_lable = Label(add_menu, text="Image")
    clothes_id = Entry(add_menu)
    clothes_name = Entry(add_menu)
    brand_name = Entry(add_menu)
    image = Entry(add_menu)
    addbutton1 = Button(add_menu, command=add_check, text=" Add ",
                        bg='ghost white', height=1, width=10, font=k_font)

    clothes_id_label.grid(row=0, sticky=E)
    clothes_id.grid(row=0, column=1)
    clothes_label.grid(row=1, sticky=E)
    clothes_name.grid(row=1, column=1)
    Model_label.grid(row=2, sticky=E)
    brand_name.grid(row=2, column=1)
    image_lable.grid(row=3, sticky=E)
    image.grid(row=3, column=1)
    addbutton1.grid(columnspan=2)

    add_menu.mainloop()


def add_check():
    global b_id
    b_id = clothes_id.get()
    b_name = clothes_name.get().upper()
    a_id = brand_name.get()
    image_name = image.get()

    if len(b_name) == 0:
        tkinter.messagebox.showinfo(
            "Add Clothes", "You did not type a clothes name O_O")
        add_menu.lift()
        return(add_clothes)

    if len(b_id) != 5 or b_id.isdigit() == False:
        tkinter.messagebox.showinfo(
            "Add Clothes", "Please renter the details(ID should be 5 positive integers)")
        add_menu.lift()
        return(add_clothes)

    if len(a_id) == 0:
        a_id = "Anonymous"

    pos = binary_search('clothIndex.txt', b_id)
    if pos != -1:
        tkinter.messagebox.showinfo(
            "Clothes", "Clothes already present.Please try again")
        add_menu.lift()
        return(add_clothes)

    f22 = open('cloth.txt', 'a')
    pos = f22.tell()
    f33 = open('clothIndex.txt', 'a')
    buf = b_id + '|' + b_name + '|' + a_id + '|'  + 'Y' + '|'+ image_name+'|'+ '#'
    f22.write(buf)
    f22.write('\n')
    buf = b_id + '|' + str(pos) + '|' + '#'
    f33.write(buf)
    f33.write('\n')
    f33.close()
    f22.close()
    key_sort('clothIndex.txt')
    tkinter.messagebox.showinfo("Add", "Cloth added Successfully!")
    add_menu.destroy()


def del_clothes():
    global rb_id
    global del_menu

    del_menu = Tk()
    del_menu.wm_title("Delete")
    del_menu.minsize(1000, 600)
    del_menu.maxsize(1000, 600)
    del_menu.resizable(0, 0)
    k_font = tkinter.font.Font(
        family='Times new roman', size=10, weight=tkinter.font.BOLD)

    Id = []
    Title = []
    Model = []
    Availability = []

    f1 = open('clothIndex.txt', 'r')
    f = open("cloth.txt", 'r')
    norecord = 0
    for line in f1:
        if not line.startswith('*'):
            norecord += 1
            line = line.rstrip('\n')
            word = line.split('|')
            f.seek(int(word[1]))
            line1 = f.readline().rstrip()
            word1 = line1.split('|')
            Id.append(word1[0])
            Title.append(word1[1])
            Model.append(word1[2])
            Availability.append(word1[3])
    f.close()

    borrow_list = Listbox(del_menu, height=50, width=20)
    borrow_list2 = Listbox(del_menu, height=50, width=50)
    borrow_list3 = Listbox(del_menu, height=50, width=50)
    borrow_list4 = Listbox(del_menu, height=50, width=20)

    for num in range(0, norecord):
        borrow_list.insert(0, Id[num])
        borrow_list2.insert(0, Title[num])
        borrow_list3.insert(0, Model[num])
        borrow_list4.insert(0, Availability[num])

    b_label = Label(del_menu, text="Clothes ID")
    rb_id = Entry(del_menu)
    delbutton1 = Button(del_menu, command=del_check, text="Remove Clothes",
                        bg='dark orange', height=1, width=10, font=k_font)
    borrow_list2.configure(background="yellow")
    borrow_list3.configure(background="yellow")
    borrow_list.configure(background="red")
    borrow_list4.configure(background="red")
    borrow_label = Label(del_menu, text="Id")
    borrow_label2 = Label(del_menu, text="Title")
    borrow_label3 = Label(del_menu, text="Model")
    borrow_label4 = Label(del_menu, text="Availability")

    borrow_label.grid(row=6, column=0)
    borrow_label2.grid(row=6, column=1)
    borrow_label3.grid(row=6, column=3)
    borrow_label4.grid(row=6, column=6)

    borrow_list.grid(row=7, column=0)
    borrow_list2.grid(row=7, column=1)
    borrow_list3.grid(row=7, column=3)
    borrow_list4.grid(row=7, column=6)
    b_label.grid(row=0, sticky=E)
    rb_id.grid(row=0, column=1)
    delbutton1.grid(row=2, columnspan=1)

    del_menu.mainloop()


def del_check():

    global del_id
    del_id = rb_id.get()

    if len(del_id) == 0:
        tkinter.messagebox.showinfo(
            "Delete Clothes", "You did not type anything O_O")
        del_menu.lift()
        return(del_clothes)

    pos = binary_search('clothIndex.txt', del_id)
    if(pos == -1):
        tkinter.messagebox.showinfo(
            "Delete", "Clothes not present.Please reenter")
        del_menu.destroy()
        return(del_clothes)
    else:
        f = open('cloth.txt', 'r')
        f.seek(pos)
        l1 = f.readline().rstrip()
        w1 = l1.split('|')
        if(w1[3] == 'N'):
            tkinter.messagebox.showinfo(
                "Delete", "Clothes currently borrowed. Please try another Clothes")
            del_menu.destroy()
            return(del_clothes)

    index = -1

    with open('clothIndex.txt', 'r') as file:
        for line in file:
            words = line.split("|")
            if(words[0] == del_id):
                index = int(words[1])

    index = 0
    with open("clothIndex.txt", 'r+') as file:
        line = file.readline()
        while line:
            words = line.split("|")
            if words[0] == del_id:
                file.seek(index, 0)
                file.write("*")
                break
            else:
                index = file.tell()
                line = file.readline()
    tkinter.messagebox.showinfo("Delete", "Clothes Successfully removed")
    del_menu.destroy()


def Main_Menu():
    base = Tk()
    # Window title and size optimization
    base.wm_title("Clothes store")
    base.minsize(600, 600)

    in_font = tkinter.font.Font(
        family='Lucida Calligraphy', size=15, weight=tkinter.font.BOLD)
    current_time1 = datetime.datetime.now()
    current_time = str(current_time1)

    # Bunch of labels
    status = Label(base, text=("Date and time logged in: " +
                               current_time), bd=1, relief=SUNKEN, anchor=W, bg='light blue')
    orionLabel = Label(base, text="House Of Clothes", bg='brown1', font=(
        "Castellar", "50", "bold", "italic", "underline"), fg="black")
    welcomeLabel = Label(base, text=("Welcome! "+id),
                         font=("Freestyle Script", "50", "bold"))
    imageLibrary = PhotoImage(file="try1.gif")
    topFrame = Frame(base)
    bottomFrame = Frame(base)

    # Positioning of labels
    status.pack(side=BOTTOM, fill=X)
    orionLabel.pack(fill=X)
    welcomeLabel.pack()
    Label(base, image=imageLibrary).pack()
    topFrame.pack()
    bottomFrame.pack(side=BOTTOM)

    # Buttons
    borrow_but = Button(bottomFrame, bg="black", fg="white", text="Borrow Clothes",
                        font=in_font, height=5, width=15, command=borrow_in)
    buy_but1 = Button(bottomFrame, bg="RosyBrown2", text="Buy Clothes",
                      font=in_font, height=5, width=15, command=buy_in)
    return_but = Button(bottomFrame, bg="RosyBrown2", text="Return Clothes",
                        font=in_font, height=5, width=15, command=return_in)
    search_but = Button(bottomFrame, bg="RosyBrown2", text="Search for Clothes",
                        font=in_font, height=5, width=15, command=search_in)
    feed_but = Button(bottomFrame, bg="RosyBrown2", text="FeedBack",font=in_font, height=5, width=15, command=feedback_in)
    feedback_but = Button(bottomFrame, bg="black", fg="white", text="Check Purchased",
                          font=in_font, height=5, width=15, command=purchased)

    # Positioning of buttons
    borrow_but.pack(side=LEFT)
    buy_but1.pack(side=LEFT)
    return_but.pack(side=LEFT)
    search_but.pack(side=LEFT)
    feed_but.pack(side=LEFT)
    feedback_but.pack(side=LEFT)

    base.mainloop()


def buy_in():
    global borrow_entry1
    global borrow_menu

    borrow_menu = Tk()

    borrow_menu.wm_title("Buy")
    borrow_menu.minsize(900, 550)
    borrow_menu.maxsize(1200, 550)
    borrow_menu.resizable(0, 0)

    Id = []
    Title = []
    Model = []
    Availability = []

    f1 = open('clothIndex.txt', 'r')
    f = open("cloth.txt", 'r')
    norecord = 0
    for line in f1:
        if not line.startswith('*'):
            norecord += 1
            line = line.rstrip('\n')
            word = line.split('|')
            f.seek(int(word[1]))
            line1 = f.readline().rstrip()
            word1 = line1.split('|')
            Id.append(word1[0])
            Title.append(word1[1])
            Model.append(word1[2])
            Availability.append(word1[3])
    f.close()

    borrow_list = Listbox(borrow_menu, height=50, width=20)
    borrow_list1 = Listbox(borrow_menu, height=50, width=50)
    borrow_list2 = Listbox(borrow_menu, height=50, width=50)
    borrow_list3 = Listbox(borrow_menu, height=50, width=20)

    for num in range(0, norecord):
        borrow_list.insert(0, Id[num])
        borrow_list1.insert(0, Title[num])
        borrow_list2.insert(0, Model[num])
        borrow_list3.insert(0, Availability[num])

    borrow_list.configure(background="khaki3")
    borrow_list1.configure(background="lightSkyBlue2")
    borrow_list2.configure(background="lightSkyBlue2")
    borrow_list3.configure(background="khaki3")
    borrow_label1 = Label(borrow_menu, text="Please enter the Clothe ID that you wish to borrow", font=(
        "Times", "20", "bold", "italic"), bg="light blue")
    borrow_label = Label(borrow_menu, text="Id")
    borrow_label2 = Label(borrow_menu, text="Brand")
    borrow_label3 = Label(borrow_menu, text="Model")
    borrow_label4 = Label(borrow_menu, text="Availability")

    borrow_entry1 = Entry(borrow_menu, width=50)
    borrow_button1 = Button(borrow_menu, text="Buy", command=buy_check, font=(
        "Times new roman", "10", "bold"), bg="red")
    borrow_button2 = Button(borrow_menu, text="View Image", command=view_img, font=(
        "Times new roman", "10", "bold"), bg="red")

    borrow_label1.grid(row=0, columnspan=20)
    borrow_label.grid(row=5, column=0)
    borrow_label2.grid(row=5, column=1)
    borrow_label3.grid(row=5, column=4)
    borrow_label4.grid(row=5, column=7)

    borrow_entry1.grid(row=1, columnspan=20)
    borrow_button1.grid(row=2, columnspan=20)
    borrow_button2.grid(row=3, columnspan=20)
    borrow_list.grid(row=6, column=0)
    borrow_list1.grid(row=6, column=1)
    borrow_list2.grid(row=6 ,column=4)
    borrow_list3.grid(row=6, column=7)
    borrow_menu.mainloop()




def buy_check():
    date = datetime.date.today()
    enddate = date + timedelta(days=7)
    bclothes = borrow_entry1.get().upper()

    if len(bclothes) == 0:
        tkinter.messagebox.showinfo("BUY", "You did not type anything O_O")
        borrow_menu.lift()
        return(buy_in)

    pos = binary_search('clothIndex.txt', bclothes)
    if pos == -1:
        tkinter.messagebox.showinfo(
            "BUY", "The cloth ID that you had entered is not in our database,sorry,please enter a different Cloth ID")
        borrow_menu.lift()
    else:
        f2 = open('cloth.txt', 'r+')
        f2.seek(pos)
        l2 = f2.readline()
        l2 = l2.rstrip('\n')
        w2 = l2.split('|')
        if(w2[3] == 'Y'):
            l3 = w2[0] + '|' + w2[1] + '|' + w2[2] + '|' + 'P|' +w2[4]+ '|#'
            f2.seek(pos)
            f2.write(l3)
            f2.close()
            tkinter.messagebox.showinfo(
                "Purchased", "You have successfully purchased "+w2[1]+" Clothes")

            buf = id + '|' + bclothes + '|#\n'
            f3 = open('Purchase.txt', 'a')
            f3.write(buf)
            f3.close()
            key_sort('Purchase.txt')
            Done2 = tkinter.messagebox.askyesno(
                "Borrow", "Do you want to buy another set of Clothes?")
            if Done2 == True:
                borrow_menu.destroy()
                buy_in()
            else:
                borrow_menu.destroy()
        else:
            tkinter.messagebox.showinfo(
                "Borrow", "This Clothe is currently unavailable, please select another Cloth")
            borrow_menu.lift()


def borrow_in():
    global borrow_entry1
    global borrow_menu

    borrow_menu = Tk()

    borrow_menu.wm_title("Borrow")
    borrow_menu.minsize(900, 550)
    borrow_menu.maxsize(1200, 550)
    borrow_menu.resizable(0, 0)

    Id = []
    Title = []
    Model = []
    Availability = []

    f1 = open('clothIndex.txt', 'r')
    f = open("cloth.txt", 'r')
    norecord = 0
    for line in f1:
        if not line.startswith('*'):
            norecord += 1
            line = line.rstrip('\n')
            word = line.split('|')
            f.seek(int(word[1]))
            line1 = f.readline().rstrip()
            word1 = line1.split('|')
            Id.append(word1[0])
            Title.append(word1[1])
            Model.append(word1[2])
            Availability.append(word1[3])
    f.close()

    borrow_list = Listbox(borrow_menu, height=50, width=20)
    borrow_list1 = Listbox(borrow_menu, height=50, width=50)
    borrow_list2 = Listbox(borrow_menu, height=50, width=50)
    borrow_list3 = Listbox(borrow_menu, height=50, width=20)

    for num in range(0, norecord):
        borrow_list.insert(0, Id[num])
        borrow_list1.insert(0, Title[num])
        borrow_list2.insert(0, Model[num])
        borrow_list3.insert(0, Availability[num])

    borrow_list.configure(background="khaki3")
    borrow_list1.configure(background="lightSkyBlue2")
    borrow_list2.configure(background="lightSkyBlue2")
    borrow_list3.configure(background="khaki3")
    borrow_label1 = Label(borrow_menu, text="Please enter the Cloth ID that you wish to borrow", font=(
        "Times", "20", "bold", "italic"), bg="light blue")
    borrow_label = Label(borrow_menu, text="Id")
    borrow_label2 = Label(borrow_menu, text="Brand")
    borrow_label3 = Label(borrow_menu, text="Model")
    borrow_label4 = Label(borrow_menu, text="Availability")

    borrow_entry1 = Entry(borrow_menu, width=50)
    borrow_button1 = Button(borrow_menu, text="Borrow", command=borrow_check, font=(
        "Times new roman", "10", "bold"), bg="red")
    borrow_button2 = Button(borrow_menu, text="View Image", command=view_img, font=(
        "Times new roman", "10", "bold"), bg="red")

    borrow_label1.grid(row=0, columnspan=20)
    borrow_label.grid(row=5, column=0)
    borrow_label2.grid(row=5, column=1)
    borrow_label3.grid(row=5, column=4)
    borrow_label4.grid(row=5, column=7)

    borrow_entry1.grid(row=1, columnspan=20)
    borrow_button1.grid(row=2, columnspan=20)
    borrow_button2.grid(row=3, columnspan=20)
    borrow_list.grid(row=6, column=0)
    borrow_list1.grid(row=6, column=1)
    borrow_list2.grid(row=6 ,column=4)
    borrow_list3.grid(row=6, column=7)
    borrow_menu.mainloop()

def view_img():
    bbook=borrow_entry1.get().upper()
    pos = binary_search('clothIndex.txt', bbook)
    if pos == -1:
        tkinter.messagebox.showinfo("Borrow","The Cloth ID that you had entered is not in our database,sorry,please enter a different ID")
        borrow_menu.lift()
    else:
        f2 = open('cloth.txt', 'r+')
        f2.seek(pos)
        l2 = f2.readline()
        l2 = l2.rstrip('\n')
        w2 = l2.split('|')
        imageName = w2[4]
        print(imageName)

        image = Image.open(imageName)
        image.show()
def borrow_check():

    count = 0
    f = open('Record.txt', 'r')
    for l in f:
        l = l.split('|')
        if l[0] == id:
            count += 1
    if count >= 3:
        tkinter.messagebox.showinfo(
            "Borrow", "Cannot borrow more than 3 Clothes")
        borrow_menu.destroy()

    else:
        date = datetime.date.today()
        enddate = date + timedelta(days=7)
        bclothes = borrow_entry1.get().upper()

        if len(bclothes) == 0:
            tkinter.messagebox.showinfo(
                "Borrow", "You did not type anything O_O")
            borrow_menu.lift()
            return(borrow_in)

        pos = binary_search('clothIndex.txt', bclothes)
        if pos == -1:
            tkinter.messagebox.showinfo(
                "Borrow", "The Cloth ID that you had entered is not in our database,sorry,please enter a different Cloth")
            borrow_menu.lift()
        else:
            f2 = open('cloth.txt', 'r+')
            f2.seek(pos)
            l2 = f2.readline()
            l2 = l2.rstrip('\n')
            w2 = l2.split('|')
            if(w2[3] == 'Y'):
                l3 = w2[0] + '|' + w2[1] + '|' + w2[2] + '|' + 'N|' +w2[4]+ '|#'
                f2.seek(pos)
                f2.write(l3)
                f2.close()
                tkinter.messagebox.showinfo(
                    "Borrow", "The cloth you have selected has been successfully borrowed. Please return it by:" + '\n' + str(enddate))

                buf = id + '|' + bclothes + '|#\n'
                f3 = open('Record.txt', 'a')
                f3.write(buf)
                f3.close()
                key_sort('Record.txt')
                Done2 = tkinter.messagebox.askyesno(
                    "Borrow", "Do you want to borrow another cloth?")
                if Done2 == True:
                    borrow_menu.destroy()
                    borrow_in()
                else:
                    borrow_menu.destroy()
            else:
                tkinter.messagebox.showinfo(
                    "Borrow", "This cloth is currently unavailable, please select another cloth")
                borrow_menu.lift()


def return_in():
    global return_entry1
    global return_menu
    global record_verification

    return_menu = Tk()
    return_menu.minsize(900, 500)
    return_menu.maxsize(1200, 500)
    return_menu.wm_title("Return")
    return_menu.resizable(0, 0)

    Id = []
    Title = []
    Model = []
    Availability = []
    record_verification = []

    f = open("Record.txt")
    norecord = 0
    for line in f:
        line = line.rstrip()
        words = line.split('|')
        if(words[0] == id):
            pos = binary_search('clothIndex.txt', words[1])
            if pos != -1:
                norecord += 1
                f2 = open('cloth.txt', 'r')
                f2.seek(pos)
                l1 = f2.readline()
                l1 = l1.rstrip()
                w1 = l1.split('|')
                Id.append(w1[0])
                record_verification.append(w1[0])
                Title.append(w1[1])
                Model.append(w1[2])
                Availability.append(w1[3])
    f.close()

    return_list = Listbox(return_menu, height=50, width=20)
    return_list1 = Listbox(return_menu, height=50, width=50)
    return_list2 = Listbox(return_menu, height=50, width=50)
    return_list3 = Listbox(return_menu, height=50, width=20)

    for num in range(0, norecord):
        return_list.insert(0, Id[num])
        return_list1.insert(0, Title[num])
        return_list2.insert(0, Model[num])
        return_list3.insert(0, Availability[num])

    return_list.configure(background="khaki3")
    return_list1.configure(background="lightSkyBlue2")
    return_list2.configure(background="lightSkyBlue2")
    return_list3.configure(background="khaki3")
    return_label = Label(return_menu, text="Id")
    return_label2 = Label(return_menu, text="Title")
    return_label3 = Label(return_menu, text="Model")
    return_label4 = Label(return_menu, text="Availability")

    return_button1 = Button(return_menu, text="Return", command=return_check, font=(
        "Times new roman", "10", "bold"), bg="RosyBrown2")
    return_entry1 = Entry(return_menu, width=50)
    return_label1 = Label(return_menu, text=" Please enter the cloth ID that you wish to return ", font=(
        "Times", "12", "bold", "italic"), bg="light blue")
    return_label1.grid(row=0, columnspan=20)
    return_entry1.grid(row=1, columnspan=20)
    return_button1.grid(row=2, columnspan=20)

    return_label.grid(row=3, column=0)
    return_label2.grid(row=3, column=1)
    return_label3.grid(row=3, column=4)
    return_label4.grid(row=3, column=7)

    return_list.grid(row=4, column=0)
    return_list1.grid(row=4, column=1)
    return_list2.grid(row=4, column=4)
    return_list3.grid(row=4, column=7)

    return_menu.mainloop()


def purchased():
    global return_entry1
    global return_menu
    global record_verification

    return_menu = Tk()
    return_menu.minsize(900, 500)
    return_menu.maxsize(1200, 500)
    return_menu.wm_title("Purchased")
    return_menu.resizable(0, 0)

    Id = []
    Title = []
    Model = []
    Availability = []
    record_verification = []

    f = open("Purchase.txt")
    norecord = 0
    for line in f:
        line = line.rstrip()
        words = line.split('|')
        if(words[0] == id):
            pos = binary_search('clothIndex.txt', words[1])
            if pos != -1:
                norecord += 1
                f2 = open('cloth.txt', 'r')
                f2.seek(pos)
                l1 = f2.readline()
                l1 = l1.rstrip()
                w1 = l1.split('|')
                Id.append(w1[0])
                record_verification.append(w1[0])
                Title.append(w1[1])
                Model.append(w1[2])
                Availability.append(w1[3])
    f.close()

    return_list = Listbox(return_menu, height=50, width=20)
    return_list1 = Listbox(return_menu, height=50, width=50)
    return_list2 = Listbox(return_menu, height=50, width=50)
    return_list3 = Listbox(return_menu, height=50, width=20)

    for num in range(0, norecord):
        return_list.insert(0, Id[num])
        return_list1.insert(0, Title[num])
        return_list2.insert(0, Model[num])
        return_list3.insert(0, Availability[num])

    return_list.configure(background="khaki3")
    return_list1.configure(background="lightSkyBlue2")
    return_list2.configure(background="lightSkyBlue2")
    return_list3.configure(background="khaki3")
    return_label = Label(return_menu, text="Id")
    return_label2 = Label(return_menu, text="Brand")
    return_label3 = Label(return_menu, text="Model")
    #return_label4 = Label(return_menu, text="Availability")

  

    return_label.grid(row=3, column=0)
    return_label2.grid(row=3, column=1)
    return_label3.grid(row=3, column=4)
    #return_label4.grid(row=3, column=7)

    return_list.grid(row=4, column=0)
    return_list1.grid(row=4, column=1)
    return_list2.grid(row=4, column=4)
    #return_list3.grid(row=4, column=7)

    return_menu.mainloop()


def return_check():
    import datetime as dt
    from datetime import timedelta
    date = dt.date.today()
    bclothes = return_entry1.get().upper()

    if len(bclothes) == 0:
        tkinter.messagebox.showinfo("Return", "You did not type anything")
        return_menu.lift()
        return(return_in)

    if(bclothes in record_verification):
        pos = binary_search('clothIndex.txt', bclothes)
        if pos != -1:
            f1 = open('cloth.txt', 'r+')
            f1.seek(pos)
            l1 = f1.readline().rstrip()
            w1 = l1.split('|')
            if(w1[3] == 'N'):
                tkinter.messagebox.showinfo(
                    "Return", "The cloth you have selected has been successfully returned on"+'\n'+str(date))
                f1.seek(pos)
                line = w1[0] + '|' + w1[1] + '|' + w1[2] + '|Y|' + w1[4]+ '|#'
                f1.write(line)

                f2 = open('Record.txt', 'r')
                lines = f2.readlines()
                f2.close()
                f3 = open('Record.txt', 'w')
                for l2 in lines:
                    l3 = l2.split('|')
                    if l3[1] == bclothes and l3[0] == id:
                        continue
                    else:
                        f3.write(l2)
                f3.close()
                Done3 = tkinter.messagebox.askyesno(
                    "Return", "Do you want to return another cloth?")
                if Done3 == True:
                    f1.close()
                    return_menu.destroy()
                    return_in()
                else:
                    return_menu.destroy()
            else:
                tkinter.messagebox.showinfo(
                    "This cloth has been returned, please select another cloth")
            f1.close()
    else:
        tkinter.messagebox.showinfo(
            "Return", "The cloth that you had entered is invalid.Please reenter a different cloth")
        return_menu.lift()


def search_in():
    global search_entry
    global search_menu
    search_menu = Tk()

    search_menu.maxsize(500, 100)
    search_menu.maxsize(500, 100)
    search_menu.wm_title("Search")
    search_menu.resizable(0, 0)

    search_label1 = Label(search_menu, text="Search through our database to check if your desired cloth is available", font=(
        "Times", "12", "bold", "italic"), bg="red")
    search_label1.pack(side=TOP)

    search_entry = Entry(search_menu, width=50)
    search_entry.pack(side=TOP)

    search_button = Button(search_menu, text="Search", command=search_check, font=(
        "Times new roman", "10", "bold"), bg="RosyBrown2")
    search_button.pack(side=TOP)

    search_menu.mainloop()


def search_check():
    search_word = search_entry.get().upper()
    search_menu.destroy()

    if len(search_word) == 0:
        tkinter.messagebox.showinfo("Search", "You did not type anything O_O")
        return(search_in)

    pos = binary_search('clothIndex.txt', search_word)

    if (pos == -1):
        tkinter.messagebox.showinfo(
            "Search", "Sorry,this cloth does not exist in our database")
    else:
        search_menu2 = Tk()
        search_menu2.wm_title("Search")
        search_menu2.attributes("-topmost", True)
        tkinter.messagebox.showinfo("Search", "It is in our database!")

        search_result = Listbox(search_menu2, height=10, width=50)
        f2 = open('cloth.txt', 'r')
        f2.seek(pos)
        l1 = f2.readline()
        l1 = l1.rstrip()
        w1 = l1.split('|')
        b_id = w1[0]
        clothes = w1[1]
        Model = w1[2]
        if(w1[3] == 'Y'):
            availability = 'Available'
        else:
            availability = 'Unavailable'
        f2.close()

        search_result.insert(1, "ID:" + b_id)
        search_result.insert(2, "Name:" + clothes)
        search_result.insert(3, "Model:" + Model)
        search_result.insert(4, "Availability:" + availability)

        search_result.pack()
        search_menu2.mainloop()


def feedback_in():
    global feedback_bar
    global feedback_menu
    global feedback_input

    feedback_menu = Tk()
    feedback_menu.wm_title("Feedback")
    feedback_menu.maxsize(800, 200)
    feedback_menu.resizable(0, 0)

    feedback_bar = Entry(feedback_menu, width=100)
    feedback_label = Label(feedback_menu, text="We improve from your valuable feedback.Thank you!", font=(
        "Monotype corsiva", "15", "italic"), bg="red")
    button1 = Button(feedback_menu, text="Submit feedback", command=feedback_check, font=(
        "Times new roman", "10", "bold"), bg="RosyBrown2")

    feedback_bar.pack(side=TOP)
    feedback_label.pack(side=TOP)
    button1.pack(side=TOP)
    feedback_menu.mainloop()


def feedback_check():
    user_feedback = feedback_bar.get()
    if len(feedback_bar.get()) == 0:
        tkinter.messagebox.showinfo(
            "Feedback", "You did not type anything")
        feedback_menu.lift()
        return(feedback_in)
    else:
        tkinter.messagebox.showinfo(
            "Feedback", "Thank you for your valuable feedback!")
        file = open('Feedback.txt', 'a')
        file.write(user_feedback + "\n")
        file.close()
        feedback_menu.destroy()


def feedback_read():
    login_menu.destroy()
    read_feedback_menu = Tk()
    read_feedback_menu.minsize = (1000, 1000)
    read_feedback_menu.minsize = (1000, 1000)
    read_feedback_menu.wm_title("Users' feedback")

    list = Listbox(read_feedback_menu)
    file = open('Feedback.txt', 'r')
    num_feedback = len(file.readlines())
    file.close()
    file = open('Feedback.txt', 'r')
    count = 1
    feedback = file.readlines()
    for i in range(0, num_feedback):
        list_feedback = str(count) + ('.') + (feedback[count - 1])
        list.insert(count, list_feedback)
        count += 1
    file.close()

    list.pack(side=LEFT, fill=BOTH, expand=YES)
    read_feedback_menu.mainloop()


login_in()
