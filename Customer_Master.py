from tkinter import*
from tkinter import ttk,messagebox
import sqlite3

class customer_class:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1020x540+240+105")
        self.root.title("Customer Master")
        self.root.config (bg="white")
        self.root.focus_force()
#=========================================Variables================================================
        self.var_customer_id=StringVar()
        self.var_customer_Name=StringVar()
        self.var_address=StringVar()
        self.var_gst_no=StringVar()
        self.var_email=StringVar()
        self.var_phone=StringVar()
#==================================================================================================
        title=Label(self.root,text="Customer Master",font=("arial",30,"bold")).place(x=0,y=0,relwidth=1,height=60)   

        lbl_customer_id=Label(self.root,text="Customer ID",font=("Times New Roman",15),bg="pink").place(x=10,y=70,width=150,height=30) 
        lbl_customer_Name=Label(self.root,text="Customer Name",font=("Times New Roman",15),bg="pink").place(x=10,y=120,width=150,height=30)
        lbl_gst_no=Label(self.root,text="GST No.",font=("Times New Roman",15),bg="pink").place(x=10,y=170,width=150,height=30)
        lbl_phone=Label(self.root,text="Phone",font=("Times New Roman",15),bg="pink").place(x=10,y=220,width=150,height=30)
        lbl_email=Label(self.root,text="Email",font=("Times New Roman",15),bg="pink").place(x=10,y=270,width=150,height=30)
        lbl_address=Label(self.root,text="Address",font=("Times New Roman",15),bg="pink").place(x=10,y=320,width=150,height=30)
        

        txt_customer_id=Entry(self.root,textvariable=self.var_customer_id,font=("Times New Roman",15),bg="white").place(x=170,y=70,width=150,height=30) 
        txt_customer_name=Entry(self.root,textvariable=self.var_customer_Name,font=("Times New Roman",15),bg="white").place(x=170,y=120,width=150,height=30)
        txt_gst_no=Entry(self.root,textvariable=self.var_gst_no,font=("Times New Roman",15),bg="white").place(x=170,y=170,width=150,height=30)
        txt_phone=Entry(self.root,textvariable=self.var_phone,font=("Times New Roman",15),bg="white").place(x=170,y=220,width=150,height=30)
        txt_email=Entry(self.root,textvariable=self.var_email,font=("Times New Roman",15),bg="white").place(x=170,y=270,width=150,height=30)
        self.txt_address=Entry(self.root,textvariable=self.var_address,font=("Times New Roman",15),bg="white").place(x=170,y=320,width=150,height=30)

        btn_add=Button(self.root,text="Add",command=self.add,font=("arial",15),cursor="hand2").place(x=20,y=455,width=140,height=30)
        btn_update=Button(self.root,text="Update",command=self.update,font=("arial",15),cursor="hand2").place(x=170,y=455,width=140,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("arial",15),cursor="hand2").place(x=20,y=495,width=140,height=30)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("arial",15),cursor="hand2").place(x=170,y=495,width=140,height=30)
#===============Tree View============================================================================================
        self.customertable=ttk.Treeview(self.root,columns=("customer_ID","customer_Name","GST","Phone","Email","Address"))
               
        self.customertable.place(x=330,y=70,width=675,height=460)
        self.customertable.heading("customer_ID",text="Customer ID")
        self.customertable.heading("customer_Name",text="Company Name")
        self.customertable.heading("GST",text="GST no.")
        self.customertable.heading("Phone",text="Phone")
        self.customertable.heading("Email",text="Email")
        self.customertable.heading("Address",text="Address")
        self.customertable["show"]="headings"

        self.customertable.column("customer_ID",width=80)
        self.customertable.column("customer_Name",width=80)
        self.customertable.column("GST",width=80)
        self.customertable.column("Phone",width=80)
        self.customertable.column("Email",width=80)
        self.customertable.column("Address",width=80)
        self.customertable.bind("<ButtonRelease-1>",self.get_data)

        self.show()

#=========================================================================
    def add(self):
        con=sqlite3.connect(database=r'oms.db')
        cur = con.cursor()
        try:
            if self.var_customer_id.get()=="" or self.var_address.get()=="" or self.var_email.get()=="" or self.var_gst_no.get()=="" or self.var_customer_Name.get()=="" or self.var_phone.get()=="":
                messagebox.showerror("Error","All fields required",parent=self.root)
            elif self.var_phone.get().isnumeric()==False:               
                messagebox.showerror("Error","Phone must contain numbers only",parent=self.root)
            elif (len(self.var_gst_no.get())==15) is False:
                messagebox.showerror("Error","GST must contain 15 characters.",parent=self.root)
            elif (len(self.var_phone.get())==10) is False:
                messagebox.showerror("Error","Phone must contain 10 characters.",parent=self.root)
            elif self.var_customer_id.get().isnumeric()==False:
                messagebox.showerror("Error","Customer ID must contain numbers only",parent=self.root)
            else:
                cur.execute("Select * from customer where customer_ID=?",(self.var_customer_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","The ID has been assigned, try different ID",parent=self.root)
                else:
                    cur.execute("Insert into customer (customer_ID,customer_Name,GST,Phone,Email,Address) values(?,upper(?),?,?,?,?)",(self.var_customer_id.get(),self.var_customer_Name.get(),self.var_gst_no.get(),self.var_phone.get(),self.var_email.get(),self.var_address.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Added Successfully",parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            if str(ex)=="UNIQUE constraint failed: customer.customer_Name":
                messagebox.showerror("Error","Customer Name already exists",parent=self.root)
            elif str(ex)=="UNIQUE constraint failed: customer.GST":
                messagebox.showerror("Error","GST number already exists",parent=self.root)
            else:
                messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def update(self):
        con=sqlite3.connect(database=r'oms.db')
        cur = con.cursor()
        try:
            if self.var_customer_id.get()=="":
                messagebox.showerror("Error","customer ID must be required",parent=self.root)
            elif self.var_phone.get().isdigit()==False:               
                messagebox.showerror("Error","Phone must contain numbers only",parent=self.root)
            elif (len(self.var_gst_no.get())==15) is False:
                messagebox.showerror("Error","GST must contain 15 characters.",parent=self.root)
            elif (len(self.var_phone.get())==10) is False:
                messagebox.showerror("Error","Phone must contain 10 characters.",parent=self.root)
            elif self.var_customer_id.get().isnumeric()==False:
                messagebox.showerror("Error","Customer ID must contain numbers only",parent=self.root)
            else:
                cur.execute("Select * from customer where customer_ID=?",(self.var_customer_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid ID",parent=self.root)
                else:
                    cur.execute("Update customer set customer_Name=upper(?),GST=?,Phone=?,Email=?,Address=? where customer_ID=?",(self.var_customer_Name.get(),self.var_gst_no.get(),self.var_phone.get(),self.var_email.get(),self.var_address.get(),self.var_customer_id.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Updated Successfully",parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            if str(ex)=="UNIQUE constraint failed: customer.customer_Name":
                messagebox.showerror("Error","Customer Name already exists",parent=self.root)
            elif str(ex)=="UNIQUE constraint failed: customer.GST":
                messagebox.showerror("Error","GST number already exists",parent=self.root)
            else:
                messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'oms.db')
        cur = con.cursor()
        cur1= con.cursor()
        try:
            cur1.execute("Select count(*) from order_mast where customer_Name=?",(self.var_customer_Name.get(),))
            row1 = cur1.fetchone()
            if row1[0]>0:
                messagebox.showerror("Error","Customer has orders - Cannot delete")
            else:
                if self.var_customer_id.get()=="":
                    messagebox.showerror("Error","Invalid customer ID",parent=self.root)
                else:
                    cur.execute("Select * from customer where customer_ID=?",(self.var_customer_id.get(),))
                    row=cur.fetchone()
                    if row==None:
                        messagebox.showerror("Error","Invalid customer ID",parent=self.root)
                    else:
                        op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                        if op==True:
                            cur.execute("delete from customer where customer_ID=?",(self.var_customer_id.get(),))
                            con.commit()
                            messagebox.showinfo("Delete","Deleted Successfully",parent=self.root)
                            self.show()
                            self.clear()
        except Exception as ex:

            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.var_customer_id.set("")
        self.var_customer_Name.set("")
        self.var_gst_no.set("")
        self.var_phone.set("")
        self.var_email.set("")
        self.var_address.set("")
        self.show()

    def show(self):
        con=sqlite3.connect(database=r'oms.db')
        cur=con.cursor()
        try:
            cur.execute("select * from customer")
            rows=cur.fetchall()
            self.customertable.delete(*self.customertable.get_children())
            for row in rows:
                self.customertable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.customertable.focus()
        content=(self.customertable.item(f))
        row=content['values']
        #print(row)
        self.var_customer_id.set(row[0])
        self.var_customer_Name.set(row[1])
        self.var_gst_no.set(row[2])
        self.var_phone.set(row[3])
        self.var_email.set(row[4])
        self.var_address.set(row[5])

if __name__=="__main__":
    root=Tk()
    obj=customer_class(root)
    root.mainloop()