import cx_Oracle

class Admin:
    loggedIn = False

    def logIn(self):
        self.loggedIn=True

    def closed(self):
        is_active='N'
        cur.execute('select c_id,account_no,type FROM account WHERE is_active = :1',(is_active))
        a = cur.fetchall()
        for row in a:
            print("Customer ID:",row[0],", account_no:",row[1],",type:",row[2])

    def fdreport(self):
        customer_id = int(input("customer id"))
        cur.execute('select account_no,duration,balance FROM fixed WHERE C_ID=:1',(customer_id,))
        a=cur.fetchall()
        if a:
            for row in a:
                print("account no:", row[0], ", deposite duration :", row[1], ",balance:", row[2])
        else:
            print("Wrong Customer ID")

    def visFd(self):
        customer_id = int(input("customer id"))
        cur.execute('select account_no,duration,balance,c_id FROM fixed WHERE balance>(SELECT SUM(balance) FROM fixed where c_id = :1)', (customer_id,))
        a = cur.fetchall()
        if a:
            for row in a:
                print("account no:", row[0], ", deposite duration :", row[1], ",balance:", row[2],", Customer Id",row[3])
        else:
            print("Wrong Customer ID")

    def wrtFd(self):
        amount = int(input("amount :"))
        if amount<0:
            print("negative amount")
        elif amount%10 != 0:
            print("Enter amount in multiple of 100")
        else:
            cur.execute('SELECT c_id,balance from fixed WHERE balance>:1',(amount,))
            a=cur.fetchall()
            for row in a:
                cur.execute('SELECT c_id, full_name from customer WHERE c_id =:1', (row[0],))
                b = cur.fetchall()
                for row1 in b:
                    print("customer id :",row1[0],", Name :",row1[1],",Amount :",row[1])

    def loanreport(self):
        customer_id = int(input("customer id"))
        cur.execute('select c_id,loan_id,amount,duration FROM loan WHERE c_id = :1',(customer_id,))
        a = cur.fetchall()
        if a:
            for row in a:
                print("customer id:", row[0], ", loan id :", row[1], ",Amount :", row[2], ", Duration", row[3])
            if len(a) == 0:
                print(" N.A.")
        else:
            print("Wrong Customer ID")



    def visLoan(self):
        customer_id = int(input("customer id"))
        cur.execute('select c_id,loan_id,amount,duration FROM loan WHERE amount>(SELECT SUM(amount) FROM loan where c_id = :1)',(customer_id,))
        a = cur.fetchall()
        if a:
            for row in a:
                print("customer Id:", row[0], ", loan Id :", row[1], ",Amount:", row[2], ", Duration", row[3])
            if len(a) == 0:
                print(" N.A.")
        else:
            print("Wrong Customer ID")

    def wrtLoan(self):
        amount = int(input("amount :"))
        if amount < 0:
            print("negative amount")
        elif amount % 10 != 0:
            print("Enter amount in multiple of 100")
        else:
            cur.execute('SELECT c_id,amount from loan WHERE amount>:1', (amount,))
            a = cur.fetchall()
            for row in a:
                cur.execute('SELECT c_id, full_name from customer WHERE c_id =:1', (row[0],))
                b = cur.fetchall()
                for row1 in b:
                    print("customer id :", row1[0], ", Name :", row1[1], ",Amount :", row[1])
            if len(a) ==0 :
                print("N.A.")


    def loanFd(self):
        a = cur.execute('SELECT * FROM Customer').fetchall()
        for row in a:
            l=cur.execute('SELECT sum(amount) from loan where c_id=:1',(row[0],)).fetchall()
            l1=l[0][0]
            f=cur.execute('SELECT sum(balance) from fixed where c_id=:1',(row[0],)).fetchall()
            f1=f[0][0]
            if l1>f1:
                print(row)
        if len(a)==0:
            print(" N.A.")

    def yetloan(self):
        a = cur.execute('SELECT * FROM Customer').fetchall()
        for i in a:
            f = cur.execute('SELECT * FROM fixed WHERE c_id = :1', (i[0],))
            if f:
                continue
            else:
                print(i)
        if len(a)==0:
            print("N.A.")

    def yetaccount(self):
        a = cur.execute('SELECT * FROM customer').fetchall()
        for i in a:
            f = cur.execute('SELECT * FROM fixed WHERE c_id = :1', (i[0],))
            if f:
                continue
            else:
                print(i)

        if len(a) == 0:
            print("N.A.")

    def norfdloan(self):
        a = cur.execute('SELECT * FROM Customer').fetchall()
        for i in a:
            f = cur.execute('SELECT * FROM fixed WHERE c_id = :1', (i[0],))
            g = cur.execute('SELECT * FROM loan WHERE c_id = :1', (i[0],))
            if f or g:
                continue
            else:
                print(i)

        if len(a) == 0:
            print("N.A.")

    def logout(self):
        self.loggedIn = False

con = cx_Oracle.connect("BANK/12345@XE")
cur = con.cursor()
admin=input("Admin Id ")
adminId="admin"
password = input("password ")
adminpass = "graphicera"
adminlog = Admin()

if admin == adminId and password == adminpass:
    adminlog.logIn()
else:
    print("wrong Id or password")
try:
    while adminlog.loggedIn is True:
        if adminlog.loggedIn is True:
            print("1. closed Account history ")
            print("2. FD report of Customer")
            print("3. FD report of customer vis-a-vis another customer ")
            print("4. FD report w.r.t a particular FD amount")
            print("5. Loan report of customer")
            print("6. Loan report of customer vis-a-vis another customer")
            print("7. loan report w.r.t a particular loan amount")
            print("8. loan-fd report of customer")
            print("9. Report of customers who are yet to avail loan")
            print("10. Report of customers who are yet to open FD account")
            print("11. Report who neither have fd acoount or nor loan")
            print("0. quit")
            choice = int(input())
            if  choice==1:
               adminlog.closed()
            elif choice==2:
                adminlog.fdreport()
            elif choice==3:
               adminlog.visFd()
            elif choice==4:
               adminlog.wrtFd()
            elif choice==5:
               adminlog.loanreport()
            elif choice==6:
               adminlog.visLoan()
            elif choice==7 :
               adminlog.wrtLoan()
            elif choice==8 :
                adminlog.loanFd()
            elif choice==9 :
               adminlog.yetloan()
            elif choice==10 :
                adminlog.yetaccount()
            elif choice==11 :
                adminlog.norfdloan()
            elif choice==0:
                admin.logout()
            else :
                print("Wrong choice")
        input("Input any key to continue : ")
except:
    print("Something went wrong,try again")