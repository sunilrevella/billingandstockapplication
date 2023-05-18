import sys
import mysql.connector
from datetime import date
from PyQt6.QtWidgets import QMainWindow,QApplication
from mart import *

class mart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui =Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.view.clicked.connect(self.viewStock)
        self.ui.arrivaldate.clicked.connect(self.arrivalDate)
        self.ui.reset.clicked.connect(self.clear)
        self.ui.update.clicked.connect(self.updateStock)
        self.ui.submit.clicked.connect(self.entry)
        self.ui.pushButton.clicked.connect(self.getDetails)
        self.ui.delete_2.clicked.connect(self.deleteStock)
        self.ui.pushButton_5.clicked.connect(self.reset1)
        self.ui.pushButton_4.clicked.connect(self.bill)
        self.l=[]
        self.m=[]
        self.t1="fi"
        self.t2=0
        self.amount=0
        self.row=0
        self.qr=[]
        self.ids=[]
        
        self.ui.pushButton_2.clicked.connect(self.add1)
        self.ui.pushButton_3.clicked.connect(self.rem)
        
    def add1(self):
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "Sunil123",database = "market")  
        cur = myconn.cursor()
        pid = int(self.ui.lineEdit_10.text())
        qnt = int(self.ui.lineEdit_11.text())
        
        sql='select id,Name,price,quantity from mart where id=%s'
        val=[(pid)]
        cur.execute(sql,val)
        r=cur.fetchone()
        print(r)
        self.ui.tableWidget_2.setRowCount(self.row)
        self.ui.tableWidget_2.insertRow(self.row)
        self.ui.tableWidget_2.setItem(self.row,0,QtWidgets.QTableWidgetItem(str(r[0])))
        self.ui.tableWidget_2.setItem(self.row,1,QtWidgets.QTableWidgetItem(str(r[1])))
        self.ui.tableWidget_2.setItem(self.row,2,QtWidgets.QTableWidgetItem(str(r[2])))
        self.ui.tableWidget_2.setItem(self.row,3,QtWidgets.QTableWidgetItem(str(qnt)))
        self.ui.tableWidget_2.setItem(self.row,4,QtWidgets.QTableWidgetItem(str(r[2]*qnt)))
        
        self.row+=1
        self.ui.lineEdit_10.clear()
        self.ui.lineEdit_11.setText("1")
        self.t1=r[1]
        self.t2=r[2]*qnt
        self.l.append(r[1])
        self.m.append(r[2]*qnt)
        self.amount=self.amount+r[2]*qnt
        self.qr.append(qnt)
        self.ids.append(pid)
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "Sunil123",database = "market")  
        cur = myconn.cursor()
        
        sql='update mart set Quantity=%s where id=%s'
        val=(r[3]-qnt,pid)
        cur.execute(sql,val)
        myconn.commit()
        myconn.close()

        print(self.qr)
        print(self.ids)

        print(self.amount)
    def reset1(self):
        self.amount=0
        ss=self.row
        for i in range(ss):
            row1 = self.ui.tableWidget_2.currentRow()
            self.ui.tableWidget_2.removeRow(row1+1)
        self.l.clear()
        self.m.clear()
        self.qr.clear()
        self.row=0
        
        
    def bill(self):
        a=""" \t\tSunil' Mart  \t\t"""
        nas=self.ui.lineEdit_13.text()
        a=a+"\n"+"\t"+"Hi "+nas+" Your Bill is:"
        
        for i in range(len(self.l)):
            print("hI")
            a=a+"\n"+"\t"+str(self.l[i])+"\t\t"+str(self.m[i])+"\t"+"\n"
        a=a+"\t---------------------------------"
        a=a+"\n"+"\t"+"Total  : "+"\t\t"+str(self.amount)+"\t"+"\n"
        print(a)
        QtWidgets.QMessageBox.about(self,"Success",a)
        
        self.amount=0
        ss=self.row
        for i in range(ss):
            row1 = self.ui.tableWidget_2.currentRow()
            self.ui.tableWidget_2.removeRow(row1+1)
        self.l.clear()
        self.m.clear()
        self.row=0
        self.ui.lineEdit_13.setText("")
    def rem(self):
        self.ui.tableWidget_2.removeRow((self.row)-1)
        self.row-=1
        self.amount-=self.m[-1]
        self.l.pop()
        self.m.pop()
        idt=self.ids.pop()
        qnts=self.qr.pop()
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "Sunil123",database = "market")  
        cur = myconn.cursor()
        sql='select quantity from mart where id=%s'
        val=[(idt)]
        cur.execute(sql,val)
        r=cur.fetchone()

        print("-----")
        print(r[0])
        print(qnts)
        print(idt)
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "Sunil123",database = "market")  
        cur = myconn.cursor()
        
        sql='update mart set quantity=%s where id=%s'
        val=((r[0]+qnts),idt)
        cur.execute(sql,val)
        myconn.commit()
        myconn.close()
        
        if(len(self.l)>0):
            self.t1=self.l[-1]
            self.t2=self.m[-1]
        elif(len(self.l)==0):
            self.t1="fi"
            self.t2=0
        

    def viewStock(self):
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "Sunil123",database = "market")  
        cur = myconn.cursor()
        cur.execute("select * from mart")
        res=cur.fetchall()
        for i,j in enumerate(res):
            print(i)
            
        self.ui.tableWidget.setRowCount(0)
        for r_no, r_data in enumerate(res):
            self.ui.tableWidget.insertRow(r_no)
            
            for c_no, data in enumerate(r_data):

                self.ui.tableWidget.setItem(r_no,c_no,QtWidgets.QTableWidgetItem(str(data)))
        myconn.close()
    def arrivalDate(self):
        self.date=self.ui.calendarWidget.selectedDate()
        self.ui.lineEdit_5.setText(self.date.toString("yyyy/MM/dd"))
    def places(self):
        return self.ui.comboBox.currentText()
    def clear(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_7.clear()
        self.ui.lineEdit_8.clear()
    def entry(self):
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "Sunil123",database = "market")  
        cur = myconn.cursor()
        pid = int(self.ui.lineEdit.text())
        pcode = self.ui.lineEdit_2.text()
        name = self.ui.lineEdit_3.text()
        price = float(self.ui.lineEdit_4.text())
        da = str(self.ui.lineEdit_5.text())
        vname = self.ui.lineEdit_6.text()
        vnumber = self.ui.lineEdit_7.text()
        place = self.places()
        quantity = int(self.ui.lineEdit_8.text())
        print(type(da))
        v=[pid,pcode,name,price,da,vname,vnumber,place,quantity]
        print(v)
        sql="insert into mart (id,pcode,Name,price,date_of_arrival, Vendor_name, Vendor_Number, place, quantity) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        val=(pid,pcode,name,price,da,vname,vnumber,place,quantity)
        cur.execute(sql,val)
        myconn.commit()
        myconn.close()
        QtWidgets.QMessageBox.about(self,"Success","Sucessfully Inserted")
        self.statusBar().showMessage('Sucessfully Inserted')
        self.clear()
    def getDetails(self):
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "Sunil123",database = "market")  
        cur = myconn.cursor()
        pid = int(self.ui.lineEdit.text())
        
        sql='select * from mart where id=%s'
        val=[(pid)]
        cur.execute(sql,val)
        r=cur.fetchone()
        print(r)

        self.ui.lineEdit_2.setText(r[1])
        self.ui.lineEdit_3.setText(r[2])
        self.ui.lineEdit_4.setText(str(r[3]))
        self.ui.lineEdit_6.setText(r[5])        
        self.ui.lineEdit_7.setText(r[6])
        self.ui.lineEdit_8.setText(str(r[8]))
        
        self.ui.lineEdit_5.setText(r[4])
    def updateStock(self):
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "Sunil123",database = "market")  
        cur = myconn.cursor()
        
        pid = int(self.ui.lineEdit.text())
        pcode = self.ui.lineEdit_2.text()
        name = self.ui.lineEdit_3.text()
        price = float(self.ui.lineEdit_4.text())
        da = self.ui.lineEdit_5.text()
        vname = self.ui.lineEdit_6.text()
        vnumber = self.ui.lineEdit_7.text()
        place = self.places()
        quantity = int(self.ui.lineEdit_8.text())
        s=[pcode,name,price,da,vname,vnumber,place,quantity,pid]
        print(s)
        sql='update mart set PCode=%s, Name=%s,price=%s,date_of_arrival=%s,Vendor_Name=%s,Vendor_Number=%s,Place=%s,Quantity=%s where id=%s'
        val=(pcode,name,price,da,vname,vnumber,place,quantity,pid)

        cur.execute(sql,val)
        myconn.commit()
        myconn.close()

        QtWidgets.QMessageBox.about(self,"Success","Sucessfully Updated")
        self.statusBar().showMessage('Sucessfully Updated')
        self.clear()
    def deleteStock(self):
        
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "Sunil123",database = "market")  
        cur = myconn.cursor()
        pid = int(self.ui.lineEdit_9.text())

        sql='delete from mart where id=%s'
        val=[(pid)]
        cur.execute(sql,val)
        myconn.commit()
        myconn.close()
        QtWidgets.QMessageBox.about(self,"Success","Sucessfully Deleted")
        self.statusBar().showMessage('Sucessfully Deleted')
        self.clear()
    
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    w = mart()
    list_of_items=''
    d={}
    myconn = mysql.connector.connect(host = "localhost", user = "root",password = "Sunil123",database = "market")  
    cur = myconn.cursor()
    w.show()
    sys.exit(app.exec())
