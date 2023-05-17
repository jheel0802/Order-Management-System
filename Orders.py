from sqlite3.dbapi2 import complete_statement
from tkinter import*
from tkinter import ttk,messagebox
import sqlite3
from tkcalendar import Calendar, DateEntry

class order_class:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1020x540+240+105")
        self.root.title("Orders")
        self.root.config (bg="white")
        self.root.focus_force()

#===========================================================================================================================================

        self.var_order=StringVar()
        self.var_date=StringVar()
        self.var_customer=StringVar()
        self.var_product=StringVar()
        self.var_quantity=IntVar()
        self.var_status=StringVar()
        self.var_rate=IntVar()
        self.var_total=IntVar()
        self.var_serial=StringVar()
        self.var_amount=IntVar()
        self.customer_list=[]
        self.prod_list=[]
        self.fetch_customer_product()

#=========================================================================================================================================
        
        title=Label(self.root,text="Orders",font=("arial",35,"bold"),bg="light blue").pack(side=TOP,fill=X)

        lbl_order=Label(self.root,text="Order No.",font=("Times New Roman",15),bg="pink").place(x=15,y=70,width=150,height=30)
        lbl_serial=Label(self.root,text="Serial No.",font=("Times New Roman",15),bg="pink").place(x=15,y=335,width=150,height=30)
        lbl_date=Label(self.root,text="Date",font=("Times New Roman",15),bg="pink").place(x=15,y=110,width=150,height=30)
        lbl_customer=Label(self.root,text="Customer",font=("Times New Roman",15),bg="pink").place(x=15,y=150,width=150,height=30)
        lbl_product=Label(self.root,text="Product",font=("Times New Roman",15),bg="pink").place(x=15,y=375,width=150,height=30)
        lbl_quantity=Label(self.root,text="Quantity",font=("Times New Roman",15),bg="pink").place(x=15,y=415,width=150,height=30)
        lbl_status=Label(self.root,text="Status",font=("Times New Roman",15),bg="pink").place(x=15,y=190,width=150,height=30)

        txt_order=Entry(self.root,textvariable=self.var_order,font=("Arial",15),bg="white").place(x=180,y=70,width=150,height=30)         
        txt_serial=Entry(self.root,textvariable=self.var_serial,font=("Arial",15),bg="white").place(x=180,y=335,width=150,height=30)         
        #txt_date=Entry(self.root,textvariable=self.var_date,font=("Arial",15),bg="white").place(x=180,y=110,width=150,height=30)         
        txt_date = DateEntry(self.root,textvariable=self.var_date,state='readonly', width=12,font=("Arial",15), background='darkblue',foreground='white', borderwidth=2, year=2021).place(x=180,y=110,width=150,height=30)
        cmb_customer=ttk.Combobox(self.root,textvariable=self.var_customer,values=self.customer_list,font=("Arial",15),state='readonly',justify=CENTER).place(x=180,y=150,width=150,height=30)        
        cmb_product=ttk.Combobox(self.root,textvariable=self.var_product,values=self.prod_list,font=("Arial",15),state='readonly',justify=CENTER).place(x=180,y=375,width=150,height=30)
        txt_quantity=Entry(self.root,textvariable=self.var_quantity,font=("Arial",15),bg="white").place(x=180,y=415,width=150,height=30)         
        cmb_status=ttk.Combobox(self.root,textvariable=self.var_status,values=('Pending','Delivered','Cancelled'),font=("Arial",15),state='readonly',justify=CENTER)   
        cmb_status.place(x=180,y=190,width=150,height=30)
        cmb_status.current(0)

        btn_add=Button(self.root,text="Add",command=self.add,font=("arial",12),cursor="hand2").place(x=15,y=230,width=150,height=30)
        btn_update=Button(self.root,text="Update",command=self.update,font=("arial",12),cursor="hand2").place(x=180,y=230,width=150,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("arial",12),cursor="hand2").place(x=15,y=270,width=150,height=30)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("arial",12),cursor="hand2").place(x=180,y=270,width=150,height=30)
        btn_add_detail=Button(self.root,text="Add detail",command=self.add_detail,font=("arial",12),cursor="hand2").place(x=15,y=455,width=150,height=30)
        btn_update_detail=Button(self.root,text="Update detail",command=self.update_detail,font=("arial",12),cursor="hand2").place(x=180,y=455,width=150,height=30)
        btn_delete_detail=Button(self.root,command=self.delete_detail,text="Delete detail",font=("arial",12),cursor="hand2").place(x=15,y=495,width=150,height=30)

#===========TABLE 1=====================================================================================================================

        self.ordertable=ttk.Treeview(self.root,columns=("Order_ID","Order_Date","customer_Name","Total_Amt","Status"))
               
        self.ordertable.place(x=350,y=75,width=650,height=225)
        self.ordertable.heading("Order_ID",text="Order No.")
        self.ordertable.heading("Order_Date",text="Date")
        self.ordertable.heading("customer_Name",text="Customer Name")
        self.ordertable.heading("Total_Amt",text="Total Amount")
        self.ordertable.heading("Status",text="Status")
        self.ordertable["show"]="headings"

        self.ordertable.column("Order_ID",width=80)
        self.ordertable.column("Order_Date",width=80)
        self.ordertable.column("customer_Name",width=80)
        self.ordertable.column("Total_Amt",width=80)
        self.ordertable.column("Status",width=80)
        self.ordertable.bind("<ButtonRelease-1>",self.get_mast_data)

       

#=======TABLE 2======================================================================================================================
        
        self.detailtable=ttk.Treeview(self.root,columns=("Order_ID","Serial_No","Product_Name","Quantity","Rate","Amount"))
        self.detailtable.place(x=350,y=320,width=650,height=213)
        self.detailtable.heading("Order_ID",text="Order No.")
        self.detailtable.heading("Serial_No",text="Serial No.")
        self.detailtable.heading("Product_Name",text="Product Name")
        self.detailtable.heading("Quantity",text="Quantity")
        self.detailtable.heading("Rate",text="Rate")
        self.detailtable.heading("Amount",text="Amount")
        self.detailtable["show"]="headings"

        self.detailtable.column("Order_ID",width=80)
        self.detailtable.column("Serial_No",width=80)
        self.detailtable.column("Product_Name",width=80)
        self.detailtable.column("Quantity",width=80)
        self.detailtable.column("Rate",width=80)
        self.detailtable.column("Amount",width=80)
        self.detailtable.bind("<ButtonRelease-1>",self.get_det_data)
        
        self.show()
        self.show_detail()
        self.fetch_customer_product()

#========================================================================================================================================
    
    def fetch_customer_product(self):
        con=sqlite3.connect(database=r'oms.db')
        cur = con.cursor()
        try:
            cur.execute("Select customer_Name from customer")
            customer=cur.fetchall()
            for i in customer:
                self.customer_list.append(i[0])
            cur.execute("Select product_Name from product")
            prod=cur.fetchall()
            for i in prod:
                self.prod_list.append(i[0])            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def add(self):
        con=sqlite3.connect(database=r'oms.db')
        cur = con.cursor()
        try:
            if self.var_order.get()=="" or self.var_date.get()=="" or self.var_customer.get()=="" or self.var_status.get()=="":
                messagebox.showerror("Error","All fields required",parent=self.root)
            elif self.var_order.get().isnumeric()==False:               
                messagebox.showerror("Error","Order must contain number only",parent=self.root)
            else:
                cur.execute("Select * from order_mast where Order_ID=?",(self.var_order.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","The ID has been assigned, try different ID",parent=self.root)
                else:
                    cur.execute("Insert into order_mast (Order_ID,Order_Date,customer_name,Status) values(?,?,?,?)",(self.var_order.get(),self.var_date.get(),self.var_customer.get(),self.var_status.get()))
                    con.commit()
                    messagebox.showinfo("Success","Added Successfully",parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def update(self):
        con=sqlite3.connect(database=r'oms.db')
        cur = con.cursor()
        cur1= con.cursor()
        try:
            cur1.execute("Select Status from order_mast where Order_ID=?",(self.var_order.get(),))
            row=cur1.fetchone()
            if row[0]!="Pending":
                messagebox.showerror("Error","Order cannot be updated if the order is cancelled or delivered.",parent=self.root)
            else:
                if self.var_order.get()=="":
                    messagebox.showerror("Error","Order ID must be required",parent=self.root)
                elif self.var_order.get().isnumeric()==False:               
                    messagebox.showerror("Error","Order must contain number only",parent=self.root)
                elif self.var_customer.get()=="":
                    messagebox.showerror("Error","Customer Name  must be required",parent=self.root)
                elif self.var_order.get().isnumeric()==False:
                    messagebox.showerror("Error","Order ID must contain numbers only",parent=self.root)
                else:
                    cur.execute("Select * from order_mast where Order_ID=?",(self.var_order.get(),))
                    row=cur.fetchone()
                    if row==None:
                        messagebox.showerror("Error","Invalid ID",parent=self.root)
                    else:
                        cur.execute("Update order_mast set Order_Date=?,customer_Name=?,Status=? where Order_ID=?",(self.var_date.get(),self.var_customer.get(),self.var_status.get(),self.var_order.get(),))
                        con.commit()
                        messagebox.showinfo("Success","Updated Successfully",parent=self.root)
                        self.show()                
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'oms.db')
        cur = con.cursor()
        cur1= con.cursor()
        try:
            cur1.execute("Select Status from order_mast where Order_ID=?",(self.var_order.get(),))
            row=cur1.fetchone()
            if row[0]!="Pending":
                messagebox.showerror("Error","Order cannot be deleted if the order is cancelled or delivered.",parent=self.root)
            else:
                if self.var_order.get()=="":
                    messagebox.showerror("Error","Invalid Order ID",parent=self.root)
                else:
                    cur.execute("Select * from order_mast where Order_ID=?",(self.var_order.get(),))
                    row=cur.fetchone()
                    if row==None:
                        messagebox.showerror("Error","Invalid customer ID",parent=self.root)
                    else:
                        op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                        if op==True:
                            cur.execute("PRAGMA foreign_keys = ON;")
                            cur.execute("delete from order_mast where Order_ID=?",(self.var_order.get(),))
                            con.commit()
                            messagebox.showinfo("Delete","Deleted Successfully",parent=self.root)
                            self.show()
                            self.clear()
        except Exception as ex:
            if str(ex)=="FOREIGN KEY constraint failed":
                messagebox.showerror("Error","Order details exist - cannot delete",parent=self.root)
            else:
                messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.var_order.set("")
        self.var_customer.set("")
        self.var_product.set("")
        self.var_quantity.set("")
        self.var_status.set("")
        self.var_date.set("")
        self.var_serial.set("")
        self.show()

    def add_detail(self):
        con=sqlite3.connect(database=r'oms.db')
        cur = con.cursor()  
        cur1 = con.cursor()
        try:
            cur1.execute("Select Status from order_mast where Order_ID=?",(self.var_order.get(),))
            row=cur1.fetchone()
            if row[0]!="Pending":
                messagebox.showerror("Error","Order cannot be added if the order is cancelled or delivered.",parent=self.root)
            else:
                cur1.execute("Select count(*) from order_det where Order_ID=? and Product_Name=?",(self.var_order.get(),self.var_product.get(),))
                row=cur1.fetchone()
                if row[0]>0:
                    messagebox.showerror("Error","Same product exist in the order. Cannot Add",parent=self.root)
                else:
                    if self.var_order.get()=="" or self.var_serial.get=="" or self.var_product.get()=="" or self.var_quantity.get()=="":
                        messagebox.showerror("Error","All fields required",parent=self.root)
                    elif self.var_serial.get().isnumeric()==False:               
                        messagebox.showerror("Error","Serial Number must contain number only",parent=self.root)
                    elif self.var_quantity.get()<=0:
                        messagebox.showerror("Error","Quantity should be greater than 0",parent=self.root)
                    else:
                        cur.execute("Select * from order_det where Order_ID=? and Serial_No=?",(self.var_order.get(),self.var_serial.get(),))
                        row=cur.fetchone()
                        if row!=None:
                            messagebox.showerror("Error","The ID has been assigned, try different ID",parent=self.root)
                        else:
                            cur1.execute("Select Count(*) from order_mast where Order_ID=?",(self.var_order.get(),))
                            row1=cur1.fetchone()
                            if row1[0]>0:
                                cur1.execute("Select Rate from product where product_Name=? ",(self.var_product.get(),))
                                row1=cur1.fetchone()
                                self.var_rate.set(row1[0])
                                self.var_amount.set(self.var_rate.get()*self.var_quantity.get())
                                cur.execute("Insert into order_det (Order_ID,Serial_No,Product_Name,Quantity,Rate,Amount) values(?,?,?,?,?,?)",(self.var_order.get(),self.var_serial.get(),self.var_product.get(),self.var_quantity.get(),self.var_rate.get(),self.var_amount.get(),))
                                cur1.execute("Update order_mast set Total_Amt=(select sum(amount) from order_det where order_mast.order_id=order_det.order_id )",)
                                con.commit()

                                messagebox.showinfo("Success","Added Successfully",parent=self.root)
                                self.show()
                                self.show_detail()
                                self.clear()
                            else:
                                messagebox.showinfo("Error","Details cannot be added without order",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def update_detail(self):
        con=sqlite3.connect(database=r'oms.db')
        cur = con.cursor()
        cur1 = con.cursor()
        try:
            cur1.execute("Select Status from order_mast where Order_ID=?",(self.var_order.get(),))
            row=cur1.fetchone()
            if row[0]!="Pending":
                messagebox.showerror("Error","Order cannot be updated if the order is cancelled or delivered.",parent=self.root)
            else:
                if self.var_order.get()=="":
                    messagebox.showerror("Error","Order ID must be required",parent=self.root)
                if self.var_serial.get()=="":
                    messagebox.showerror("Error","Serial No. must be required",parent=self.root)
                if self.var_quantity.get()<=0:
                    messagebox.showerror("Error","Quantity should be greater than 0",parent=self.root)
                else:
                    cur.execute("Select * from order_det where Order_ID=?",(self.var_order.get(),))
                    row=cur.fetchone()
                    if row==None:
                        messagebox.showerror("Error","Invalid ID",parent=self.root)
                    else:
                        cur1.execute("Select Rate from product where product_Name=? ",(self.var_product.get(),))
                        row1=cur1.fetchone()
                        self.var_rate.set(row1[0])
                        self.var_amount.set(self.var_rate.get()*self.var_quantity.get())
                        cur.execute("Update order_det set Product_Name=?,Quantity=?,Rate=?,Amount=? where Order_ID=? and Serial_No=? ",(self.var_product.get(),self.var_quantity.get(),self.var_rate.get(),self.var_amount.get(),self.var_order.get(),self.var_serial.get(),))
                        cur1.execute("Update order_mast set Total_Amt=(select sum(amount) from order_det where order_mast.order_id=order_det.order_id )",)
                        con.commit()
                        messagebox.showinfo("Success","Updated Successfully",parent=self.root)
                        self.show()
                        self.show_detail()
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def delete_detail(self):
        con=sqlite3.connect(database=r'oms.db')
        cur = con.cursor()
        cur1 = con.cursor()
        try:
            cur1.execute("Select Status from order_mast where Order_ID=?",(self.var_order.get(),))
            row=cur1.fetchone()
            if row[0]!="Pending":
                messagebox.showerror("Error","Order cannot be deleted if the order is cancelled or delivered.",parent=self.root)
            else:
                if self.var_order.get()=="":
                    messagebox.showerror("Error","Invalid Order ID",parent=self.root)
                if self.var_serial.get()=="":
                    messagebox.showerror("Error","Invalid Serial No.",parent=self.root)
                else:
                    cur1.execute("Select Rate from product where product_Name=? ",(self.var_product.get(),))
                    row1=cur1.fetchone()
                    self.var_rate.set(row1[0])
                    self.var_amount.set(self.var_rate.get()*self.var_quantity.get())
                    cur.execute("Select * from order_det where Order_ID=?",(self.var_order.get(),))
                    row=cur.fetchone()
                    if row==None:
                        messagebox.showerror("Error","Invalid customer ID",parent=self.root)
                    else:
                        op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                        if op==True:

                            cur.execute("delete from order_det where Serial_No=?",(self.var_serial.get(),))
                            cur1.execute("Update order_mast set Total_Amt=(select sum(amount) from order_det where order_mast.order_id=order_det.order_id )",)
                            con.commit()
                            messagebox.showinfo("Delete","Deleted Successfully",parent=self.root)
                            self.show()
                            self.show_detail()
                            self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)
    
    def show(self):
        con=sqlite3.connect(database=r'oms.db')
        cur=con.cursor()
        try:
            cur.execute("select order_mast.Order_ID,order_mast.Order_Date,customer.customer_Name,order_mast.Total_Amt,order_mast.Status from order_mast , customer WHERE order_mast.customer_name=customer.customer_Name")
            rows=cur.fetchall()
            self.ordertable.delete(*self.ordertable.get_children())
            for row in rows:
                self.ordertable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def show_detail(self):
        con=sqlite3.connect(database=r'oms.db')
        cur=con.cursor()
        try:
            cur.execute("select order_det.Order_ID,order_det.Serial_No,product.product_Name,order_det.Quantity,order_det.Rate,order_det.Amount from order_det , product WHERE order_det.Product_Name=product.product_Name and order_det.order_id = ? order by order_det.order_id,order_det.Serial_No   ",(self.var_order.get(),))
            rows=cur.fetchall()
            self.detailtable.delete(*self.detailtable.get_children())
            for row in rows:
                self.detailtable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def get_mast_data(self,ev):
        f=self.ordertable.focus()
        content=(self.ordertable.item(f))
        row=content['values']
        self.var_order.set(row[0])
        self.var_date.set(row[1])
        self.var_customer.set(row[2])
        self.var_total.set(row[3])
        self.var_status.set(row[4])
        self.show_detail()
         
    def get_det_data(self,ev):
        g=self.detailtable.focus()
        content=(self.detailtable.item(g))
        row=content['values']
        self.var_order.set(row[0])
        self.var_serial.set(row[1])
        self.var_product.set(row[2])
        self.var_quantity.set(row[3])
        self.var_rate.set(row[4])
        self.var_amount.set(row[5])

if __name__=="__main__":
    root=Tk()
    obj=order_class(root)
    root.mainloop()