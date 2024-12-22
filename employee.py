from tkinter import *
import tkinter as tk
import sqlite3
import tkinter.messagebox
import datetime
import math
import os
from tkinter import *
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3

class employeeclass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Employee Management System")
        self.root.config(bg="#fafafa")
        self.root.focus_force()

        # Initialize all variables
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        
        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name=StringVar()
        self.var_dob=StringVar()
        self.var_doj=StringVar()
        self.var_pass=StringVar()
        self.var_utype=StringVar()

        # Title Label
        title=Label(self.root,text="Employee Details",font=("goudy old style",20,"bold"),bg="#2a2f4f",fg="white")
        title.place(x=0,y=0,width=1100,height=40)


        # Content Section
        # Row1
        lbl_empid=Label(self.root,text="Emp ID",font=("goudy old style",15),bg="#fafafa").place(x=50,y=50)
        lbl_gender=Label(self.root,text="Gender",font=("goudy old style",15),bg="#fafafa").place(x=350,y=50)
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style",15),bg="#fafafa").place(x=750,y=50)

        txt_empid=Entry(self.root,textvariable=self.var_emp_id,font=("goudy old style",15),bg="lightgrey").place(x=150,y=50,width=180)
        cmb_gender=ttk.Combobox(self.root,textvariable=self.var_gender,values=("Select","Male","Female","Other"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_gender.place(x=500,y=50,width=180)
        cmb_gender.current(0)
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightgrey").place(x=850,y=50,width=180)

        # Row2
        lbl_name=Label(self.root,text="Name",font=("goudy old style",15),bg="#fafafa").place(x=50,y=100)
        lbl_dob=Label(self.root,text="D.O.B",font=("goudy old style",15),bg="#fafafa").place(x=350,y=100)
        lbl_doj=Label(self.root,text="D.O.J",font=("goudy old style",15),bg="#fafafa").place(x=750,y=100)

        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightgrey").place(x=150,y=100,width=180)
        txt_dob=Entry(self.root,textvariable=self.var_dob,font=("goudy old style",15),bg="lightgrey").place(x=500,y=100,width=180)
        txt_doj=Entry(self.root,textvariable=self.var_doj,font=("goudy old style",15),bg="lightgrey").place(x=850,y=100,width=180)

        # Row3
        lbl_pass=Label(self.root,text="Password",font=("goudy old style",15),bg="#fafafa").place(x=50,y=150)
        lbl_utype=Label(self.root,text="User Type",font=("goudy old style",15),bg="#fafafa").place(x=350,y=150)

        
        txt_pass=Entry(self.root,textvariable=self.var_pass,font=("goudy old style",15),bg="lightgrey").place(x=150,y=150,width=180)
        cmb_utype=ttk.Combobox(self.root,textvariable=self.var_utype,values=("Select","Admin","Employee"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_utype.place(x=500,y=150,width=180)
        cmb_utype.current(0)


        # Button Section
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15,"bold"),bg="#008000",fg="#FFFFFF",cursor="hand2",relief=RIDGE)
        btn_add.place(x=300,y=250,width=110,height=40)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15,"bold"),bg="#800080",fg="#FFFFFF",cursor="hand2",relief=RIDGE)
        btn_update.place(x=420,y=250,width=110,height=40)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15,"bold"),bg="#FF0000",fg="#FFFFFF",cursor="hand2",relief=RIDGE)
        btn_delete.place(x=540,y=250,width=110,height=40)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15,"bold"),bg="#FFA500",fg="#FFFFFF",cursor="hand2",relief=RIDGE)
        btn_clear.place(x=660,y=250,width=110,height=40)

        # Employee Details Frame
        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=300,relwidth=1,height=200)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("eid","name","gender","contact","dob","doj","pass","u_type"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)
        self.EmployeeTable.heading("eid",text="Employee ID")
        self.EmployeeTable.heading("name",text="Name")
        self.EmployeeTable.heading("gender",text="Gender")
        self.EmployeeTable.heading("contact",text="Contact Number")
        self.EmployeeTable.heading("dob",text="D.O.B")
        self.EmployeeTable.heading("doj",text="D.O.J")
        self.EmployeeTable.heading("pass",text="Password")
        self.EmployeeTable.heading("u_type",text="User Type")
        self.EmployeeTable["show"]="headings"

        self.EmployeeTable.pack(fill=BOTH,expand=1)

        self.EmployeeTable.column("eid",width=90)
        self.EmployeeTable.column("name",width=200)
        self.EmployeeTable.column("gender",width=100)
        self.EmployeeTable.column("contact",width=100)
        self.EmployeeTable.column("dob",width=100)
        self.EmployeeTable.column("doj",width=100)
        self.EmployeeTable.column("pass",width=100)
        self.EmployeeTable.column("u_type",width=100)
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()

    # Method to add a new employee record    
    def add(self):
        conn=sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            if self.var_emp_id.get()=="": 
                messagebox.showerror("Error","All Fields must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID is Alreary Assigned, try different",parent=self.root)
                else:
                    cur.execute("Insert into employee (eid,name,gender,contact,dob,doj,pass,u_type) values(?,?,?,?,?,?,?,?)",(
                                        self.var_emp_id.get(),
                                        self.var_name.get(),
                                        self.var_gender.get(),
                                        self.var_contact.get(),                                       
                                        self.var_dob.get(),
                                        self.var_doj.get(),
                                        self.var_pass.get(),
                                        self.var_utype.get(),
                                    
                    ))
                    conn.commit()
                    messagebox.showinfo("Succes","Employee Added Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
    
    # Method to display employee data in the table
    def show(self):
        conn=sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            cur.execute("Select * from employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    # Method to retrieve employee data for update
    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        #print(row)
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_gender.set(row[2])
        self.var_contact.set(row[3])
                                        
        self.var_dob.set(row[4])
        self.var_doj.set(row[5])
                                        
        self.var_pass.set(row[6])
        self.var_utype.set(row[7])

    # Method to update employee data
    def update(self):
        conn=sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            if self.var_emp_id.get()=="": 
                messagebox.showerror("Error","All Fields must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    cur.execute("Update employee set name=?,gender=?,contact=?,dob=?,doj=?,pass=?,u_type=? where eid=?",(
                                        self.var_name.get(),
                                        self.var_gender.get(),
                                        self.var_contact.get(),
                                        self.var_dob.get(),
                                        self.var_doj.get(),
                                        self.var_pass.get(),
                                        self.var_utype.get(),
                                        self.var_emp_id.get()
                    ))
                    conn.commit()
                    messagebox.showinfo("Succes","Employee Updated Successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    # Method to delete employee data
    def delete(self):
        conn=sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            if self.var_emp_id.get()=="": 
                messagebox.showerror("Error","All Fields must be required",parent=self.root)
            else:
                cur.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from employee where eid=?",(self.var_emp_id.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete","Employee Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    # Method to clear the input fields
    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
                                        
        self.var_dob.set("")
        self.var_doj.set("")
                                        
        self.var_pass.set("")
        self.var_utype.set("Select")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        conn=sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By Option",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search Input is Required",parent=self.root)
            else:
                cur.execute("Select * from employee where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found!!!",parent=self.root)
        except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

# Running the application
if __name__=="__main__":
    root=Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.resizable(screen_width,screen_height)
    obj=employeeclass(root)
    root.mainloop()
    