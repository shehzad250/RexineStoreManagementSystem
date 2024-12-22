from tkinter import *
import tkinter as tk
import sqlite3
import tkinter.messagebox
from tkinter import ttk,messagebox
from PIL import Image,ImageTk  # for image (Python Imaging Library)

# Establishing a connection to the SQLite database
conn = sqlite3.connect("D:\Rexine Store Management\Database\store.db")
c = conn.cursor()

# Executing an SQL query to fetch the maximum ID from the inventory table
result = c.execute("SELECT Max(id) from inventory")
for r in result:
    id = r[0]   # Retrieving the maximum ID

# Defining the Database class
class Database:
    def __init__(self,master,*args,**kwargs):
        # Setting the master frame and heading
        self.master = master
        self.heading = Label(master,text="Add Products", font=('goudy old style',20,"bold"),fg='#FFFFFF',bg="#2A2F4F")
        self.heading.place(width=1370,height=40,x=0,y=0)

        # Back Button to return to home page
        self.back_button = Button(master, text="← Back", font=("Arial", 10, "bold"), bg="white", fg="black",
                                  command=self.go_back)
        self.back_button.place(x=10, y=10)  # Position the back button


        # Labels for input fields
        self.id_l = Label(master, text="Enter ID", font=("Verdana 18 bold"))
        self.id_l.place(x=0, y=400)

        self.category_l=Label(master,text="Enter Category Name",font=("Verdana 18 bold"))
        self.category_l.place(x=0,y=50)

        self.product_name_l = Label(master, text="Enter The Product Name", font=("Verdana 18 bold"))
        self.product_name_l.place(x=0, y=100)

        self.stock_l = Label(master, text="Enter Availabe Stock", font=("Verdana",18,"bold"))
        self.stock_l.place(x=0, y=150)

        self.costPrize_l = Label(master, text="Enter Cost Prize", font=("Verdana 18 bold"))
        self.costPrize_l.place(x=0, y=200)

        self.sellPrize_l = Label(master, text="Enter Selling Prize", font=("Verdana 18 bold"))
        self.sellPrize_l.place(x=0, y=250)

        self.vendor_l = Label(master, text="Enter the Vendor Name", font=("Verdana 18 bold"))
        self.vendor_l.place(x=0, y=300)

        self.vendor_phone_l = Label(master, text="Enter the Vendor Number", font=("Verdana 18 bold"))
        self.vendor_phone_l.place(x=0, y=350)

        self.status_l=Label(master,text="Status",font=("Verdana 18 bold"))
        self.status_l.place(x=0,y=450)


        # Entry widgets for user input
        self.id_e = Entry(master,width=25,font=("arial 18"))
        self.id_e.place(x=380,y=400)

        self.category_e=ttk.Combobox(master, width=24,values=("Select","Rexine","Velvet","Carpet"),state='readonly',justify=CENTER,font=("arial 18"))
        self.category_e.place(x=380,y=55)
        self.category_e.current(0)

        self.product_name_e = Entry(master,width=25,font=("arial 18"))
        self.product_name_e.place(x=380,y=100)

        self.stock_e = Entry(master,width=25,font=("arial 18"))
        self.stock_e.place(x=380,y=150)

        self.costPrize_e = Entry(master,width=25,font=("arial 18"))
        self.costPrize_e.place(x=380,y=200)

        self.sellPrize_e = Entry(master,width=25,font=("arial 18"))
        self.sellPrize_e.place(x=380,y=250)

        self.vendor_e = Entry(master,width=25,font=("arial 18"))
        self.vendor_e.place(x=380,y=300)

        self.vendor_phone_e = Entry(master,width=25,font=("arial 18"))
        self.vendor_phone_e.place(x=380,y=350)

        self.status_e=ttk.Combobox(master,width=24,values=("Select","Active","Inactive"),state='readonly',justify=CENTER,font=("Arial 18"))
        self.status_e.place(x=380,y=450)
        self.status_e.current(0)


        # Button to add the entered data to the database
        self.btn_add = Button(master,text="Add to Database",font=("Arial",10,"bold"),width=30,height=3,bg="#008000",fg="#FFFFFF",bd=3,command=self.get_items,relief=RIDGE)
        self.btn_add.place(x=550,y=520,width=150,height=50)

        image_path = (r"D:\Rexine Store Management\Icons\clear3.png")
        clear_symbol = Image.open(image_path)
        clear_symbol = clear_symbol.resize((30, 30), Image.Resampling.LANCZOS)
        self.clear_symbol_tk = ImageTk.PhotoImage(clear_symbol)
        # Button to clear all input fields
        self.btn_clear = Button(master, text="    Clear All",font=("Arial",10,"bold"), image=self.clear_symbol_tk, compound=tk.LEFT, width=30, height=3, bg='#FFFFFF',fg='#FF0000',bd=5,command=self.clear_all,relief=RIDGE)
        self.btn_clear.place(x=380, y=520,width=150,height=50)

        # Text box for logging purposes
        self.tBox = Text(master,width=60,height=21,bg="#87CEEB")
        self.tBox.place(x=750,y=100)
        self.tBox.insert(END, "ID has reached upto: "+str(id))

    # Method to retrieve and process the data from input fields
    def get_items(self,*args,**kwargs):
        # Extracting/Get data from Entry widgets
        self.category = self.category_e.get()
        self.product_name = self.product_name_e.get()
        self.stock = self.stock_e.get()
        self.costPrize = self.costPrize_e.get()
        self.sellPrize = self.sellPrize_e.get()
        self.vendor = self.vendor_e.get()
        self.vendor_phone = self.vendor_phone_e.get() 
        self.status = self.status_e.get()


        # Calculating total cost and selling price
        self.totalcp = float(self.costPrize) * float(self.stock) if self.costPrize and self.stock else 0.0
        try:
             self.totalsp = float(self.sellPrize) * float(self.stock)
        except ValueError:
            self.totalsp = 0.0 

        # Calculating assumed profit
        self.assumed_profit = float(self.totalsp) - float(self.totalcp)

        # Validating user input and executing SQL query to insert data
        if self.category == ''or self.product_name == '' or self.stock == '' or self.costPrize == '' or self.sellPrize == '' or self.vendor == '' or self.vendor_phone == '':
            tkinter.messagebox.showinfo("Error","Please fill all the entries.")
        else:
            sql = "INSERT INTO inventory (category, product_name, stock, costPrize, sellPrize, totalcp, totalsp, assumed_profit, vendor, vendor_phone,status) VALUES(?,?,?,?,?,?,?,?,?,?,?)"
            c.execute(sql,(self.category,self.product_name,self.stock,self.costPrize,self.sellPrize,self.totalcp,self.totalsp,self.assumed_profit,self.vendor,self.vendor_phone,self.status))
            conn.commit()
            #The succesful insertion
            self.tBox.insert(END,"\n \nInserted " +str(self.category) + " Into the database with ID, " + str(self.id_e.get()))
            tkinter.messagebox.showinfo("Success","Sucessfully added to the database")

    # Method to clear all the input fields
    def clear_all(self,*args,**kwargs):
        self.id_e.delete(0, END)
        self.category_e.set("Select")
        self.product_name_e.delete(0, END)
        self.stock_e.delete(0, END)
        self.costPrize_e.delete(0, END)
        self.sellPrize_e.delete(0, END)
        self.vendor_e.delete(0, END)
        self.vendor_phone_e.delete(0, END)
        self.status_e.set("Select")

    def go_back(self):
        self.master.destroy()  # Close the current window
        import home  # Import and run home.py (make sure home.py is in the same directory)

# Main loop to run the application
root=Tk()
b = Database(root)

root.geometry("1366x700+50+100")
root.title("Add to the Database")

root.mainloop()
