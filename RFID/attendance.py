import mysql.connector
import sys
from datetime import datetime
from time import sleep
from mfrc522 import SimpleMFRC522
from datetime import date
import calendar
import datetime
mydate = datetime.datetime.now()
month=mydate.strftime("%B")
my_date=date.today()
day=calendar.day_name[my_date.weekday()]
reader=SimpleMFRC522()
ip=input("Enter database server IP:")
mydb=mysql.connector.connect(host=ip,user="raspi",password="root",database="project")
mycursor=mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS temp_scan (RFID VARCHAR(50), Count VARCHAR(5), ID Varchar(10))")
mycursor.execute("Truncate table temp_scan")
mydb.commit()
try:
        while True:
                sleep(2)
                print("Today is: %s"%day)
                print("Scan your ID:")
                tag=reader.read()
                tag_id=tag[0]
                mycursor.execute("Select UID from student where RFID_S=%s"%tag_id)
                UID=mycursor.fetchone()
                if not UID:
                        mycursor.execute("Select TID from login where RFID_T=%s"%tag_id)
                        rec=mycursor.fetchall()
                        mycursor.execute("select Subject from teacherinfo where TID='%s'"%rec[0])
                        rec=mycursor.fetchall()
                        mycursor.execute("Update attendance Set Conducted=Conducted+1 where Subject='%s'"%rec[0])
                        mydb.commit()
                        print(tag_id)
                        print("Subject: %s"%rec[0])
                        sleep(2)

                else:
                        #mycursor.execute("Select UID from student where RFID_S=%s"%tag_id)
                        #UID=mycursor.fetchall()
                        print(UID[0])
                        mycursor.execute("Insert into temp_scan (RFID,ID) Values('%s','%s')"%(tag_id,UID[0]))   
                        mycursor.execute("Select Class from student where RFID_S=%s"%tag_id)
                        course=mycursor.fetchone()
                        print(course[0])
                        clas=course[0]
                        mycursor.execute("Select conducted,attended from attendance where UID='%s' AND Month='%s'"%(UID[0],month))
                        records=mycursor.fetchall()
                        a = 0
                        for rec in records:
                                if(rec[0]<=rec[1]):
                                        
                                        a = 1
                        if a:
                                print("Lectures attended cannot be more than lectures conducted.")
                                continue        
                        
                        if(day=="Monday"):
                                print("Doing something")
                                sleep(2)
                                if(clas=="TY-IT(A)"):
                                        subject=["ITSM","BI","SQA","SIC"]

                                if(clas=="TY-IT(B)"):
                                        subject=["GIS","SIC","ITSM","BI"]  

                                print("\nCurrent Attendance:")   
                        
                                for x in subject:
                                        query="Select * from attendance where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],x,month)
                                        mycursor.execute(query)
                                        records=mycursor.fetchall()
                                        print(records)
                                        sleep(2)

                                print("\nAttendance successfully updated:")  
                                for y in subject:
                                        query="Update attendance SET Attended=Attended+1 where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],y,month)
                                        mycursor.execute(query)
                                        mydb.commit()
                                        query="Select * from attendance where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],y,month)
                                        mycursor.execute(query)
                                        records=mycursor.fetchall()
                                        print(records)
                        if(day=="Tuesday"):
                                print("Doing something")
                                sleep(2)
                                if(clas=="TY-IT(A)"):
                                        subject=["ITSM","BI","GIS","SIC"]

                                if(clas=="TY-IT(B)"):
                                        subject=["GIS","SQA","BI","SIC"] 
                                print("Current Attendance:\n")
                                for x in subject:
                                        query="Select * from attendance where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],x,month)
                                        mycursor.execute(query)
                                        records=mycursor.fetchall()
                                        print(records)               
                                        sleep(2)
                                print("Attendance successfully updated:\n")       
                                for y in subject:
                                        query="Update attendance SET Attended=Attended+1 where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],y,month)
                                        mycursor.execute(query)
                                        mydb.commit()
                                        query="Select * from attendance where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],y,month)
                                        mycursor.execute(query)
                                        records=mycursor.fetchall()
                                        print(records)
                        if(day=="Wednesday"):
                                print("Doing something")
                                sleep(2)
                                if(clas=="TY-IT(A)"):
                                        subject=["BI","SQA","SIC","ITSM"]

                                if(clas=="TY-IT(B)"):
                                        subject=["SIC","GIS","BI","SQA"] 

                                print("Current Attendance:\n")
                                print(subject)
                                for x in subject:
                                        query="Select * from attendance where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],x,month)
                                        mycursor.execute(query)
                                        records=mycursor.fetchall()
                                        print(records)
                                        sleep(2)
                                print("Attendance successfully updated:\n")       
                                for y in subject:
                                        query="Update attendance SET Attended=Attended+1 where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],y,month)
                                        mycursor.execute(query)
                                        mydb.commit()
                                        query="Select * from attendance where UID='%s'AND Subject='%s' AND Month='%s'"%(UID[0],y,month)
                                        mycursor.execute(query)
                                        records=mycursor.fetchall()
                                        print(records)
                        if(day=="Thursday"):
                                print("Doing something")
                                sleep(2)
                                if(clas=="TY-IT(A)"):
                                        subject=["BI","SQA","SIC","ITSM"]

                                if(clas=="TY-IT(B)"):
                                        subject=["SIC","GIS","SQA","SQA"] 
                                
                                print("Current Attendance:\n")
                                for x in subject:
                                        query="Select * from attendance where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],x,month)
                                        mycursor.execute(query)
                                        records=mycursor.fetchall()
                                        print(records)
                                        sleep(2)

                                print("Attendance successfully updated:\n")      
                                for y in subject:
                                        query="Update attendance SET Attended=Attended+1 where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],y,month)
                                        mycursor.execute(query)
                                        mydb.commit()
                                        query="Select * from attendance where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],y,month)
                                        mycursor.execute(query)
                                        records=mycursor.fetchall()
                                        print(records)
                        if(day=="Friday"):
                                print("Doing something")
                                sleep(2)
                                if(clas=="TY-IT(A)"):
                                        subject=["SIC","SQA","GIS","ITSM"]

                                if(clas=="TY-IT(B)"):
                                        subject=["BI","ITSM","SQA","GIS"] 
                                print("Current Attendance:\n")
                                for x in subject:
                                        query="Select * from attendance where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],x,month)
                                        mycursor.execute(query)
                                        records=mycursor.fetchall()
                                        print(records)
                                        sleep(2)                                      
                                print("Attendance successfully updated:\n")      
                                for y in subject:
                                        query="Update attendance SET Attended=Attended+1 where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],y,month)
                                        mycursor.execute(query)
                                        mydb.commit()
                                        query="Select * from attendance where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],y,month)
                                        mycursor.execute(query)
                                        records=mycursor.fetchall()
                                        print(records)
                        if(day=="Saturday"):
                                print("Doing something")
                                sleep(2)
                                if(clas=="TY-IT(A)"):
                                        subject=["GIS","ITSM","GIS","SQA"]

                                if(clas=="TY-IT(B)"):
                                        subject=["BI","SQA","ITSM","GIS"] 
                                print("Current Attendance:\n")
                                for x in subject:
                                        query="Select * from attendance where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],x,month)
                                        mycursor.execute(query)
                                        records=mycursor.fetchall()
                                        print(records)
                                        sleep(2)
                                print("Attendance successfully updated:\n")        
                                for y in subject:
                                        query="Update attendance SET Attended=Attended+1 where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],y,month)
                                        mycursor.execute(query)
                                        mydb.commit()
                                        query="Select * from attendance where UID='%s' AND Subject='%s' AND Month='%s'"%(UID[0],y,month)
                                        mycursor.execute(query)
                                        records=mycursor.fetchall()
                                        print(records)
except KeyboardInterrupt:
        mycursor.execute("Select RFID From temp_scan Where Count IS NULL")
        records=mycursor.fetchall()
        count=len(records)
        mycursor.execute("Update attendance set Missed=Conducted-Attended")
        mydb.commit()
        mycursor.execute("Update attendance set Percentage=(Attended/Conducted)*100")
        mydb.commit()
        mycursor.execute("Insert into temp_scan (Count) Values('%s')"%count)
        mydb.commit()
        mydb.close()