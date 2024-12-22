#import all modules
from tkinter import *
import sqlite3
import tkinter.messagebox
from tkinter import ttk,messagebox

# Establish a connection to the SQLite database
conn = sqlite3.connect("D:\Rexine Store Management\Database\store.db")
c = conn.cursor()

# Fetch the maximum ID from the inventory table
result = c.execute("SELECT Max(id) from inventory")
for r in result:
    id = r[0]


# Define the Database class to manage inventory data within the GUI
class Database:
    def __init__(self,master,*args,**kwargs):
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_id=StringVar()
        self.var_category=StringVar()
        self.var_product_name=StringVar()
        self.var_stock=StringVar()
        self.var_costPrize=StringVar()
        self.var_sellPrize=StringVar()
        self.var_totalcp=StringVar()
        self.var_totalsp=StringVar()
        self.var_assumed_profit=StringVar()
        self.var_vendor=StringVar()
        self.var_vendor_phone=StringVar()
        self.var_status=StringVar()

        # Set the master widget (root window) and configure the heading label
        self.master = master
        self.heading = Label(master,text="Update Products", font=('goudy old style',20,"bold"),fg='white',bg="#2A2F4F")
        self.heading.place(x=0,y=0,width=1370,height=40)
    
        # Label definitions for the inventory fields
        self.id_l = Label(master,text="Enter ID", font=("arial 18 bold"))
        self.id_l.place(x=0,y=70)

        self.category_l=Label(master,text="Enter Category",font=("arial 18 bold"))
        self.category_l.place(x=0, y=120) 

        self.product_name_l = Label(master, text="Enter The Product Name", font=("arial 18 bold"))
        self.product_name_l.place(x=0, y=170)

        self.stock_l = Label(master, text="Enter Available Stock", font=("arial 18 bold"))
        self.stock_l.place(x=0, y=220)

        self.costPrize_l = Label(master, text="Enter Cost Price", font=("arial 18 bold"))
        self.costPrize_l.place(x=0, y=270)

        self.sellPrize_l = Label(master, text="Enter Selling Price", font=("arial 18 bold"))
        self.sellPrize_l.place(x=0, y=320)

        self.totalcp_l = Label(master, text="Enter Total Cost Price", font=("arial 18 bold"))
        self.totalcp_l.place(x=0, y=370)

        self.totalsp_l = Label(master, text="Enter Total Selling Price", font=("arial 18 bold"))
        self.totalsp_l.place(x=0, y=420)

        self.assumed_profit = Label(master, text="Assumed Profit", font=("arial 18 bold"))
        self.assumed_profit.place(x=0, y=470)

        self.vendor_l = Label(master, text="Enter the Vendor Name", font=("arial 18 bold"))
        self.vendor_l.place(x=0, y=520) 

        self.vendor_phone_l = Label(master, text="Enter the Vendor Number", font=("arial 18 bold"))
        self.vendor_phone_l.place(x=0, y=570)

        self.status=Label(master,text="Status",font=("arial 18 bold"))
        self.status.place(x=0,y=620) 

        # Entry widgets for user input corresponding to the labels defined above
        self.id_e = Entry(master, font=("arial 18"), width=25)
        self.id_e.place(x=380, y=70)

        self.category_e=ttk.Combobox(master, width=24,values=("Select","Rexine","Velvet","Carpet"),state='readonly',justify=CENTER,font=("arial 18"))
        self.category_e.place(x=380,y=120)
        self.category_e.current(0)

        self.product_name_e = Entry(master,width=25,font=("arial 18"))
        self.product_name_e.place(x=380,y=170)

        self.stock_e = Entry(master,width=25,font=("arial 18"))
        self.stock_e.place(x=380,y=220)

        self.costPrize_e = Entry(master,width=25,font=("arial 18"))
        self.costPrize_e.place(x=380,y=270)

        self.sellPrize_e = Entry(master,width=25,font=("arial 18"))
        self.sellPrize_e.place(x=380,y=320)

        self.totalcp_e = Entry(master,width=25,font=("arial 18"))
        self.totalcp_e.place(x=380,y=370)

        self.totalsp_e = Entry(master,width=25,font=("arial 18"))
        self.totalsp_e.place(x=380,y=420)

        self.assumed_profit_e = Entry(master,width=25,font=("arial 18"))
        self.assumed_profit_e.place(x=380,y=470)

        self.vendor_e = Entry(master,width=25,font=("arial 18"))
        self.vendor_e.place(x=380,y=520)

        self.vendor_phone_e = Entry(master,width=25,font=("arial 18"))
        self.vendor_phone_e.place(x=380,y=570)

        self.status_e=ttk.Combobox(master,width=24,values=("Select","Active","Inactive"),state='readonly',justify=CENTER,font=("arial 18"))
        self.status_e.place(x=380,y=620)
        self.status_e.current(0)

        # Buttons to handle update, delete, and clear operations on the database
        self.btn_add = Button(master, text="Update",width=17,height=2,font=("Arial",10,"bold"),bg='#008000',fg="#FFFFFF",bd=3,command=self.update,relief=RIDGE)
        self.btn_add.place(x=550,y=670)

        self.btn_add = Button(master, text="Delete",width=17,height=2,font=("Arial",10,"bold"),bg="#FF0000",fg="#FFFFFF",bd=3,command=self.delete,relief=RIDGE)
        self.btn_add.place(x=380,y=670)

        self.btn_clear = Button(master,text="Clear All",width=17,height=2,font=("Arial",10,"bold"),bg="blue",fg='#FFFFFF',bd=3,command=self.clear_all,relief=RIDGE)
        self.btn_clear.place(x=210, y=670)

        # Search frame configuration with associated input and button
        SearchFrame=LabelFrame(root,text="Search Product",font=("goudy old style",12))
        SearchFrame.place(x=750,y=60,width=600,height=80)

        #===options===
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Vendor","Product_Name"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search1,font=("goudy old style",15,"bold"),bg="blue",fg="white",bd=3,cursor="hand2",relief=RIDGE).place(x=410,y=9,width=150,height=30)

        # Frame to display product details in a Treeview table
        product_frame=Frame(root,bd=3,relief=RIDGE)
        product_frame.place(x=750,y=170,width=600,height=390)

        # Scrollbars for the Treeview widget
        scrolly=Scrollbar(product_frame,orient=VERTICAL)
        scrollx=Scrollbar(product_frame,orient=HORIZONTAL)

        self.ProductTable=ttk.Treeview(product_frame,columns=("id","category", "product_name", "stock", "costPrize", "sellPrize", "totalcp", "totalsp", "assumed_profit", "vendor", "vendor_phone","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=TOP,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)

        # Define the headings for each column in the Treeview widget
        self.ProductTable.heading("id",text="ID")
        self.ProductTable.heading("category",text="Category")
        self.ProductTable.heading("product_name",text="Product Name")
        self.ProductTable.heading("stock",text="Stock")
        self.ProductTable.heading("costPrize",text="Cost Prize")
        self.ProductTable.heading("sellPrize",text="Sell Prize")
        self.ProductTable.heading("totalcp",text="Total C.P")
        self.ProductTable.heading("totalsp",text="Total S.P")
        self.ProductTable.heading("assumed_profit",text="Assumed Profit")
        self.ProductTable.heading("vendor",text="Vendor")       
        self.ProductTable.heading("vendor_phone",text="Vendor No.")
        self.ProductTable.heading("status",text="Status")
        self.ProductTable["show"]="headings"

        # Set the column width for each column in the Treeview widget
        self.ProductTable.column("id",width=50)
        self.ProductTable.column("category",width=100)
        self.ProductTable.column("product_name",width=100)
        self.ProductTable.column("stock",width=50)
        self.ProductTable.column("costPrize",width=80)
        self.ProductTable.column("sellPrize",width=80)
        self.ProductTable.column("totalcp",width=80)
        self.ProductTable.column("totalsp",width=80)
        self.ProductTable.column("assumed_profit",width=100)
        self.ProductTable.column("vendor",width=100)
        self.ProductTable.column("vendor_phone",width=100)  
        self.ProductTable.column("status",width=100)

        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)
        # Load the data into the table view
        self.show() # this is show right side box,  


    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        # print(row)
        self.var_id.set(row[0])
        self.var_category.set(row[1])
        self.var_product_name.set(row[2])
        self.var_stock.set(row[3])
        self.var_costPrize.set(row[4])
        self.var_sellPrize.set(row[5])
        self.var_totalcp.set(row[6])
        self.var_totalsp.set(row[7])
        self.var_assumed_profit.set(row[8])
        self.var_vendor.set(row[9])
        self.var_vendor_phone.set(row[10])
        self.var_status.set(row[11])

        # Update the entry widgets directly
        self.id_e.insert(0, row[0])
        self.category_e.set(row[1])
        self.product_name_e.insert(0, row[2])
        self.stock_e.insert(0, row[3])
        self.costPrize_e.insert(0, row[4])
        self.sellPrize_e.insert(0, row[5])
        self.totalcp_e.insert(0, row[6])
        self.totalsp_e.insert(0, row[7])
        self.assumed_profit_e.insert(0, row[8])
        self.vendor_e.insert(0, row[9])
        self.vendor_phone_e.insert(0, row[10])
        self.status_e.set(row[11])

    
    def update(self, *args, **kwargs):
        #get all the update values
        self.u0 = self.id_e.get()
        self.u1 = self.category_e.get()
        self.u2 = self.product_name_e.get()
        self.u3 = self.stock_e.get()
        self.u4 = self.costPrize_e.get()
        self.u5 = self.sellPrize_e.get()
        self.u6 = self.totalcp_e.get()
        self.u7 = self.totalsp_e.get()
        self.u8 = self.assumed_profit_e.get()
        self.u9 = self.vendor_e.get()
        self.u10 = self.vendor_phone_e.get()
        self.u11 = self.status_e.get()

        query = "UPDATE inventory SET category=?, product_name=?, stock=?, costPrize=?, sellPrize=?, totalcp=?, totalsp=?, assumed_profit=?, vendor=?, vendor_phone=?, status=? WHERE id=?"
        c.execute(query, (self.u1, self.u2, self.u3, self.u4, self.u5, self.u6, self.u7, self.u8, self.u9,self.u10, self.u11, self.id_e.get()))
        conn.commit()
        tkinter.messagebox.showinfo("Success", "Updated Database Successfully")
        self.show()

    def show(self):
        conn = sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            cur.execute("Select * from inventory")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=root)
    
    # Function to delete the selected product from the database
    def delete(self):
        conn = sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            if self.id_e.get()=="": 
                messagebox.showerror("Error","please select Product for deleting",parent=root)
            else:
                cur.execute("Select * from inventory where id=?",(self.id_e.get(),))    
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Error, Invalid ID",parent=root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=root)
                    if op==True:
                        cur.execute("delete from inventory where id=?",(self.id_e.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=root)
                        self.show()
                        self.clear_all()
                        

        except Exception as ex:
            # Handle exceptions during the deletion operation
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=root)
        
    def search1(self):
        conn = sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search By Option",parent=root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search Input is Required",parent=root)
            else:
                cur.execute("Select * from inventory where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found!!!",parent=root)
        except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=root)

    def clear_all(self,*args,**kwargs):
        self.id_e.delete(0, END)
        self.category_e.set("Select")
        self.product_name_e.delete(0, END)
        self.stock_e.delete(0, END)
        self.costPrize_e.delete(0, END)
        self.sellPrize_e.delete(0, END)
        self.totalcp_e.delete(0, END)
        self.totalsp_e.delete(0, END)
        self.assumed_profit_e.delete(0, END)
        self.vendor_e.delete(0, END)
        self.vendor_phone_e.delete(0, END)
        self.status_e.set("Select")

# Initializing the main application window
root=Tk()
b = Database(root)
root.geometry("1366x768+50+30")
root.title("Update the database")

root.mainloop()

