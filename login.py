from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
import time

class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.title("Login System")
        self.root.geometry("450x600+500+70")
        self.root.config(bg="#192A51")
        self.otp=''
       
        # String variables to hold the employee ID and password
        self.var_emp_id=StringVar()
        self.var_password=StringVar()

        # Login Frame Design
        Login_Frame=Frame(self.root,bg="#192A51")
        Login_Frame.place(x=50,y=30,width=350,height=400)

        # Title Label for the Login Frame
        Frametitle=Label(Login_Frame,text="Login",width=10,font=("Times New Roman",30,"bold"),bg="#192A51",fg="#db0404").place(x=50,y=10)

        # Label and Entry Field
        lbl_emp_id=Label(Login_Frame,text="ID",font=("Arial",15,"bold"),fg="#db0404",bg="#192A51").place(x=50,y=100)
        txt_emp_id=Entry(Login_Frame,textvariable=self.var_emp_id,font=("times new roman",15),bg="#f29999",fg="black").place(x=50,y=140,width=250,height=30)

        lbl_password=Label(Login_Frame,text="Password",font=("Arial",15,"bold"),fg="#db0404",bg="#192A51").place(x=50,y=200)
        txt_password=Entry(Login_Frame,textvariable=self.var_password,show="*",font=("times new roman",15,"bold"),bg="#f29999",fg="black").place(x=50,y=240,width=250,height=30)


        # Login Button
        btn_login=Button(Login_Frame,text=" Log In ",font=("Arial",20,"bold"),bg="#db0404",activebackground="#07f50f",activeforeground="red",fg="white",cursor="hand2",command=self.login,relief=RIDGE)
        btn_login.place(x=50,y=300,width=250,height=40)

        # Register Frame Design
        Sign_Up_Frame=Frame(self.root,bg="#192A51")
        Sign_Up_Frame.place(x=50,y=500,width=350,height=70)

        # Label and Button for Registering a New User
        lbl_register_info=Label(Sign_Up_Frame,text=" ↓Don't have an Account??↓ ",font=("Candara",15,"bold"),bg="#192A51",fg="#FFFFFF").place(x=55,y=5)
        btn_sign_up=Button(Sign_Up_Frame,text=" ..Sign Up.. ",font=("",15,"bold"),bg="#192A51",fg="#03FC2C",cursor="hand2",bd=0,activebackground="white",activeforeground="#07f50f",command=self.sign_up)
        btn_sign_up.place(x=90,y=40,width=150,height=20)

    # Function to handle the login process
    def login(self):
        conn=sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            # Check if either the Employee ID or Password fields are empty
            if self.var_emp_id.get()=="" or self.var_password.get()=="":
                messagebox.showerror("Error","All Fields are Required",parent=self.root)
            else:
                # Query to check if the provided ID and Password match an employee in the database
                cur.execute("select u_type from employee where eid=? AND pass=?",(self.var_emp_id.get(),self.var_password.get()))
                employee=cur.fetchone()

                # If no matching employee is found, show a warning
                if employee==None:
                    messagebox.showwarning("Warning","Invalid Employee ID or Password",parent=self.root)
                else:
                    # If the user is an Admin, open the admin home page
                    if employee[0]=="Admin":
                        self.root.destroy()
                        os.system("python home.py") #link with home page
                    else:
                        # Otherwise, open the main page for regular employees
                        self.root.destroy()
                        os.system("python main.py") #link with main page
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    # Function to handle the sign-up process for new users
    def sign_up(self):
        conn=sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            # Create a new window for the Sign-Up form
            self.forget_password_window=Toplevel(self.root)
            self.forget_password_window.title("SIGN UP System")
            self.forget_password_window.geometry("900x500+200+40")
            self.forget_password_window.config(bg="#fafafa")
            self.forget_password_window.focus_force()

            #===Employee Entry=====
            self.var_new_emp_id=StringVar()
            self.var_new_gender=StringVar()
            self.var_new_contact=StringVar()
            self.var_new_name=StringVar()
            self.var_new_dob=StringVar()
            self.var_new_doj=StringVar()
            self.var_new_pass=StringVar()
            self.var_new_utype=StringVar()

            # Title Label for the Sign-Up Form
            title=Label(self.forget_password_window,text="Enter Details",font=("sanserif",18,"bold"),bg="Black",fg="white").place(x=10,y=15,width=878,height=40)

            # Sign-Uo Form Content

            # Row 1: Employee ID and Name
            lbl_new_empid=Label(self.forget_password_window,text="Emp ID",font=("goudy old style",15),bg="#fafafa").place(x=50,y=100)
            lbl_new_name=Label(self.forget_password_window,text="Name",font=("goudy old style",15),bg="#fafafa").place(x=500,y=100)

            txt_new_empid=Entry(self.forget_password_window,textvariable=self.var_new_emp_id,font=("goudy old style",15),bg="lightgrey").place(x=150,y=100,width=200)
            txt_new_name=Entry(self.forget_password_window,textvariable=self.var_new_name,font=("goudy old style",15),bg="lightgrey").place(x=600,y=100,width=200)
            
            # Row 2: Contact and Password
            lbl_new_contact=Label(self.forget_password_window,text="Contact",font=("goudy old style",15),bg="#fafafa").place(x=50,y=150)
            lbl_new_pass=Label(self.forget_password_window,text="Password",font=("goudy old style",15),bg="#fafafa").place(x=500,y=150)
            
            txt_new_contact=Entry(self.forget_password_window,textvariable=self.var_new_contact,font=("goudy old style",15),bg="lightgrey").place(x=150,y=150,width=200)            
            txt_new_pass=Entry(self.forget_password_window,textvariable=self.var_new_pass,font=("goudy old style",15),bg="lightgrey").place(x=600,y=150,width=200)
            
            # Row 3: Date of Birth (D.O.B) and Date of Joining (D.O.J)
            lbl_new_dob=Label(self.forget_password_window,text="D.O.B",font=("goudy old style",15),bg="#fafafa").place(x=50,y=200)
            lbl_new_doj=Label(self.forget_password_window,text="D.O.J",font=("goudy old style",15),bg="#fafafa").place(x=500,y=200)

            txt_new_dob=Entry(self.forget_password_window,textvariable=self.var_new_dob,font=("goudy old style",15),bg="lightgrey").place(x=150,y=200,width=200)
            txt_new_doj=Entry(self.forget_password_window,textvariable=self.var_new_doj,font=("goudy old style",15),bg="lightgrey").place(x=600,y=200,width=200)

            # Row 4: Gender and User Type
            lbl_new_gender=Label(self.forget_password_window,text="Gender",font=("goudy old style",15),bg="#fafafa").place(x=50,y=250)
            lbl_new_utype=Label(self.forget_password_window,text="User Type",font=("goudy old style",15),bg="#fafafa").place(x=500,y=250)

            cmb_new_gender=ttk.Combobox(self.forget_password_window,textvariable=self.var_new_gender,values=("Select","Male","Female","Other"),state='readonly',justify=CENTER,font=("sanserif",15))
            cmb_new_gender.place(x=150,y=250,width=200)
            cmb_new_gender.current(0)
            cmb_new_utype=ttk.Combobox(self.forget_password_window,textvariable=self.var_new_utype,values=("Select","Admin","Employee"),state='readonly',justify=CENTER,font=("sanserif",15))
            cmb_new_utype.place(x=600,y=250,width=200)
            cmb_new_utype.current(0)
            

            # Button to Add the New User
            btn_new_add=Button(self.forget_password_window,text="Add User",command=self.new_add,font=("sanserif",15,"bold"),bg="Green",fg="White",cursor="hand2",relief=RIDGE).place(x=350,y=320,width=200,height=38)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    # Function to handle adding the new user to the database
    def new_add(self):
                conn=sqlite3.connect("D:\Rexine Store Management\Database\store.db")
                cur=conn.cursor()
                try:
                    # Check if the Employee ID field is empty
                    if self.var_new_emp_id.get()=="": 
                        messagebox.showerror("Error","All Fields must be required",parent=self.forget_password_window)
                    else:
                        # Query the database to check if the Employee ID already exists
                        cur.execute("Select * from employee where eid=?",(self.var_new_emp_id.get(),))
                        row=cur.fetchone()

                        # If the Employee ID is already in use, display an error message
                        if row!=None:
                            messagebox.showerror("Error","This Employee ID is Alreary Assigned, try different",parent=self.root)
                        else:
                            # If the Employee ID is unique, insert the new user details into the database
                            cur.execute("Insert into employee (eid,name,gender,contact,dob,doj,u_type,pass) values(?,?,?,?,?,?,?,?)",(
                                                self.var_new_emp_id.get(),
                                                self.var_new_name.get(),
                                                self.var_new_gender.get(),
                                                self.var_new_contact.get(), 
                                                self.var_new_dob.get(),
                                                self.var_new_doj.get(),                          
                                                self.var_new_utype.get(),
                                                self.var_new_pass.get(),
                            ))
                            # Commit the changes to the database
                            conn.commit()
                            messagebox.showinfo("Succes","Employee Added Successfully",parent=self.forget_password_window)
                        messagebox.showinfo("Success","Sign Up Successful")

                        # Close the sign-up window after successful registration
                        self.forget_password_window.destroy()
                        
                except Exception as ex:
                    # If an error occurs, display the error message
                    messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.forget_password_window)


root=Tk()
obj=Login_System(root)
root.mainloop()