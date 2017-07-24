import cx_Oracle
import runpy

con = cx_Oracle.connect("BANK/12345@XE")
cur = con.cursor()
#class for cutomer Map#######################
class Customer:
    #customer table#########################
    def signUp(self,name,gender,address,city,state,pincode,password):
        cur.execute('INSERT INTO CUSTOMER values(crno.nextval,:1,:2,:3,:4,:5,:6,:7)',(name,gender,address,city,state,pincode,password))
        con.commit()
        a = cur.execute('Select crno.currval from dual').fetchall()
        print("CUSTOMER ID : ",int(a[0][0]))

#datails of user####################################
try:
    name = input("NAME :")
    gender= input("GENDER M or F:")
    address= input("ADRESS :")
    pincode=int(input("PIN CODE :"))
    city=input("CITY :")
    state=input("STATE :")
    password = input("password :")
    #object of class customer###########################
    user = Customer()
    user.signUp(name,gender,address,city,state,pincode,password)
    print("Sucessfully Signed Up")
    input("print any key to continue : ")
    runpy.run_path("menu.py")
except:
    print("Somethin went wrong,Try again ")

