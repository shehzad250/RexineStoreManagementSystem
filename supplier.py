from tkinter import *
from PIL import Image,ImageTk # pip install pillow
from tkinter import ttk,messagebox
import sqlite3

class supplierClass:
    def __init__(self,root):
        # Initialize the main window
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Supplier Management System")
        self.root.config(bg="#fafafa")
        self.root.focus_force()

        # Define all variables used to capture user inputs
        self.var_searchtxt=StringVar()
        self.var_supid=StringVar()
        self.var_company=StringVar()
        self.var_name=StringVar()
        self.var_contact=StringVar()

        # Create a search frame for searching suppliers
        SearchFrame=LabelFrame(self.root,text="Search Supplier",font=("goudy old style",12),bd=2,relief=RIDGE,bg="#fafafa")
        SearchFrame.place(x=470,y=40,width=600,height=90)

        # Add label and search box to the search frame
        lbl_search=Label(SearchFrame,text="Search By Supplier ID",font=("goudy old style",15),bg="#fafafa")
        lbl_search.place(x=10,y=10,width=180)
        
        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",18),bg="#D3D3D3").place(x=200,y=10,width=210)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="#0000FF",fg="#FFFFFF",cursor="hand2",relief=RIDGE).place(x=430,y=10,width=150,height=30)

        # Add a title label at the top of the main window
        title=Label(self.root,text="Supplier Details",font=("goudy old style",20,"bold"),bg="#2a2f4f",fg="#FFFFFF").place(x=0,y=0,width=1100,height=40)


        # Create and place labels and entry fields for supplier details   
        lbl_supid=Label(self.root,text="Supplier ID",font=("goudy old style bold",18),bg="#fafafa").place(x=50,y=150)
        txt_supid=Entry(self.root,textvariable=self.var_supid,font=("goudy old style ",18),bg="#D3D3D3").place(x=220,y=150,width=210)
        
        lbl_company=Label(self.root,text="Company",font=("goudy old style bold",18),bg="#fafafa").place(x=50,y=200)
        txt_company=Entry(self.root,textvariable=self.var_company,font=("goudy old style ",18),bg="#D3D3D3").place(x=220,y=200,width=210)
        
        lbl_name=Label(self.root,text="Supplier Name",font=("goudy old style bold",18),bg="#fafafa").place(x=50,y=250)        
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style ",18),bg="#D3D3D3").place(x=220,y=250,width=210)
        
        lbl_contact=Label(self.root,text="Contact",font=("goudy old style bold",18),bg="#fafafa").place(x=50,y=300)       
        txt_contact=Entry(self.root,textvariable=self.var_contact,font=("goudy old style ",18),bg="#D3D3D3").place(x=220,y=300,width=210)
        
       
        # Add buttons for Save, Update, Delete, and Clear operations
        btn_add=Button(self.root,text="Save",command=self.add,font=("goudy old style",15,"bold"),bg="#008000",fg="#FFFFFF",cursor="hand2",bd=3,relief=RIDGE)
        btn_add.place(x=20,y=450,width=130,height=40)
        btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",15,"bold"),bg="#800080",fg="#FFFFFF",cursor="hand2",bd=3,relief=RIDGE)
        btn_update.place(x=160,y=450,width=130,height=40)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15,"bold"),bg="#FF0000",fg="#FFFFFF",cursor="hand2",bd=3,relief=RIDGE)
        btn_delete.place(x=300,y=450,width=130,height=40)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15,"bold"),bg="#FFA500",fg="#FFFFFF",cursor="hand2",bd=3,relief=RIDGE)
        btn_clear.place(x=440,y=450,width=130,height=40)


        # Frame to display the list of suppliers
        sup_frame=Frame(self.root,bd=3,relief=RIDGE)
        sup_frame.place(x=470,y=150,width=600,height=290)

        # Scrollbars for the table that will display supplier details
        scrolly=Scrollbar(sup_frame,orient=VERTICAL)
        scrollx=Scrollbar(sup_frame,orient=HORIZONTAL)

        # Table for displaying supplier details with scrollbars linked
        self.SupplierTable=ttk.Treeview(sup_frame,columns=("supid","company","name","contact"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SupplierTable.xview)
        scrolly.config(command=self.SupplierTable.yview)
        
        # Define table headings
        self.SupplierTable.heading("supid",text="Supplier ID")
        self.SupplierTable.heading("company",text="Company")
        self.SupplierTable.heading("name",text="Name")
        self.SupplierTable.heading("contact",text="Contact")
        self.SupplierTable["show"]="headings" # Hide default heading column

        #self.SupplierTable.pack(fill=BOTH,expand=1) #mai is ko comment kya hu

        self.SupplierTable.column("supid",width=90)
        self.SupplierTable.column("company",width=100)
        self.SupplierTable.column("name",width=200)
        self.SupplierTable.column("contact",width=100)
        self.SupplierTable.pack(fill=BOTH,expand=1)
        self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()



    def sup_apmc(self):
        self.new_win=Toplevel(self.root)

    # Function to add a new supplier record to the database
    def add(self):
        conn=sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            if self.var_supid.get()=="": # Check if Supplier ID is empty
                messagebox.showerror("Error","All Fields must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where supid=?",(self.var_supid.get(),))
                row=cur.fetchone()
                if row!=None: # Check if the Supplier ID already exists
                    messagebox.showerror("Error","This Supplier ID is Alreary Assigned, try different",parent=self.root)
                else:
                     # Insert new supplier record into the database
                    cur.execute("Insert into supplier (supid,company,name,contact) values(?,?,?,?)",(
                                        self.var_supid.get(),
                                        self.var_company.get(),
                                        self.var_name.get(),
                                        self.var_contact.get(),
                    ))
                    conn.commit() # Commit changes to the database
                    messagebox.showinfo("Succes","Supplier Added Successfully",parent=self.root)
                    self.show() # Refresh the supplier list
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        # Function to retrieve and display all supplier records from the database
        conn=sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            cur.execute("Select * from supplier")
            rows=cur.fetchall()
            self.SupplierTable.delete(*self.SupplierTable.get_children()) # Clear the current table
            for row in rows:
                self.SupplierTable.insert('',END,values=row) # Insert each record into the table
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        # Function to populate form fields with the data of the selected table row
        f=self.SupplierTable.focus() # Get the focused item in the table

        content=(self.SupplierTable.item(f))
        row=content['values']
        # Set Supplier ID, Company, Name, and Contact
        self.var_supid.set(row[0])
        self.var_company.set(row[1])
        self.var_name.set(row[2])
        self.var_contact.set(row[3])

    def update(self):
        # Function to update an existing supplier record in the database
        conn=sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            if self.var_supid.get()=="": 
                messagebox.showerror("Error","All Fields must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where supid=?",(self.var_supid.get(),))
                row=cur.fetchone()
                if row==None: # Check if the Supplier ID exists
                    messagebox.showerror("Error","Invalid Supplier ID",parent=self.root)
                else:
                    # Update supplier details in the database
                    cur.execute("Update supplier set  company=?,name=?,contact=? where supid=?",(
                                        self.var_company.get(),
                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.var_supid.get()
                    ))
                    conn.commit() # Commit changes to the database
                    messagebox.showinfo("Succes","Supplier Updated Successfully",parent=self.root)
                    self.show() # Refresh the supplier list
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def delete(self):
        # Function to delete a supplier record from the database
        conn=sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            if self.var_supid.get()=="": 
                messagebox.showerror("Error","All Fields must be required",parent=self.root)
            else:
                cur.execute("Select * from supplier where supid=?",(self.var_supid.get(),))
                row=cur.fetchone()
                if row==None: # Check if the Supplier ID exists
                    messagebox.showerror("Error","Invalid Supplier ID",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True: # Confirm the deletion
                        cur.execute("delete from supplier where supid=?",(self.var_supid.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear(self):
        # Function to clear all form fields and refresh the supplier list
        self.var_supid.set("")
        self.var_company.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        # Function to search for a supplier by Supplier ID
        conn=sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            if self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Supplier ID is Required",parent=self.root)
            else:
                cur.execute("Select * from supplier where supid=?",(self.var_searchtxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.SupplierTable.delete(*self.SupplierTable.get_children()) # Clear current table
                    self.SupplierTable.insert('',END,values=row) # Display search result
                else:
                    messagebox.showerror("Error","No Record Found!!!",parent=self.root)
        except Exception as ex:
                messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
 

if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()
