from tkinter import*
from tkinter import ttk,messagebox
from Customer_Master import customer_class
from Product_Master import product_class
from Orders import order_class

class OMS:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Order Management System")
        self.root.config (bg="white")
        #==========title================
        title=Label(self.root,text="Order Management System",font=("arial",35,"bold")).place(x=0,y=0,relwidth=1,height=70)
        #==========Menu btns============
        LeftMenu = Frame(self.root,bd=2,relief=RIDGE)
        LeftMenu.place(x=10,y=80,width=230,height=570)
        lbl_menu=Label(LeftMenu,text="Menu",font=("arial",30,"bold"),bg="light blue").pack(side=TOP,fill=X)
        btn_customer=Button(LeftMenu,text="Customer Master",command=self.customer,font=("arial",20),cursor="hand2").pack(side=TOP,fill=X)
        btn_product=Button(LeftMenu,text="Product Master",command=self.product,font=("arial",20),cursor="hand2").pack(side=TOP,fill=X)
        btn_order=Button(LeftMenu,text="Orders",command=self.order,font=("arial",20),cursor="hand2").pack(side=TOP,fill=X)
        #==========exit btn===========
        btn_exit=Button(LeftMenu,text="Exit",font=("arial",20,"bold"),cursor="hand2",command=root.destroy).pack(side=BOTTOM,fill=X)
        
    def customer(self):
        self.customer_win=Toplevel(self.root)
        self.customer_obj=customer_class(self.customer_win)

    def product(self):
        self.product_win=Toplevel(self.root)
        self.product_obj=product_class(self.product_win)

    def order(self):
        self.order_win=Toplevel(self.root)
        self.order_obj=order_class(self.order_win)


if __name__=="__main__":
    root=Tk()
    obj=OMS(root)
    root.mainloop()
