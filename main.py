# import necessary modules
from tkinter import *
import sqlite3
import tkinter.messagebox
import datetime
import math
import os
import random

# Establish connection to the database
conn = sqlite3.connect("D:\Rexine Store Management\Database\store.db")
c = conn.cursor()

# Get the current date and format it
date = datetime.datetime.now().date()
formatted_date = date.strftime("%d/%m/%Y")

# Initialize temporary lists to store session data
products_list = []  # Stores product serial numbers
product_price = []
product_quantity = []   # Stores product quantities
product_id = []

# Initialize a list to store dynamically created label widgets
labels_list = []


# Define the main application class
class Application :
    def __init__(self, master, *args, **kwargs):
        # Set up the main window (root) and its components
        self.master = master
        
        # Create left and right frames in the main window
        self.left= Frame(master,width=720,height=780,bg="white")
        self.left.pack(side=LEFT)

        self.right= Frame(master,width=646,height=780,bg="lightgrey") #width --> 1366 - 720 = 646
        self.right.pack(side=RIGHT)

         # Heading label for the store name
        self.heading = Label(self.left, text="REXINE STORE",font=("Times New Roman",40,"bold"), bg="white",fg="black" )
        self.heading.place(x=0,y=0)

        # Label to display the current date
        self.date_l = Label(self.right, text="Today's Date: " +str(formatted_date), font=("arial 16 bold"), bg='lightgrey',fg='black')
        self.date_l.place(x=0,y=0)

        # Labels for the table headers in the invoice section
        self.tproduct_name = Label(self.right,text="Product Name",font=('arial 18 bold'), bg='lightgrey',fg='black')
        self.tproduct_name.place(x=0,y=60)

        self.tquantity = Label(self.right,text="Quantity",font=('arial 18 bold'), bg='lightgrey',fg='black')
        self.tquantity.place(x=300,y=60)

        self.tamount = Label(self.right,text="Amount",font=('arial 18 bold'), bg='lightgrey',fg='black')
        self.tamount.place(x=500,y=60)

        # Label and entry field for entering the product ID
        self.enterid = Label(self.left,text="Enter Product's ID", font=('arial 17 bold'),bg='white')
        self.enterid.place(x=0,y=80)

        self.enteride = Entry(self.left, width=25,font=('arial 18 bold'), bg='lightgrey')
        self.enteride.place(x=210, y=80)
        self.enteride.focus()

        # Search button to trigger the product search
        self.search_btn = Button(self.left, text='Search',font=("Arial",12,"bold"), width=22, height=2,bg='black',fg="white", command=self.ajax,bd=4,relief=RIDGE)
        self.search_btn.place(x=370,y=120)

        # Labels for displaying product details after search
        self.sproduct_name = Label(self.left, text="", font=('arial 27 bold'),bg='white' )
        self.sproduct_name.place(x=0,y=220)

        self.pprice = Label(self.left, text="", font=('arial 27 bold'),bg='white')
        self.pprice.place(x=0,y=270)

        # Label to display the total amount of the invoice
        self.total_l = Label(self.right,text="",font=('arial 37 bold'),bg="lightgrey",fg='black')
        self.total_l.place(x=0,y=600)

        # Display the change in a new label
        self.c_amount = Label(self.left, font=('arial 18 bold'),fg='red',bg='white')
        self.c_amount.place(x=0,y=600)
        self.c_amount.configure(text="")


    # Function to search for a product in the database
    def ajax(self,*args,**kwargs):
        self.get_id = self.enteride.get() # Get the product ID from the entry field

        # SQL query to fetch product details based on the ID
        query = "SELECT * FROM inventory WHERE id=?"
        result = c.execute(query, (self.get_id, )) 

        product_found = False  # Flag to check if the product exists
        for self.r in result:
            product_found = True  # Set flag to true if product is found
            self.get_id = self.r[0]
            self.get_product_name = self.r[2]
            self.get_price = self.r[5]
            self.get_stock = self.r[3]

        # Check if the product was found
        if product_found:
            # Display product details in the labels
            self.sproduct_name.configure(text="Product Name: " + str(self.get_product_name))
            self.pprice.configure(text="Price: Rs." + str(self.get_price))

            # Create the quantity and discount table
            self.quantity_l = Label(self.left, text="Enter Quantity", font=('arial 18 bold'), bg='white')
            self.quantity_l.place(x=0,y=370)

            self.quantity_e = Entry(self.left, width=25, font=('arial 18 bold'), bg='lightgrey')
            self.quantity_e.place(x=180,y=370)
            self.quantity_e.focus()

            self.discount_l = Label(self.left, text="Enter Discount", font=('arial 18 bold'), bg='white')
            self.discount_l.place(x=0,y=410)

            self.discount_e = Entry(self.left, width=25, font=('arial 18 bold'), bg='lightgrey')
            self.discount_e.place(x=180,y=410)
            self.discount_e.insert(END,0)

            # Button to add the product to the cart
            self.add_to_cart_btn = Button(self.left, text='Add to Shopping cart',font=("Arial",12,"bold"), width=22, height=2,bg='black',fg="white",command=self.add_to_cart,bd=4,relief=RIDGE)
            self.add_to_cart_btn.place(x=350,y=450)

            # Input fields for the amount given by the customer and button to calculate change
            self.change_l = Label(self.left, text='Given Amount', font=('arial 18 bold'),bg='white')
            self.change_l.place(x=0,y=550)

            self.change_e = Entry(self.left, width=25, font=('arial 18 bold'),bg='lightgrey')
            self.change_e.place(x=190,y=550)

            self.change_btn = Button(self.left, text='Calculate Change',font=("Arial",12,"bold"),width=22, height=1,bg='black',fg="white",command=self.change_func,bd=4,relief=RIDGE)
            self.change_btn.place(x=350,y=590)

            # Button to generate the bill
            self.bill_btn = Button(self.left, text='Genarate Bill', width=70, height=2,font=("Arial",12,"bold"),bg="green",fg='white',command=self.generate_bill,bd=4,relief=RIDGE)
            self.bill_btn.place(x=0,y=640)

        else:
            # Display error message if the product is not found
            tkinter.messagebox.showinfo("Error", "Product not found.")

        
    # Function to add the product to the cart
    def add_to_cart(self,*args,**kwargs):
        # Check if the quantity field is empty
        quantity_text = self.quantity_e.get().strip()
        if not quantity_text:
            tkinter.messagebox.showinfo("Error", "Please enter the quantity.")
            return  # Exit the function if quantity is not provided
        # Get the quantitiy value from the database
        # Validate if the input is an integer
        try:
            self.quantity_value = int(self.quantity_e.get())  # Convert to integer
        except ValueError:
            tkinter.messagebox.showinfo("Error", "Please enter a valid integer quantity.")
            return  # Exit if the input is not an integer
        # Validate if the input is an integer for discount
        try:
            self.discount_value = int(self.discount_e.get())  # Convert to integer
        except ValueError:
            tkinter.messagebox.showinfo("Error", "Please enter a valid integer discount.")
            return  # Exit if the input is not an integer
                
        # Check if the requested quantity is available in stock
        if self.quantity_value > int(self.get_stock):
            tkinter.messagebox.showinfo("Error","Not that many product in our inventory..'AVAILABLE SOON'")
        else:
            # Calculate the final price after applying the discount
            self.final_price = (float(self.quantity_value) * float(self.get_price)) - (float(self.discount_e.get()))
            products_list.append(self.get_product_name) # Add product serial number to the list
            product_price.append(self.final_price)  # Add final price to the list
            product_quantity.append(self.quantity_value)  # Add quantity to the list
            product_id.append(self.get_id)  # Add product ID to the list

            # Display the added products in the invoice section
            self.x_index = 0
            self.y_index = 100
            self.counter = 0
            for self.p in products_list:
                self.tempproduct_name = Label(self.right, text=str(products_list[self.counter]),font=('arial 18 bold'),bg='lightgrey',fg='black')
                self.tempproduct_name.place(x=0,y=self.y_index)
                labels_list.append(self.tempproduct_name)

                self.tempqt = Label(self.right, text=str(product_quantity[self.counter]),font=('arial 18 bold'),bg='lightgrey',fg='black')
                self.tempqt.place(x=300,y=self.y_index)
                labels_list.append(self.tempqt)

                self.tempprice = Label(self.right, text=str(product_price[self.counter]),font=('arial 18 bold'),bg='lightgrey',fg='black')
                self.tempprice.place(x=500,y=self.y_index)
                labels_list.append(self.tempprice)

                self.y_index += 40 
                self.counter += 1

                # Update the total amount
                self.total_l.configure(text="Total: Rs. " + str(sum(product_price)))

                # Remove the quantity and discount input fields and reset labels
                self.quantity_l.place_forget()
                self.quantity_e.place_forget()
                self.discount_l.place_forget()
                self.discount_e.place_forget()
                self.sproduct_name.configure(text='')
                self.pprice.configure(text='')
                self.add_to_cart_btn.destroy()

    # Function to calculate the change to be returned to the customer
    def change_func(self,*args,**kwargs):
        # Check if the amount field is empty
        amount_text = self.change_e.get().strip()
        if not amount_text:
            tkinter.messagebox.showinfo("Error", "Please enter the amount.")
            return  # Exit the function if amount is not provided

        # Validate if the input is an integer
        try:
            self.amount_given = int(self.change_e.get())  # Convert to integer
        except ValueError:
            tkinter.messagebox.showinfo("Error", "Please enter a valid integer amount.")
            return  # Exit if the input is not an integer
        self.our_total = float(sum(product_price))  # Calculate the total amount
        self.to_give = self.amount_given - self.our_total # Calculate the change


        # Display the change in the pre-initialized label
        self.c_amount.configure(text="Change: Rs. " +str(self.to_give))

    # Function to generate the bill and save it in the database
    def generate_bill(self, *args, **kwargs):
        # Check if any products have been added to the cart
        if not products_list:
            tkinter.messagebox.showinfo("Error", "No products in the cart. Please add products before generating the bill.")
            return  # Exit the function if the cart is empty

        # Create a new window for displaying the bill
        directory = "D:/Rexine Store Management/Invoice/"+str(date)+ "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Templates for the bill (ESCAPE SEQUENCE CHARACTERS '\')
        company = "\t\t\tRuby Fashion Corporation Pvt. Ltd.\n"
        address = "\t\t\tWadala Antop Hill, Mumbai, 400037, Maharahtra.\n"
        phone = "\t\t\tContact : XXXX086XXX"
        dt = "\t\t\t\tDate :" + str(formatted_date) +"\n\n\n"
        sample = "\t\t\t\t\t\t____INVOICE____"
        

        table_header = "\n\n\t\t----------------------------------------------------------\n\t\tSerial No.\tProduct Name\tQuantity\t\tAmount\n\n\t\t----------------------------------------------------------"
        final = company + address + phone + dt + sample + "\n" + table_header

        # Open a file to write mode
        file_name = str(directory)+str(random.randrange(5000, 10000)) + ".rtf"
        f = open(file_name, 'w')
        f.write(final)
        # Fill dynamics
        r = 1
        i = 0
        for t in products_list:
            f.write("\n\t\t" + str(r) + "\t\t" + str(products_list[i]) + "\t\t\t" + str(product_quantity[i]) + "\t\t\t" + str(product_price[i]))
            i += 1
            r += 1
        f.write("\n\n\n\t\t\t\t\t\t\tTotal: Rs. " + str(sum(product_price)))
        f.write("\n\t\t\t\t\t\t\tThanks For Buying Product.")
        f.write("\n\t\t----------------------------------------------------------")
        os.startfile(file_name,"print")
        f.close()
        
        # Decrease the stock
        self.x = 0

        initial = "SELECT * FROM inventory WHERE id =?"
        result = c.execute(initial, (product_id[self.x], ))

        for i in products_list: 
            for r in result:
                self.old_stock = r[3]
            self.new_stock = int(self.old_stock) - int(product_quantity[self.x])

            # Update the stock
            sql = "UPDATE inventory SET stock=? WHERE id = ?"
            c.execute(sql,(self.new_stock, product_id[self.x]))
            conn.commit()

            # Insert into the transaction
            sql2 = "INSERT INTO transactions (product_name, quantity, amount, date) VALUES (?,?,?,?)"
            c.execute(sql2, (products_list[self.x], product_quantity[self.x], product_price[self.x], date))
            conn.commit()

            self.x += 1

        # Clear labels and lists after generating the bill
        for a in labels_list:
            a.destroy()
            
        del(products_list[:])
        del(product_id[:])
        del(product_quantity[:])
        del(product_price[:])

        self.total_l.configure(text="") 
        self.c_amount.configure(text="")
        self.change_e.delete(0,END)
        self.enteride.delete(0,END)
    
        tkinter.messagebox.showinfo("Success","Bill generated and printed successfully.")

# Initialize the main application window and run the application
root = Tk()
b = Application(root)
root.geometry("1366x768+50+20")
root.title("Bill Generate!")

root.mainloop() 