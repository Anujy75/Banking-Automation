from tkinter import Tk, Label, Frame, Entry, Button, messagebox, filedialog
from tkinter.ttk import Combobox
import time, random
import project_tables
import sqlite3, gmail
from tkintertable import TableCanvas, TableModel
from PIL import Image, ImageTk
import os
import shutil

file =open("gmail_login.txt")
email,apppass = file.read().split(',')
file.close()

win = Tk()
win.state("zoomed")
win.resizable(width = False, height = False)
win.configure(bg = 'lime')
title = Label(win, text = "Banking Automation", font = ('arial', 50, 'bold', 'underline'), bg = 'lime', fg = 'blue')
title.pack()

date = time.strftime("%d-%B-%Y")
currdate = Label(win, text = date, font = ('arial', 20, 'bold',), bg = 'lime', fg = 'brown')
currdate.pack(pady = 10)

img = Image.open("logo1.JPG").resize((350, 135))
bitmap_img = ImageTk.PhotoImage(img, master = win)

lbl_img = Label(win, image = bitmap_img)
lbl_img.place(relx = 0, rely = 0)

img2 = Image.open("logo2.JPG").resize((350, 135))
bitmap_img2 = ImageTk.PhotoImage(img2, master = win)

lbl_img2 = Label(win, image = bitmap_img2)
lbl_img2.place(relx = .82, rely = 0)

footer = Label(win, text = "Created by Anuj @956XXXXX32\nLucknow U.P.", font = ('arial', 20, 'bold','underline'), bg = 'lime', fg = 'blue')
footer.pack(side = 'bottom')

def main_screen():
    frm = Frame(win, highlightbackground= 'black', highlightthickness=3)
    frm.configure(bg = 'pink')
    frm.place(relx = 0, rely = .13, relwidth= 1, relheight=.8)

    code_cap = ''
    for i in range(3):
       i = random.randint(65, 90)  # Generate a random uppercase letter
       c = chr(i)
       j = random.randint(0, 9)    # Generate a random digit
       code_cap = code_cap+str(j) + c   


    def forgot_pass():
        frm.destroy()
        forgotpass_screen()
    
    def login():
        acn_type = cb_type.get()
        acn = e_acn.get()
        pwd = e_pass.get()
        user_cap = e_captcha.get()
        if acn_type == "admin" and acn =="0" and pwd == "0":
            if user_cap == code_cap:
                frm.destroy()
                welcome_admin_screen()
            else:
                messagebox.showerror("login", "invalid Captcha")

        elif acn_type=="user":
            if user_cap==code_cap:
                conobj=sqlite3.connect('bank.sqlite')
                curobj=conobj.cursor()
                curobj.execute('select * from users where users_acno=? and users_pass=?',(acn,pwd))
                tup=curobj.fetchone()
                if tup==None:
                    messagebox.showerror("Login","Invalid ACN/Pass")
                    return
                else:
                    global welcome_user, users_acno
                    welcome_user=tup[1]
                    users_acno = tup[0]
                    frm.destroy()
                    welcome_user_screen()
            else:
                messagebox.showerror("login","invalid captcha")
        else:
            messagebox.showerror("login","invalid acn or password")

    lbl_type = Label(frm, text = "Account Type:",font = ('arial', 20, 'bold',), bg = 'pink' )
    lbl_type.place(relx = .3, rely = .15)

    cb_type = Combobox(frm, values = ['---select account type---','admin', 'user' ], font = ('arial', 20, 'bold',))
    cb_type.current(0)
    cb_type.place(relx = .425, rely = .15)

    lbl_acn = Label(frm, text = "Account Number:",font = ('arial', 20, 'bold',), bg = 'pink' )
    lbl_acn.place(relx = .3, rely = .25)

    e_acn = Entry(frm, font = ('arial', 20, ), bd = 5)
    e_acn.place(relx = .425, rely = .25)
    e_acn.focus()

    lbl_pass = Label(frm, text = "Password:",font = ('arial', 20, 'bold',), bg = 'pink' )
    lbl_pass.place(relx = .3, rely = .35)

    e_pass = Entry(frm, font = ('arial', 20, ), bd = 5, show = '*')
    e_pass.place(relx = .425, rely = .35)

    

    lbl_Captcha = Label(frm, text = f"Captcha:\t{code_cap}",font = ('arial', 20, 'bold',), bg = 'pink' , fg = "green")
    lbl_Captcha.place(relx = .35, rely = .47)

    def refresh():
        frm.destroy()
        main_screen()
 

    btn_refresh = Button(frm, text = 'refresh  captcha', font = ('arial', 14, 'bold' ), bd = 5, fg = "blue", command = refresh)
    btn_refresh.place(relx = .5, rely = .47, relheight=.04)

    Captcha = Label(frm, text = "Enter Captcha:",font = ('arial', 20, 'bold',), bg = 'pink' )
    Captcha.place(relx = .3, rely = .55)

    e_captcha = Entry(frm, font = ('arial', 20, ), bd = 5)
    e_captcha.place(relx = .43, rely = .55)

    btn_login = Button(frm, text = 'login', font = ('arial', 20, 'bold' ), bd = 5, command = login)
    btn_login.place(relx = .43, rely = .65)

    btn_reset = Button(frm, text = 'reset', font = ('arial', 20, 'bold' ), bd = 5, command= refresh)
    btn_reset.place(relx = .53, rely = .65)

    btn_forgetpass = Button(frm, text = 'Forgot password', font = ('arial', 20, 'bold' ), bd = 5, command = forgot_pass)
    btn_forgetpass.place(relx = .43, rely = .75)

def forgotpass_screen():
        frm = Frame(win, highlightbackground= 'black', highlightthickness=3)
        frm.configure(bg = 'grey')
        frm.place(relx = 0, rely = .13, relwidth= 1, relheight=.8)

        title_frame = Label(win, text = "Reset your password here by using Authentic Credentials", font = ('arial', 20, 'bold'), bg = 'slate grey', fg = 'red')
        title_frame.pack()
        title_frame.pack(pady = 20)

        def back():
            frm.destroy()
            main_screen()
        
        def reset():
            e_acn.delete(0, "end")
            e_mail.delete(0, "end")
            e_mob.delete(0, "end")
            e_acn.focus()
        
        def forgotpass_db():
            uacno = e_acn.get()
            umob = e_mob.get()
            uemail = e_mail.get()

            conobj=sqlite3.connect('bank.sqlite')
            curobj=conobj.cursor()
            curobj.execute('select users_name, users_pass from users where users_acno=? and users_email=? and users_mob = ?',(uacno,uemail, umob))
            tup=curobj.fetchone()
            if tup==None:
                messagebox.showerror("Forgot pasword","details")
                return
            else:
                global upass, uname
                uname = tup[0]
                upass=tup[1]
            
            otp = random.randint(1000, 9999)

            try:
                con=gmail.GMail(email, apppass)
                utext=f'''Hello, {uname},
                Your OTP to recover password is : {otp}
                For verification kindely use this OTP 

                Thanks
                ABC Bank Corp
                '''
                msg=gmail.Message(to=uemail,subject='OTP for password recovery',text=utext)
                con.send(msg)

                messagebox.showinfo('New User','Mail sent successfully')

                def otp_verify():
                    if otp == int(e_otp.get()):
                        messagebox.showinfo("Forgot pass", f"OTP verified, Your password is: {upass}")
                    else:
                        messagebox.showerror("Forgot password", "Invalid OTP")

                lbl_otp = Label(frm, text = "Enter OTP:",font = ('arial', 20, 'bold',), bg = 'grey' )
                lbl_otp.place(relx = .3, rely = .6)

                e_otp = Entry(frm, font = ('arial', 20, ), bd = 5)
                e_otp.place(relx = .428, rely = .6)

                btn_otp = Button(frm, text = 'Verify OTP', font = ('arial', 20, 'bold' ), bd = 5, fg = 'green', command = otp_verify ) 
                btn_otp.place(relx = .452, rely = .68, relheight= .05)

               
            except:
                messagebox.showerror('Network Problem','Something went wrong with network')
            


        btn_back = Button(frm, text = 'Back', font = ('arial', 20, 'bold' ), bd = 5, command = back)
        btn_back.place(relx = 0, rely = 0)

        lbl_acn = Label(frm, text = "Account Number:",font = ('arial', 20, 'bold',), bg = 'grey' )
        lbl_acn.place(relx = .3, rely = .2)

        e_acn = Entry(frm, font = ('arial', 20, ), bd = 5)
        e_acn.place(relx = .428, rely = .2)
        e_acn.focus()

        lbl_Mob = Label(frm, text = "Mobile Number:",font = ('arial', 20, 'bold',), bg = 'grey' )
        lbl_Mob.place(relx = .3, rely = .3)

        e_mob = Entry(frm, font = ('arial', 20, ), bd = 5)
        e_mob.place(relx = .428, rely = .3)

        lbl_Mail = Label(frm, text = "Mail ID:",font = ('arial', 20, 'bold',), bg = 'grey' )
        lbl_Mail.place(relx = .3, rely = .4)

        e_mail = Entry(frm, font = ('arial', 20, ), bd = 5)
        e_mail.place(relx = .428, rely = .4)

        btn_submit = Button(frm, text = 'submit', font = ('arial', 20, 'bold' ), bd = 5, fg = 'green', command = forgotpass_db) 
        btn_submit.place(relx = .428, rely = .5, relheight= .05)

        btn_reset = Button(frm, text = 'reset', font = ('arial', 20, 'bold' ), bd = 5, fg = 'blue', command = reset)
        btn_reset.place(relx = .52, rely = .5, relheight= .05)

def welcome_admin_screen():
    frm = Frame(win, highlightbackground= 'black', highlightthickness=3)
    frm.configure(bg = 'pink')
    frm.place(relx = 0, rely = .13, relwidth= 1, relheight=.8)

    title_frame = Label(frm, text = "Admin Home Screen", font = ('arial', 20, 'bold', "underline"), bg = 'pink', fg = 'black')
    title_frame.pack()
    

    def logout():
        frm.destroy()
        main_screen()
        
    def newuser():
        frm.destroy()
        newuser_screen()
    
    def deleteuser():
        frm.destroy()
        deleteuser_screen()
    
    def viewuser():
        frm.destroy()
        viewuser_screen()
    
    def back():
        frm.destroy()
        main_screen()
      
    btn_back = Button(frm, text = 'back', font = ('arial', 20, 'bold'), bd = 5, command = back)
    btn_back.place(relx = 0, rely = 0)

    btn_logout = Button(frm, text = 'logout', font = ('arial', 20, 'bold'), bd = 5, command = logout)
    btn_logout.place(relx = .94, rely = 0)

    btn_newuser = Button(frm, text = 'open user acn', font = ('arial', 20, 'bold'), bd = 5, bg = 'green' , fg = 'white', command = newuser)
    btn_newuser.place(relx = 0, rely = .2, relwidth  = .2)

    btn_viewuser = Button(frm, text = 'view user acn', font = ('arial', 20, 'bold'), bd = 5, command = viewuser, fg="blue")
    btn_viewuser.place(relx = 0, rely = .35, relwidth = .2)

    btn_deleteuser = Button(frm, text = 'delete user acn', command = deleteuser, font = ('arial', 20, 'bold'), bd = 5, bg = 'red', fg = 'white')
    btn_deleteuser.place(relx = 0, rely = .5, relwidth = .2)

def newuser_screen():
    frm = Frame(win, highlightbackground= 'black', highlightthickness=3)
    frm.configure(bg = 'pink')
    frm.place(relx = 0, rely = .13, relwidth= 1, relheight=.8)

    title_frame = Label(frm, text = "Open New Acccont", font = ('arial', 20, 'bold', "underline"), bg = 'pink', fg = 'green')
    title_frame.pack()

    def logout():
        frm.destroy()
        main_screen()
        
    def back():
        frm.destroy()
        welcome_admin_screen()
    
    def newuser_db():
        uname = e_name.get()
        umob = e_mob.get()
        umail = e_mail.get()
        uadhar = e_adhar.get()
        ubal = 0
        upass = ''
        for i in range(3):
            i = random.randint(65, 90)  # Generate a random uppercase letter
            c = chr(i)
            j = random.randint(0, 9)    # Generate a random digit
            upass = upass+str(j) + c 
    
        conobj = sqlite3.connect("bank.sqlite")
        curobj = conobj.cursor()
        curobj.execute("insert into users(users_name,users_pass,users_mob,users_email,users_bal,users_adhar,users_opendate) values(?, ?, ?, ?, ?, ?, ?)", (uname, upass, umob, umail, ubal, uadhar, date))
        conobj.commit()
        conobj.close() 

        conobj = sqlite3.connect("bank.sqlite")
        curobj = conobj.cursor()
        curobj.execute('select max(users_acno) from users')
        uacn = curobj.fetchone()[0]
        conobj.close()

        messagebox.showinfo("New User", f"ACN Created with ACN:{uacn} & PASS: {upass}")
        try:
            con=gmail.GMail(email, apppass)
            utext=f'''Hello, {uname},
            Your acount has been opened succesfully with ABC Bank
            Your Account No is {uacn}
            Your Password is {upass}

            Kindly change your password when you login to app

            Thanks
            ABC Bank Corp
            '''
            msg=gmail.Message(to=umail,subject='Account opened successfully',text=utext)
            con.send(msg)
            messagebox.showinfo('New User','Mail sent successfully')
        except:
            messagebox.showerror('Network Problem','Something went wrong with network')

    def reset():
         e_name.delete(0, "end")
         e_mail.delete(0, "end")
         e_mob.delete(0, "end")
         e_adhar.delete(0, "end")
         e_name.focus()
    
    btn_logout = Button(frm, text = 'logout', font = ('arial', 20, 'bold'), bd = 5, command = logout)
    btn_logout.place(relx = .94, rely = 0)

    btn_back = Button(frm, text = 'back', font = ('arial', 20, 'bold'), bd = 5, command = back)
    btn_back.place(relx = 0, rely = 0)

    lbl_name = Label(frm, text = "Name: ",font = ('arial', 20, 'bold',), bg = 'pink' )
    lbl_name.place(relx = .3, rely = .2)

    e_name = Entry(frm, font = ('arial', 20, ), bd = 5)
    e_name.place(relx = .428, rely = .2)
    e_name.focus()

    lbl_Mob = Label(frm, text = "Mobile Number:",font = ('arial', 20, 'bold',), bg = 'pink' )
    lbl_Mob.place(relx = .3, rely = .3)

    e_mob = Entry(frm, font = ('arial', 20, ), bd = 5)
    e_mob.place(relx = .428, rely = .3)

    lbl_Mail = Label(frm, text = "Mail ID:",font = ('arial', 20, 'bold',), bg = 'pink' )
    lbl_Mail.place(relx = .3, rely = .4)

    e_mail = Entry(frm, font = ('arial', 20, ), bd = 5)
    e_mail.place(relx = .428, rely = .4)

    lbl_adhar = Label(frm, text = "Adhar Number:",font = ('arial', 20, 'bold',), bg = 'pink' )
    lbl_adhar.place(relx = .3, rely = .5)

    e_adhar = Entry(frm, font = ('arial', 20, ), bd = 5)
    e_adhar.place(relx = .428, rely = .5)

    btn_submit = Button(frm, text = 'submit', font = ('arial', 20, 'bold' ), bd = 5, command = newuser_db)
    btn_submit.place(relx = .428, rely = .7, relwidth = .07)

    btn_reset = Button(frm, text = 'reset', font = ('arial', 20, 'bold' ), bd = 5, command =  reset)
    btn_reset.place(relx = .52, rely = .7, relwidth = .07)

    

def deleteuser_screen():
    frm = Frame(win, highlightbackground= 'black', highlightthickness=3)
    frm.configure(bg = 'pink')
    frm.place(relx = 0, rely = .13, relwidth= 1, relheight=.8)

    title_frame = Label(frm, text = "Delete user Acccont", font = ('arial', 20, 'bold', "underline"), bg = 'pink', fg = 'red')
    title_frame.pack()
    
    def logout():
        frm.destroy()
        main_screen()
        
    def back():
        frm.destroy()
        welcome_admin_screen()
    
    def reset():
        e_acn.delete(0, "end")
        e_adhar.delete(0, "end")
    
    def delete():
        uacn = e_acn.get()
        uadhar = e_adhar.get()
        conobj = sqlite3.connect("bank.sqlite")
        curobj = conobj.cursor()
        curobj.execute("delete from users where users_acno =? and users_adhar=?", (uacn, uadhar,))
        curobj.execute("delete from txn where txn_acno =?", (uacn,))
        conobj.commit()
        conobj.close()
        messagebox.showinfo("Delete User", f"Account number: {uacn} deleted")
    
    btn_logout = Button(frm, text = 'logout', font = ('arial', 20, 'bold'), bd = 5, command = logout, fg = 'blue')
    btn_logout.place(relx = .94, rely = 0)

    btn_back = Button(frm, text = 'back', font = ('arial', 20, 'bold'), bd = 5, command = back)
    btn_back.place(relx = 0, rely = 0)

    lbl_acn = Label(frm, text = "Account Number:",font = ('arial', 20, 'bold',), bg = 'pink' )
    lbl_acn.place(relx = .3, rely = .25)

    e_acn = Entry(frm, font = ('arial', 20, ), bd = 5)
    e_acn.place(relx = .428, rely = .25)
    e_acn.focus()

    lbl_adhar = Label(frm, text = "Adhar Number:",font = ('arial', 20, 'bold',), bg = 'pink' )
    lbl_adhar.place(relx = .3, rely = .35)

    e_adhar = Entry(frm, font = ('arial', 20, ), bd = 5)
    e_adhar.place(relx = .428, rely = .35)

    btn_delete = Button(frm, text = 'delete', font = ('arial', 20, 'bold' ), bd = 5, fg = 'red', command = delete)
    btn_delete.place(relx = .428, rely = .45, relwidth = .07)

    btn_reset = Button(frm, text = 'reset', font = ('arial', 20, 'bold' ), bd = 5, fg = 'blue', command = reset)
    btn_reset.place(relx = .52, rely = .45, relwidth = .07)

def viewuser_screen():
    frm = Frame(win, highlightbackground= 'black', highlightthickness=3)
    frm.configure(bg = 'pink')
    frm.place(relx = 0, rely = .13, relwidth= 1, relheight=.8)

    title_frame = Label(frm, text = "View Acccont", font = ('arial', 20, 'bold', "underline"), bg = 'pink', fg = 'green')
    title_frame.pack()
    
    def logout():
        frm.destroy()
        main_screen()
        
    def back():
        frm.destroy()
        welcome_admin_screen()
    
    def view():
        uacn = e_acn.get()
        conobj = sqlite3.connect("bank.sqlite")
        curobj = conobj.cursor()
        curobj.execute("select * from users where users_acno = ?", (uacn,))
        tup = curobj.fetchone()
        conobj.close()
        if tup == None:
            messagebox.showerror("View", "Account doesn't exist")
            return

        lbl_name = Label(frm, text = "User Name: ", font = ('arial', 15, 'bold'), bg = "pink",  fg = 'black')
        lbl_name.place(relx = .4, rely = 0.22)

        lbl_name_value= Label(frm, text = tup[1], font = ('arial', 14, 'bold'),bg = "pink",fg = 'blue')
        lbl_name_value.place(relx = .52, rely = 0.22)

        lbl_acn = Label(frm, text = "Account Number: ", font = ('arial', 15, 'bold'), bg = "pink", fg = 'black')
        lbl_acn.place(relx = .4, rely = 0.32)

        lbl_acn_value= Label(frm, text = tup[0], font = ('arial', 14, 'bold'),bg = "pink",fg = 'blue')
        lbl_acn_value.place(relx = .52, rely = 0.32)

        lbl_adhar = Label(frm, text = "Adhar Number: ", font = ('arial', 15, 'bold'), bg = "pink", fg = 'black')
        lbl_adhar.place(relx = .4, rely = 0.42)

        lbl_adhar_value= Label(frm, text = tup[6], font = ('arial', 14, 'bold'),bg = "pink",fg = 'blue')
        lbl_adhar_value.place(relx = .52, rely = 0.42)

        lbl_mob = Label(frm, text = "Mobile Number: ", font = ('arial', 15, 'bold'), bg = "pink", fg = 'black')
        lbl_mob.place(relx = .4, rely = 0.52)

        lbl_mob_value= Label(frm, text = tup[3], font = ('arial', 14, 'bold'),bg = "pink",fg = 'blue')
        lbl_mob_value.place(relx = .52, rely = 0.52)

        lbl_opendate = Label(frm, text = "Acn Opne Date: ", font = ('arial', 15, 'bold'),bg = "pink",  fg = 'black')
        lbl_opendate.place(relx = .4, rely = 0.62)

        lbl_opendate_value= Label(frm, text = tup[7], font = ('arial', 14, 'bold'),bg = "pink",fg = 'blue')
        lbl_opendate_value.place(relx = .52, rely = 0.62)

        lbl_bal = Label(frm, text = "Available Balance: ", font = ('arial', 15, 'bold'), bg = "pink", fg = 'black')
        lbl_bal.place(relx = .4, rely = 0.72)

        lbl_bal_value= Label(frm, text = tup[5], font = ('arial', 14, 'bold'),bg="pink",fg = 'blue')
        lbl_bal_value.place(relx = .52, rely = 0.72)
    
    btn_logout = Button(frm, text = 'logout', font = ('arial', 20, 'bold'), bd = 5, command = logout)
    btn_logout.place(relx = .94, rely = 0, relheight= .07)

    btn_back = Button(frm, text = 'back', font = ('arial', 20, 'bold'), bd = 5, command = back)
    btn_back.place(relx = 0, rely = 0, relheight=.07)

    lbl_acn = Label(frm, text = "Account Number:",font = ('arial', 20, 'bold',), bg = 'pink' )
    lbl_acn.place(relx = .3, rely = .12)

    e_acn = Entry(frm, font = ('arial', 20, ), bd = 5)
    e_acn.place(relx = .428, rely = .12)
    e_acn.focus()

    btn_search = Button(frm, text = 'search', font = ('arial', 20, 'bold' ), bd = 5, command = view)
    btn_search.place(relx = .6, rely = .12, relwidth = .07, relheight= .05)

def welcome_user_screen():
    frm = Frame(win, highlightbackground= 'black', highlightthickness=3)
    frm.configure(bg = 'pink')
    frm.place(relx = 0, rely = .13, relwidth= 1, relheight=.8)
    
    screen_title = "User Home Screen"
    frm_title = Label(frm, text = "User Home Screen", font = ('arial', 20, 'bold', "underline"), bg = 'pink', fg = 'blue')
    frm_title.place(relx = .5, rely = .1)

    lbl_well = Label(frm, text = f"Welcome, {welcome_user}", font = ('arial', 15, 'bold'), bg = 'pink', fg = 'blue')
    lbl_well.place(relx = 0, rely = 0)

    def logout():
        frm.destroy()
        main_screen()
    
    def details_screen():
        screen_title = "User Details Screen"
        frm_title.configure(text = screen_title)

        i_frm = Frame(frm, highlightbackground= 'black', highlightthickness=3)
        i_frm.configure(bg = 'white')
        i_frm.place(relx = 0.25, rely = .15, relwidth= .7, relheight=.65)

        conobj = sqlite3.connect("bank.sqlite")
        curobj = conobj.cursor()
        curobj.execute("select * from users where users_acno = ?", (users_acno, ))
        tup = curobj.fetchone()
        conobj.close()

        lbl_name = Label(i_frm, text = "User Name: ", font = ('arial', 15, 'bold'), bg = "white",  fg = 'black')
        lbl_name.place(relx = .25, rely = 0.05)

        lbl_name_value= Label(i_frm, text = tup[1], font = ('arial', 14, 'bold'),bg = "white",fg = 'blue')
        lbl_name_value.place(relx = .42, rely = 0.05)

        lbl_acn = Label(i_frm, text = "Account Number: ", font = ('arial', 15, 'bold'), bg = "white", fg = 'black')
        lbl_acn.place(relx = .25, rely = 0.17)

        lbl_acn_value= Label(i_frm, text = tup[0], font = ('arial', 14, 'bold'),bg = "white",fg = 'blue')
        lbl_acn_value.place(relx = .42, rely = 0.17)

        lbl_adhar = Label(i_frm, text = "Adhar Number: ", font = ('arial', 15, 'bold'), bg = "white", fg = 'black')
        lbl_adhar.place(relx = .25, rely = 0.29)

        lbl_adhar_value= Label(i_frm, text = tup[6], font = ('arial', 14, 'bold'),bg = "white",fg = 'blue')
        lbl_adhar_value.place(relx = .42, rely = 0.29)

        lbl_mob = Label(i_frm, text = "Mobile Number: ", font = ('arial', 15, 'bold'), bg = "white", fg = 'black')
        lbl_mob.place(relx = .25, rely = 0.41)

        lbl_mob_value= Label(i_frm, text = tup[3], font = ('arial', 14, 'bold'),bg = "white",fg = 'blue')
        lbl_mob_value.place(relx = .42, rely = 0.41)

        lbl_opendate = Label(i_frm, text = "Acn Opne Date: ", font = ('arial', 15, 'bold'),bg = "white",  fg = 'black')
        lbl_opendate.place(relx = .25, rely = 0.53)

        lbl_opendate_value= Label(i_frm, text = tup[7], font = ('arial', 14, 'bold'),bg = "white",fg = 'blue')
        lbl_opendate_value.place(relx = .42, rely = 0.53)

        lbl_bal = Label(i_frm, text = "Available Balance: ", font = ('arial', 15, 'bold'), bg = "white", fg = 'black')
        lbl_bal.place(relx = .25, rely = 0.65)

        lbl_bal_value= Label(i_frm, text = tup[5], font = ('arial', 14, 'bold'),bg = "white",fg = 'blue')
        lbl_bal_value.place(relx = .42, rely = 0.65)
    
    def deposite_screen():
        screen_title = "User Deposite Screen"
        frm_title.configure(text = screen_title)

        i_frm = Frame(frm, highlightbackground= 'black', highlightthickness=3)
        i_frm.configure(bg = 'white')
        i_frm.place(relx = 0.25, rely = .15, relwidth= .7, relheight=.65)

        def deposit():
            uamt = int(e_amt.get())
            conobj = sqlite3.connect(database = "bank.sqlite")
            curobj = conobj.cursor()
            curobj.execute("update users set users_bal = users_bal+? where users_acno = ?", (uamt, users_acno))
            conobj.commit()
            conobj.close()

            conobj = sqlite3.connect(database = "bank.sqlite")
            curobj = conobj.cursor()
            #curobj.execute("select users_bal from users where users_acno = ?", (users_acno))
            curobj.execute('select users_bal from users where users_acno=?',(users_acno,))
            ubal = curobj.fetchone()[0]
            conobj.close()

            conobj = sqlite3.connect(database = "bank.sqlite")
            curobj = conobj.cursor()
            curobj.execute("insert into txn(txn_acno, txn_type, txn_amt, txn_bal, txn_date) values(?,?,?,?,?)", (users_acno, "Cr", uamt, ubal, date ))
            conobj.commit()
            conobj.close()

            messagebox.showinfo("Deposite", f"{uamt} Deposited, Your updated balance is: {ubal}")

        lbl_amt = Label(i_frm, text = "Enter Amount: ",font = ('arial', 20, 'bold',))
        lbl_amt.place(relx = .25, rely = .25)

        e_amt = Entry(i_frm, font = ('arial', 15 ), bd = 5, bg = "light grey")
        e_amt.place(relx = .45, rely = .25)
        e_amt.focus()

        btn_submit = Button(i_frm, text = 'submit', font = ('arial', 20, 'bold'), bd = 5, bg = "green", fg = "white", command = deposit)
        btn_submit.place(relx = 0.35, rely = 0.4, relheight=.08 )


    def withdraw_screen():
        screen_title = "User Withdraw Screen"
        frm_title.configure(text = screen_title)

        i_frm = Frame(frm, highlightbackground= 'black', highlightthickness=3)
        i_frm.configure(bg = 'white')
        i_frm.place(relx = 0.25, rely = .15, relwidth= .7, relheight=.65)

        def withdraw():
            uamt = int(e_amt.get())

            
            conobj = sqlite3.connect(database = "bank.sqlite")
            curobj = conobj.cursor()
            curobj.execute('select users_bal from users where users_acno=?',(users_acno,))
            ubal = curobj.fetchone()[0]
            conobj.commit()
            conobj.close()
            if ubal>uamt:
                conobj = sqlite3.connect(database = "bank.sqlite")
                curobj = conobj.cursor()
                curobj.execute("update users set users_bal = users_bal-? where users_acno = ?", (uamt, users_acno))
                conobj.commit()
                conobj.close()

                conobj = sqlite3.connect(database = "bank.sqlite")
                curobj = conobj.cursor()
                curobj.execute("insert into txn(txn_acno, txn_type, txn_amt, txn_bal, txn_date) values(?,?,?,?,?)", (users_acno, "Dr", uamt, ubal-uamt, date ))
                conobj.commit()
                conobj.close()

                messagebox.showinfo("Withdrwa", f"{uamt} Withdrawn, Your updated balance is: {ubal-uamt}")
            else:
                messagebox.showerror("withdraw", f"Insufficient balance, Your rest amount is: {ubal}")


        lbl_amt = Label(i_frm, text = "Enter Amount: ",font = ('arial', 20, 'bold',))
        lbl_amt.place(relx = .3, rely = .25)

        e_amt = Entry(i_frm, font = ('arial', 15 ), bd = 5, bg = "light grey")
        e_amt.place(relx = .48, rely = .25)
        e_amt.focus()

        btn_withdraw = Button(i_frm, text = 'withdraw', font = ('arial', 20, 'bold'), bd = 5, bg = "red", fg = "white", command = withdraw)
        btn_withdraw.place(relx = 0.4, rely = 0.43, relheight=.07)
    
    def update_screen():
        screen_title = "User Update Screen"
        frm_title.configure(text = screen_title)

        i_frm = Frame(frm, highlightbackground= 'black', highlightthickness=3)
        i_frm.configure(bg = 'white')
        i_frm.place(relx = 0.25, rely = .15, relwidth= .7, relheight=.65)

        def update_db():
            upass = e_pass.get()
            umob = e_mob.get()
            uemail = e_mail.get()
            uname = e_name.get()
            conobj = sqlite3.connect("bank.sqlite")
            curobj = conobj.cursor()
            curobj.execute("update users set users_pass = ?, users_mob = ?, users_email = ?, users_name = ? where users_acno=?", (upass, umob, uemail, uname, users_acno))
            conobj.commit()
            conobj.close()


            messagebox.showinfo("Update Details", "Updated")
        
        lbl_name = Label(i_frm, text = "Name: ",font = ('arial', 18, 'bold',))
        lbl_name.place(relx = .25, rely = .15)

        e_name = Entry(i_frm, font = ('arial', 15 ), bd = 5, bg = "light grey")
        e_name.place(relx = .45, rely = .15)
        e_name.focus()


        lbl_mob = Label(i_frm, text = "Mobile Number: ",font = ('arial', 18, 'bold',))
        lbl_mob.place(relx = .25, rely = .3)

        e_mob = Entry(i_frm, font = ('arial', 15 ), bd = 5, bg = "light grey")
        e_mob.place(relx = .45, rely = .3)
        

        lbl_pass = Label(i_frm, text = "Password : ",font = ('arial', 18, 'bold',))
        lbl_pass.place(relx = .25, rely = .45)

        e_pass = Entry(i_frm, font = ('arial', 15 ), bd = 5, bg = "light grey")
        e_pass.place(relx = .45, rely = .45)

        lbl_mail = Label(i_frm, text = "Mail : ",font = ('arial', 18, 'bold',))
        lbl_mail.place(relx = .25, rely = .6)

        e_mail = Entry(i_frm, font = ('arial', 15 ), bd = 5, bg = "light grey")
        e_mail.place(relx = .45, rely = .6)

        btn_update = Button(i_frm, text = 'update', font = ('arial', 20, 'bold'), bd = 5, bg = "green", fg = "white", command = update_db)
        btn_update.place(relx = 0.35, rely = 0.75, relheight=.08)

        conobj = sqlite3.connect("bank.sqlite")
        curobj = conobj.cursor()
        curobj.execute("select users_pass, users_mob, users_email, users_name from users where users_acno = ?", (users_acno, ))
        tup = curobj.fetchone()
        conobj.close()

        e_pass.insert(0, tup[0])
        e_mob.insert(0, tup[1])
        e_mail.insert(0, tup[2])
        e_name.insert(0, tup[3])

        
    def transfer_screen():
        screen_title = "User Transfer Screen"
        frm_title.configure(text = screen_title)

        i_frm = Frame(frm, highlightbackground= 'black', highlightthickness=3)
        i_frm.configure(bg = 'white')
        i_frm.place(relx = 0.25, rely = .15, relwidth= .7, relheight=.65)

        lbl_to = Label(i_frm, text = "To Acoount: ",font = ('arial', 20, 'bold',))
        lbl_to.place(relx = .25, rely = .15)

        e_to = Entry(i_frm, font = ('arial', 18 ), bd = 5, bg = "light grey")
        e_to.place(relx = .45, rely = .15)
        e_to.focus()

        def transfer():
            uamt = int(e_amt.get())
            utoacn = int(e_to.get())

            conobj = sqlite3.connect("bank.sqlite")
            curobj = conobj.cursor()
            curobj.execute("select * from users where users_acno = ?", (utoacn,))
            tup = curobj.fetchone()
            conobj.close()
            if tup ==None:
                messagebox.showinfo("Transfer", "Invalid To ACN")
            else:
                conobj = sqlite3.connect(database = "bank.sqlite")
            curobj = conobj.cursor()
            curobj.execute('select users_bal from users where users_acno=?',(users_acno,))
            ubal = curobj.fetchone()[0]
            conobj.commit()
            conobj.close()
            if ubal>uamt:
                conobj = sqlite3.connect(database = "bank.sqlite")
                curobj = conobj.cursor()
                curobj.execute("update users set users_bal = users_bal-? where users_acno = ?", (uamt, users_acno))
                curobj.execute("update users set users_bal = users_bal+? where users_acno = ?", (uamt, utoacn))
                conobj.commit()
                conobj.close()

                conobj = sqlite3.connect(database = "bank.sqlite")
                curobj = conobj.cursor()
                curobj.execute("insert into txn(txn_acno, txn_type, txn_amt, txn_bal, txn_date) values(?,?,?,?,?)", (users_acno, "Dr", uamt, ubal-uamt, date ))
                curobj.execute("insert into txn(txn_acno, txn_type, txn_amt, txn_bal, txn_date) values(?,?,?,?,?)", (utoacn, "Cr", uamt, ubal+uamt, date ))
                conobj.commit()
                conobj.close()

                messagebox.showinfo("Transaction Done", f"{uamt} Transfered, Your updated balance is: {ubal-uamt}")
            else:
                messagebox.showerror("Transfer", f"Insufficient balance, Your rest amount is: {ubal}")


        lbl_amt = Label(i_frm, text = "Transfer Amount: ",font = ('arial', 20, 'bold',))
        lbl_amt.place(relx = .25, rely = .3)

        e_amt = Entry(i_frm, font = ('arial', 18 ), bd = 5, bg = "light grey")
        e_amt.place(relx = .45, rely = .3)

        btn_submit = Button(i_frm, text = 'submit', font = ('arial', 20, 'bold'), bd = 5, bg = "green", fg = "white", command = transfer)
        btn_submit.place(relx = 0.4, rely = 0.45, relheight=.08)
        
    
    def history_screen():
        screen_title = "User Txn History Screen"
        frm_title.configure(text = screen_title)

        i_frm = Frame(frm, highlightbackground= 'black', highlightthickness=3)
        i_frm.configure(bg = 'white')
        i_frm.place(relx = 0.25, rely = .15, relwidth= .7, relheight=.65)

  
        data = {}
        conobj = sqlite3.connect("bank.sqlite")
        curobj = conobj.cursor()
        curobj.execute("select * from txn where txn_acno=?", (users_acno,))
        tups = curobj.fetchall()
        i = 1
        for tup in tups:
            data[str(i)] = {"Txn Amt":tup[3], "Txn Type":tup[2], "Updated Bal": tup[4], "Txn Date": tup[5], "Txn Id": tup[0] }
            i+=1

        model = TableModel()
        model.importDict(data)

        table_frm = Frame(i_frm)
        table_frm.place(relx = .2, rely = .2)
        table = TableCanvas(table_frm, model = model, editable = False)
        table.show()

    def update_picture():
        img_path = filedialog.askopenfilename()
        shutil.copy(img_path, f"{users_acno}.png")
        #print(img_path)
        #os.rename(img_path, f"{users_acno}.png")

        pro_img = Image.open(f"{users_acno}.png").resize((230, 180))
        pro_bitmap_img = ImageTk.PhotoImage(pro_img, master = frm)

        prolbl_img = Label(frm, image = pro_bitmap_img)
        prolbl_img.image = pro_bitmap_img
        prolbl_img.place(relx=0, rely=0.04)



    btn_logout = Button(frm, text = 'logout', font = ('arial', 20, 'bold'), bd = 5, command = logout)
    btn_logout.place(relx = .94, rely = 0, relheight= .05)
    
    if os.path.exists(f"{users_acno}.png"):
        pro_img = Image.open(f"{users_acno}.png").resize((230, 180))
    else:
        pro_img = Image.open("profile.JPG").resize((230, 180))

    pro_bitmap_img = ImageTk.PhotoImage(pro_img, master = frm)

    prolbl_img = Label(frm, image = pro_bitmap_img)
    prolbl_img.image = pro_bitmap_img
    prolbl_img.place(relx=0, rely=0.04)

    btn_update_pic = Button(frm, text = 'update profile', font = ('arial', 15,), bd = 5, fg = 'blue', command= update_picture)
    btn_update_pic.place(relx = .0, rely = .262, relheight= .05, relwidth=.13)


    btn_details = Button(frm, text = 'check details', font = ('arial', 20, 'bold'), command = details_screen, bd = 5, bg = 'yellow' , fg = 'green')
    btn_details.place(relx = 0, rely = .33, relwidth  = .14)

    btn_deposit = Button(frm, text = 'deposit',  font = ('arial', 20, 'bold'), command = deposite_screen, bd = 5, bg = 'green', fg = 'white')
    btn_deposit.place(relx = 0, rely = .43, relwidth = .14)

    btn_withdraw = Button(frm, text = 'withdraw', font = ('arial', 20, 'bold'), command = withdraw_screen, bd = 5, bg = 'crimson', fg="white")
    btn_withdraw.place(relx = 0, rely = .53, relwidth = .14)

    btn_update = Button(frm, text = 'update',  font = ('arial', 20, 'bold'), bd = 5, fg = 'blue', command = update_screen)
    btn_update.place(relx = 0, rely = .63, relwidth = .14)

    btn_transfer = Button(frm, text = 'transfer',  font = ('arial', 20, 'bold'), bd = 5, bg = 'grey', command = transfer_screen,fg = 'white')
    btn_transfer.place(relx = 0, rely = .73, relwidth = .14)

    btn_history = Button(frm, text = 'history',  font = ('arial', 20, 'bold'), bd = 5, bg = 'sky blue', command = history_screen,fg = 'white')
    btn_history.place(relx = 0, rely = .83, relwidth = .14)
    
main_screen()
win.mainloop() 