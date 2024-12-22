from tkinter import *
import tkinter as tk
from PIL import Image,ImageTk
import sqlite3
import tkinter.messagebox
import datetime
import time
import math
import os
import tempfile
import random
from employee import employeeclass # Link to the employee management page
from category import categoryClass # Link to the category management page
from supplier import supplierClass # Link to the supplier management page

# Get the current date and format it for display
date = datetime.datetime.now().date()
formatted_date = date.strftime("%d/%m/%Y")

class homepage:
    def __init__(self,root):
        self.root=root
        # Heading for the main application window
        self.heading = Label(text="RUBY FASHION", font=("Comic Sans MS", 40, "bold"),anchor="w",fg="#FFFFFF", bg="#000000")
        self.heading.place(x=0, y=0, relwidth=1,height=70)

        image_path = r"D:\Rexine Store Management\Icons\logout4.png"
        logout_symbol = Image.open(image_path)
        logout_symbol = logout_symbol.resize((35,35), Image.Resampling.LANCZOS)
        self.logout_symbol_tk = ImageTk.PhotoImage(logout_symbol)

        # Logout button to exit the application
        self.log_out = Button(text='Logout', image=self.logout_symbol_tk, compound=tk.LEFT,width=30, height=2, bg='#f70717',fg="#FFFFFF",bd=5,font=("arial 18 bold"),command=self.logout,cursor="hand2")
        self.log_out.place(x=1180, y=10,width=150,height=50) #Button size and position
        
        # Displaying the clock and welcome message
        self.lbl_clock = Label(text="Welcome to RUBY FASHION\t\t\t\t\t\t\t\t\t\t\t Date: "+str(formatted_date) +"", font=("times new roman",15),fg="#000000", bg="#FFFFFF")
        self.lbl_clock.place(x=0, y=70, relwidth=1,height=30)

        # Left menu for navigation to different sections
        self.menulogo = Image.open("Photos/OIG3.jpg")
        self.menulogo = self.menulogo.resize((220,130),Image.LANCZOS)
        self.menulogo=ImageTk.PhotoImage(self.menulogo)

        leftmenu=Frame(self.root,bd=2,relief=RIDGE,bg="dodgerblue3")
        leftmenu.place(x=1138,y=100,width=220,height=595)

        lbl_menulogo=Label(leftmenu,bg="dodgerblue3",image=self.menulogo)
        lbl_menulogo.pack(side=TOP,fill=BOTH)

        # Menu buttons to access various functionalities
        self.lbl_menu = Label(leftmenu,text='Menu',width=30, height=2,fg="#FFFFFF",font=("times new roman",20),bg="#052df7",bd=5)
        self.lbl_menu.pack(side=TOP,fill=BOTH)
        btn_employee = Button(leftmenu,text='Employee',width=30,command=self.employee,height=1,fg="#FFFFFF",font=("times new roman",20,"bold"),bg="#000000",bd=3,cursor="hand2")
        btn_employee.pack(side=TOP,fill=BOTH)
        btn_supplier = Button(leftmenu,text='Supplier',width=30,command=self.supplier, height=1,fg="#000000",font=("times new roman",20,"bold"),bg="#FFFFFF",bd=3,cursor="hand2")
        btn_supplier.pack(side=TOP,fill=BOTH)
        btn_category = Button(leftmenu,text='Category',width=30,command=self.category, height=1,fg="#FFFFFF",font=("times new roman",20,"bold"),bg="#000000",bd=3,cursor="hand2")
        btn_category.pack(side=TOP,fill=BOTH)
        btn_ad_products = Button(leftmenu,text='Add Products',width=30,command=self.adding, height=1,fg="#000000",font=("times new roman",20,"bold"),bg="#FFFFFF",bd=3,cursor="hand2")
        btn_ad_products.pack(side=TOP,fill=BOTH)
        btn_up_products = Button(leftmenu,text='Update Product',width=30,command=self.updating, height=1,fg="#FFFFFF",font=("times new roman",20,"bold"),bg="#000000",bd=3,cursor="hand2")
        btn_up_products.pack(side=TOP,fill=BOTH)
        btn_sales = Button(leftmenu,text='Sales',width=30,command=self.open_bill_page, height=1,fg="#000000",font=("times new roman",20,"bold"),bg="#FFFFFF",bd=3,cursor="hand2")
        btn_sales.pack(side=TOP,fill=BOTH)
        btn_exit = Button(leftmenu,text='Exit',width=30,command=self.exit, height=1,fg="#FFFFFF",font=("times new roman",20,"bold"),bg="#000000",bd=3,cursor="hand2")
        btn_exit.pack(side=TOP,fill=BOTH)

        # Content display for different statistics
        self.lbl_employee = Label(root,text="Total Employee \n[ 0 ]",bg="#000000",fg="#FFFFFF", bd=5, relief=RIDGE,font=("arial",20,"bold"))
        self.lbl_employee.place(x=80,y=150,width=300,height=150)
        self.lbl_supplier = Label(root,text="Total Supplier\n [ 0 ]",bg="#FFFFFF",fg="#000000", bd=5, relief=RIDGE,font=("arial",20,"bold"))
        self.lbl_supplier.place(x=430,y=150,width=300,height=150)
        self.lbl_add_pd = Label(root,text="Total Products\n [ 0 ]",bg="#000000",fg="#FFFFFF", bd=5, relief=RIDGE,font=("arial",20,"bold"))
        self.lbl_add_pd.place(x=780,y=150,width=300,height=150)
        self.lbl_category = Label(root,text="Total Employee \n[ 0 ]",bg="#FFFFFF",fg="#000000", bd=5, relief=RIDGE,font=("arial",20,"bold"))
        self.lbl_category.place(x=80,y=340,width=300,height=150)
       
        # Method to update the content for statistics
        self.update_content() 
        
    
    def update_content(self):
        # Connect to the database to fetch data for employee, supplier, category, and product statistics
        conn = sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            # Fetch and update the employee coun
            cur.execute("Select * from employee")
            employee=cur.fetchall()
            # Show total employee
            self.lbl_employee.config(text=f"Total Employee \n[{str(len(employee))}]")
           
            # Fetch and update the supplier count
            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f"Total Supplier \n[{str(len(supplier))}]")
            
            # Fetch and update the category count
            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_category.config(text=f"Total Category \n[{str(len(category))}]")
            
            # Fetch and update the product count
            cur.execute("select * from inventory")
            inventory=cur.fetchall()
            self.lbl_add_pd.config(text=f"Total Products \n[{str(len(inventory))}]")
        except Exception as ex:
            tkinter.messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    # Methods to navigate to different pages within the application #Click btn and open it's page
    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeclass(self.new_win)

    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)

    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)

    def adding(self):
        os.system("python add_to_db.py")
        
    def updating(self):
        os.system("python update.py")

    def open_bill_page(self):
        os.system("python main.py")

    def exit(self):
        self.root.destroy()
        
    def logout(self):
        root.destroy()
        os.system("python login.py")

if __name__ == "__main__":

    root = tk.Tk()
    b = homepage(root)
    root.geometry("1366x700+50+40")
    root.title("Home Page")
    root.config(bg="#87CEEB")
    root.mainloop()