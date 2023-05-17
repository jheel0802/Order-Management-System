from tkinter import*
from tkinter import ttk,messagebox
from Menu_Screen import OMS

class login:
    def __init__(self,root):
        self.root = root
        self.root.geometry("500x300+500+200")
        self.root.title("Order Management System")
        self.root.config (bg="white")
        self.root.focus_force()

        #==========title================

        self.var_login=StringVar()
        self.var_password=StringVar()

        title=Label(self.root,text="Login Screen",font=("arial",30,"bold")).place(x=0,y=0,relwidth=1,height=50)
        lbl_username=Label(self.root,text="Username",font=("Times New Roman",15),bg="pink").place(x=10,y=70,width=190,height=30)
        lbl_password=Label(self.root,text="Password",font=("Times New Roman",15),bg="pink").place(x=10,y=110,width=190,height=30)
        txt_username=Entry(self.root,textvariable=self.var_login,font=("Times New Roman",15),bg="white").place(x=210,y=70,width=190,height=30)
        txt_password=Entry(self.root,textvariable=self.var_password,font=("Times New Roman",15),bg="white").place(x=210,y=110,width=190,height=30)
        btn_add=Button(self.root,text="Add",font=("arial",12),cursor="hand2").place(x=10,y=150,width=190,height=30)

        def login_button():
            if self.var_login=='admin' and self.var_password=='P@ssw0rd':
                self.new_win=Toplevel(self.root)
                self.new_obj=OMS(self.new_win)
                self.root.destroy()
            #else:




if __name__=="__main__":
    root=Tk()
    obj=login(root)
    root.mainloop()