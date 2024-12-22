from tkinter import *
from PIL import Image,ImageTk #pip install pillow , Required for image processing
from tkinter import ttk,messagebox
import sqlite3


class categoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x550+220+130") # Define the window size and position
        self.root.title("Category Management System")
        self.root.config(bg="#FFFFFF") 
        self.root.focus_force()
        
        # Variables for storing input data from user entries
        self.var_cat_id=StringVar()
        self.var_main_name=StringVar()
        self.var_sub_name=StringVar()

        # Title Label at the top of the window
        lbl_title=Label(self.root,text="Manage Product Category",font=("goudy old style",30,"bold"),bg="#2a2f4f",fg="#FFFFFF",bd=3,relief=RIDGE)
        lbl_title.pack(side=TOP,fill=X,padx=10,pady=10)
        
        # Frame to hold entry fields and buttons   
        entry_frame=Frame(self.root,bd=3,relief=RIDGE,bg="#FFFFFF")
        entry_frame.place(x=30,y=80,width=510,height=450)

        # Labels fields for Category ID and Name
        lbl_cid=Label(entry_frame,text="   Category ID",font=("goudy old style",20),bg="#FFFFFF")
        lbl_cid.place(x=10,y=10)
        lbl_m_name=Label(entry_frame,text="Category Name",font=("goudy old style",20),bg="#FFFFFF")
        lbl_m_name.place(x=10,y=60)

        # Entry fields for Category ID and Name
        lbl_cid=Entry(entry_frame,textvariable=self.var_cat_id,font=("goudy old style",20),bg="lightyellow")
        lbl_cid.place(x=250,y=10,width=200)
        lbl_m_name=Entry(entry_frame,textvariable=self.var_main_name,font=("goudy old style",20),bg="lightyellow")
        lbl_m_name.place(x=250,y=60,width=200)

        # Buttons for adding and deleting categories
        btn_add=Button(entry_frame,text="Add",command=self.add,font=("goudy old style",15,"bold"),bg="#008000",fg="#FFFFFF",cursor="hand2",relief=RIDGE)
        btn_add.place(x=250,y=150,width=250,height=50)
        btn_delete=Button(entry_frame,text="Delete",command=self.delete,font=("goudy old style",15,"bold"),bg="#ff0000",fg="#FFFFFF",cursor="hand2",relief=RIDGE)
        btn_delete.place(x=250,y=220,width=250,height=50)
        btn_clear=Button(entry_frame,text="Clear All",command=self.clear,font=("goudy old style",15,"bold"),bg="#000000",fg="#FFFFFF",cursor="hand2",relief=RIDGE)
        btn_clear.place(x=250,y=290,width=250,height=50)

        # Frame to display category details in a table format       
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=570,y=80,width=490,height=450)

        # Scrollbars for the table
        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        # Treeview widget to display category details
        self.CategoryTable=ttk.Treeview(cat_frame,columns=("cid","m_name"))
        scrollx.pack(side=BOTTOM,fill=X)  # Horizontal scrollbar
        scrolly.pack(side=RIGHT,fill=Y)   # Vertical scrollbar
        scrollx.config(command=self.CategoryTable.xview)  # Link scrollbar to treeview
        scrolly.config(command=self.CategoryTable.yview)  # Link scrollbar to treeview

        # Define table headings
        self.CategoryTable.heading("cid",text="Category ID")
        self.CategoryTable.heading("m_name",text="Main Category")
        self.CategoryTable["show"]="headings"

        # Define column widths for the table
        self.CategoryTable.column("cid",width=80)
        self.CategoryTable.column("m_name",width=100)
        self.CategoryTable.pack(fill=BOTH,expand=1)

        # Bind event to capture selected row data
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()  # Populate table with existing data


    def cat_apmc(self):
        # Placeholder method for any additional functionality
        self.new_win=Toplevel(self.root)

    def add(self):
        # Establish a connection to the SQLite database
        conn = sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            if self.var_cat_id.get()=="":  # Validation check for empty input
                messagebox.showerror("Error","All Fields must be required",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row!=None:  # Check if the category ID already exists
                    messagebox.showerror("Error","This Category ID is Alreary Assigned, try different",parent=self.root)
                else:
                    # Insert new category data into the database
                    cur.execute("Insert into category(cid,m_name) values(?,?)",(
                                        self.var_cat_id.get(),
                                        self.var_main_name.get()
                    ))
                    conn.commit()
                    messagebox.showinfo("Succes","Category Added Successfully",parent=self.root)
                    self.show() # Refresh the table to display the new category
        
        except Exception as ex: # Exception handling for database operations
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def show(self):
        # Method to retrieve and display categories from the database
        conn = sqlite3.connect("D:\Rexine Store Management\Database\store.db")        
        cur=conn.cursor()
        try:
            cur.execute("Select * from category")
            rows=cur.fetchall()  # Fetch all rows from the category table
            self.CategoryTable.delete(*self.CategoryTable.get_children()) # Clear the existing table content
            for row in rows:
                self.CategoryTable.insert('',END,values=row) # Insert each row into the table
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def get_data(self,ev):
        # Method to capture selected row data from the table
        f = self.CategoryTable.focus()  # Get the currently focused item
        content=(self.CategoryTable.item(f))
        row=content['values']
        # Set the captured data into the respective entry fields
        self.var_cat_id.set(row[0])
        self.var_main_name.set(row[1])
        
    def delete(self):
        # Method to delete the selected category from the database
        conn = sqlite3.connect("D:\Rexine Store Management\Database\store.db")
        cur=conn.cursor()
        try:
            if self.var_cat_id.get()=="":  # Validation check for empty selection
                messagebox.showerror("Error","please select category from the list",parent=self.root)
            else:
                cur.execute("Select * from category where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None: # Check if the category exists in the database
                    messagebox.showerror("Error","Error, please try again",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:  # Confirmation prompt before deletion
                        cur.execute("delete from category where cid=?",(self.var_cat_id.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete","Category ID Deleted Successfully",parent=self.root)
                        self.show() # Refresh the table after deletion

                        # Clear the entry fields
                        self.var_cat_id.set("")
                        self.var_main_name.set("")
        # Exception handling for database operations   
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def clear(self):
        self.var_cat_id.set("")
        self.var_main_name.set("")
        self.show()

# Entry point of the application
if __name__=="__main__":
    root=Tk()
    
    obj=categoryClass(root)
    root.mainloop()
