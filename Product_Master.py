from tkinter import*
from tkinter import ttk,messagebox
import sqlite3

class product_class:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1020x540+240+105")
        self.root.title("Product Master")
        self.root.config (bg="white")
        self.root.focus_force()
#===============================================================================================================================================
        self.var_product_id=StringVar()
        self.var_product_Name=StringVar()
        self.var_rate=StringVar()
#=================================================================================================================================================
        title=Label(self.root,text="Product Master",font=("arial",30,"bold")).place(x=0,y=0,relwidth=1,height=60)   

        lbl_product_id=Label(self.root,text="Product ID",font=("Times New Roman",15),bg="pink").place(x=10,y=70,width=150,height=30) 
        lbl_product_Name=Label(self.root,text="Product Name",font=("Times New Roman",15),bg="pink").place(x=10,y=120,width=150,height=30)
        lbl_rate=Label(self.root,text="Rate",font=("Times New Roman",15),bg="pink").place(x=10,y=170,width=150,height=30)
        
        txt_product_id=Entry(self.root,textvariable=self.var_product_id,font=("Times New Roman",15),bg="white").place(x=170,y=70,width=150,height=30) 
        txt_product_name=Entry(self.root,textvariable=self.var_product_Name,font=("Times New Roman",15),bg="white").place(x=170,y=120,width=150,height=30)
        txt_rate=Entry(self.root,textvariable=self.var_rate,font=("Times New Roman",15),bg="white").place(x=170,y=170,width=150,height=30)
       
        btn_add=Button(self.root,text="Add",command=self.add,font=("arial",15),cursor="hand2").place(x=20,y=455,width=140,height=30)
        btn_update=Button(self.root,text="Update",command=self.update,font=("arial",15),cursor="hand2").place(x=170,y=455,width=140,height=30)
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("arial",15),cursor="hand2").place(x=20,y=495,width=140,height=30)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("arial",15),cursor="hand2").place(x=170,y=495,width=140,height=30)
#=====================Tree View===============================================================================================================
        self.producttable=ttk.Treeview(self.root,columns=("product_ID","product_Name","Rate"))        
        self.producttable.place(x=330,y=70,width=675,height=460)

        self.producttable.heading("product_ID",text="Product ID")
        self.producttable.heading("product_Name",text="Name")
        self.producttable.heading("Rate",text="Rate")
        self.producttable["show"]="headings"

        self.producttable.column("product_ID",width=80)
        self.producttable.column("product_Name",width=80)
        self.producttable.column("Rate",width=80)
        self.producttable.bind("<ButtonRelease-1>",self.get_data)

        self.show()

#============================================================================================================================================

    def add(self):
        con=sqlite3.connect(database=r'oms.db')
        cur = con.cursor()
        try:
            if self.var_product_id.get()=="" or self.var_product_Name.get()=="" or self.var_product_id.get()=="" or self.var_rate.get()=="":
                messagebox.showerror("Error","All fields required required",parent=self.root)
            elif self.var_rate.get().isnumeric()==False:               
               messagebox.showerror("Error","Rate must contain numbers only",parent=self.root)
            elif int(self.var_rate.get())<=0:
                messagebox.showerror("Error","Rate should be greater than 0",parent=self.root)
            elif self.var_product_id.get().isnumeric()==False:
                messagebox.showerror("Error","Product ID must contain numbers only",parent=self.root)
            else:
                cur.execute("Select * from product where product_ID=?",(self.var_product_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","The ID has been assigned, try different ID",parent=self.root)
                else:
                    cur.execute("Insert into product (product_ID,product_Name,Rate) values(?,Upper(?),?)",(self.var_product_id.get(),self.var_product_Name.get(),self.var_rate.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Added Successfully",parent=self.root)
                    self.show()
                    self.clear()
        except Exception as ex:
            if str(ex)=="UNIQUE constraint failed: product.product_Name":
                messagebox.showerror("Error","Product Name already exists",parent=self.root)
            else:
                messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def update(self):
        con=sqlite3.connect(database=r'oms.db')
        cur = con.cursor()
        try:
            if self.var_product_id.get()=="":
                messagebox.showerror("Error","Product ID must be required",parent=self.root)
            elif int(self.var_rate.get())<=0:
                messagebox.showerror("Error","Rate should be greater than 0",parent=self.root)
            elif self.var_rate.get().isnumeric()==False:               
                messagebox.showerror("Error","Rate must contain numbers only",parent=self.root)
            elif self.var_product_id.get().isnumeric()==False:
                messagebox.showerror("Error","Product ID must contain numbers only",parent=self.root)
            else:
                cur.execute("Select * from product where product_ID=?",(self.var_product_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid ID",parent=self.root)
                else:
                    cur.execute("Update product set product_Name=upper(?),Rate=? where product_ID=?",(self.var_product_Name.get(),self.var_rate.get(),self.var_product_id.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Updated Successfully",parent=self.root)
                    self.show()
                    self.clear()
                    
        except Exception as ex:
            if str(ex)=="UNIQUE constraint failed: product.product_Name":
                messagebox.showerror("Error","Product Name already exists",parent=self.root)
            else:
                messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def delete(self):
        con=sqlite3.connect(database=r'oms.db')
        cur = con.cursor()
        cur1 = con.cursor()
        try:
            cur1.execute("Select count(*) from order_det where product_Name=?",(self.var_product_Name.get(),))
            row1 = cur1.fetchone()
            if row1[0]>0:
                messagebox.showerror("Error","Product is in orders - Cannot delete")
            else:
                if self.var_product_id.get()=="":
                    messagebox.showerror("Error","Invalid Product ID",parent=self.root)
                else:
                    cur.execute("Select * from product where product_ID=?",(self.var_product_id.get(),))
                    row=cur.fetchone()
                    if row==None:
                        messagebox.showerror("Error","Invalid Product ID",parent=self.root)
                    else:
                        op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                        if op==True:
                            cur.execute("delete from product where product_ID=?",(self.var_product_id.get(),))
                            con.commit()
                            messagebox.showinfo("Delete","Deleted Successfully",parent=self.root)
                            self.show()
                            self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def clear(self):
        self.var_product_id.set("")
        self.var_product_Name.set("")
        self.var_rate.set("")
        self.show()

    def show(self):
        con=sqlite3.connect(database=r'oms.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.producttable.delete(*self.producttable.get_children())
            for row in rows:
                self.producttable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.producttable.focus()
        content=(self.producttable.item(f))
        row=content['values']
        #print(row)
        self.var_product_id.set(row[0])
        self.var_product_Name.set(row[1])
        self.var_rate.set(row[2])


if __name__=="__main__":
    root=Tk()
    obj=product_class(root)
    root.mainloop()