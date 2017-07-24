import cx_Oracle
from datetime import datetime

class LoggedIn:

    loggedIn = False

    def logIn(self):
        self.loggedIn=True

    def changeAdress(self,customerId):
        address = input("new Adress : ")
        cur.execute('UPDATE customer SET address = :1 WHERE c_id = :2',(address, customerId))
        con.commit()
        print("address changed")

    def saving(self,customerId):
        ac_type='SA'
        is_active = 'y'
        password = input("password")
        amount = int(input("amount"))
        if amount<0:
            print("Invalid Amount")
        else:
            cur.execute('INSERT INTO ACCOUNT values(:1,ACNO.nextval,:2,:3,:4,0,sysdate,:5,NULL)', (customerId,password,ac_type,amount,is_active))
            con.commit()
            print("Saving account Created")

    def current(self,customerId):
        ac_type = 'CA'
        is_active = 'y'
        password = input("password")
        amount = int(input("amount"))
        if amount<5000:
            print("Amount is less than 5000, can not create account")
        else:
            cur.execute('INSERT INTO ACCOUNT values(:1,ACNO.nextval,:2,:3,:4,0,sysdate,:5,NULL)',(customerId, password, ac_type, amount, is_active))
            con.commit()
            print("Current Account Created")

    def fixed(self,cutomerId):
        password = input("password")
        amount = int(input("amount"))
        duration = int(input("duration in months"))
        if amount < 1000:
            print("Amount is less than 1000, can not create account")
        elif duration <12:
            print("Duration is than 12 months, can not create account")
        else:
            cur.execute('INSERT INTO fixed values(:1,ACNO.nextval,:2,sysdate,:3,:4)', (customerId, duration, password,amount))
            con.commit()
            print("fixed Desposite Created")

    def moneyDeposite(self):
        ac_no = int(input("account_no"))
        type = 'd'
        cur.execute('SELECT balance FROM Account where account_no = :1', (ac_no,))
        a = cur.fetchall()
        if a:
            amount = int(input("amount :"))
            final_amount = amount+a[0][0]
            cur.execute('UPDATE account SET balance = :1 WHERE account_no = :2', (final_amount, ac_no))
            cur.execute('INSERT INTO transaction VALUES (trno.nextval,:1,:2,sysdate,:3,:4)',(ac_no,type,final_amount,amount))
            con.commit()
            print("Sucessfully deposited")
        else:
            print("Invalid Account No",ac_no)

    def printStatement(self):
        ac_no = int(input("account no"))
        cur.execute('SELECT balance FROM Account where account_no = :1', (ac_no,))
        a =cur.fetchall()
        if a:
            date = input('Enter the date (MM-DD-YYYY) : ')
            date = date.split('-')
            date = datetime(int(date[2]), int(date[0]), int(date[1]))
            a = cur.execute('SELECT * FROM transaction WHERE account_no = :1 and transaction_time > :2',(ac_no, date)).fetchall()
            for row in a:
                for coloumn in row:
                    print(coloumn)
                print("")
        else:
            print("Invalid account no",ac_no)

    def moneyWithdrwal(self):
        ac_no=int(input("account_no"))
        type = 'w'
        cur.execute('SELECT balance FROM Account where account_no = :1', (ac_no,))
        a = cur.fetchall()
        if a :
            amount = int(input("amount :"))
            if a[0][0] < amount:
                print("less amount")
            else:
                final_amount = a[0][0] - amount
                cur.execute('UPDATE account SET balance = :1 WHERE account_no = :2', (final_amount, ac_no))
                cur.execute('INSERT INTO transaction VALUES (trno.nextval,:1,:2,sysdate,:3,:4)',(ac_no, type, final_amount, amount))
                con.commit()
                print("Sucessfully widrawal")
        else :
            print("Invalid account no",ac_no)

    def transferMoney(self):
        ac_no = int(input("account_no"))
        ac_no1 = int(input("account no to tranfer :"))
        type = 'w'
        cur.execute('SELECT balance FROM Account where account_no = :1', (ac_no,))
        a = cur.fetchall()
        check = True
        amount = int(input("amount :"))
        if a:
            amount = int(input("amount :"))
            if a[0][0] < amount:
                print("less amount, can't perform operation")
                check = False
            else:
                final_amount = a[0][0] - amount
                cur.execute('UPDATE account SET balance = :1 WHERE account_no = :2', (final_amount, ac_no))
                cur.execute('INSERT INTO transaction VALUES (trno.nextval,:1,:2,sysdate,:3,:4)',(ac_no, type, final_amount, amount))
                con.commit()
        else:
            print("Wrong Account No",ac_no)
            check=False

        type = 'd'
        if check == True:
            cur.execute('SELECT balance FROM Account where account_no = :1', (ac_no1,))
            a = cur.fetchall()
            if a:
                final_amount = amount + a[0][0]
                cur.execute('UPDATE account SET balance = :1 WHERE account_no = :2', (final_amount, ac_no1))
                cur.execute('INSERT INTO transaction VALUES (trno.nextval,:1,:2,sysdate,:3,:4)',(ac_no1, type, final_amount, amount))
                con.commit()
                print("transaction Successful")
            else:
                print("Wrong Account No",ac_no1)

    def accountClouser(self):
        ac_no = int(input("account_no"))
        is_active='N'
        cur.execute('SELECT balance FROM account WHERE account_no = :1', (ac_no,))
        a = cur.fetchall()
        if a:
            cur.execute('UPDATE account SET CLOSURE_DATE = sysdate WHERE account_no = :1', (ac_no,))
            con.commit()
            cur.execute('UPDATE account SET is_active = :1 WHERE account_no = :2', (is_active,ac_no))
            con.commit()
            print("amount :",a[0][0],"Account ",ac_no," is Successfully Closed")
        else:
            print("Invalid Account No",ac_no)

    def  availLoan(self,customerId):
         ac_no = int(input("Input Saving account no"))
         cur.execute('SELECT balance FROM Account where account_no = :1', (ac_no,))
         a = cur.fetchall()
         if a:
             loan_amount = int(input("loan amount"))
             duration = int(input("input duration in month"))
             am = int(a[0][0])
             if loan_amount <= am :
                 cur.execute('INSERT INTO loan VALUES (:1,lnno.nextval,:2,:3,:4,sysdate)',(customerId,ac_no,loan_amount,duration))
                 con.commit()
             print("loan granted")
         else:
             print("Invalid account NO",ac_no)

    def customerLogout(self):
        self.loggedIn = False

con = cx_Oracle.connect("BANK/12345@XE")
cur = con.cursor()
customerId=int(input("Customer Id "))
password = input("password ")
cur.execute('SELECT password FROM customer where c_id = :1',(customerId,))
a = cur.fetchall()
userLog = LoggedIn()
try:
    if a[0][0] == password:
        userLog.logIn()
    else:
        print("wrong Id or password")
except:
    print("Wrong ID ")
try:
    while userLog.loggedIn is True:
        if userLog.loggedIn is True:
            print("1. Address Change ")
            print("2. Open Account")
            print("3. Money Deposit ")
            print("4. Money Withdrawl")
            print("5. Transfer Money")
            print("6. print StateMent")
            print("7. Account Clouser")
            print("8. Avail Loan")
            print("0. Customer logout")
            choice = int(input())
            if  choice==1:
                userLog.changeAdress(customerId)
            elif choice==2:
                print("\tSA: Savings Account")
                print("\tCA: current Account")
                print("\tFD: Fixed Desposite")
                yc = input("account type :")
                if yc == "SA":
                    userLog.saving(customerId)
                elif yc == "CA":
                    userLog.current(customerId)
                elif yc == "FD":
                    userLog.fixed(customerId)
            elif choice==3:
                userLog.moneyDeposite()
            elif choice==4:
                userLog.moneyWithdrwal()
            elif choice==5:
                userLog.transferMoney()
            elif choice==6:
                userLog.printStatement()
            elif choice==7 :
                userLog.accountClouser()
            elif choice==8 :
                 userLog.availLoan(customerId)
            elif choice==0 :
                userLog.customerLogout()
except:
    print("Something Went Wrong,try again")