import sqlite3
def create_db():
    con = sqlite3.connect(database=r'oms.db')
    cur=con.cursor()

#    cur.execute("Drop Table customer")
#    cur.execute("Drop Table product")
#    cur.execute("Drop Table order_det")
#    cur.execute("Drop Table order_mast")
   
    cur.execute("CREATE TABLE IF NOT EXISTS customer(customer_ID INTEGER PRIMARY KEY AUTOINCREMENT,customer_Name text NOT NULL UNIQUE,GST text NOT NULL UNIQUE,Phone text,Email text,Address text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product(product_ID INTEGER PRIMARY KEY AUTOINCREMENT,product_Name text NOT NULL UNIQUE,Rate REAL)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS order_mast(Order_ID INTEGER PRIMARY KEY AUTOINCREMENT,Order_Date text,customer_name text references customer(customer_Name)  ON DELETE RESTRICT,Total_Amt REAL,Status text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS order_det (Order_ID INTEGER  references order_mast(Order_ID) ,Serial_No INTEGER,Product_Name text references product(product_Name) ,Quantity INTEGER,Rate REAL,Amount REAL,PRIMARY KEY(Order_ID,Serial_No))")
    con.commit()

create_db()