import mysql.connector
from pandas import DataFrame
import tkinter
conn=mysql.connector.connect(host='localhost',password='0000',user='root',database='emergency_database')
mycursor=conn.cursor()
box=0
r_r=0

def data_in():
    hr("insert fresh data")
    n=int(input("enter number of locations: "))
    for i in range(n):
        print("row",i+1)
        location=input("enter location: ")       
        count=int(input("enter person_count: "))
        mycursor.execute("INSERT INTO emergency_table VALUES('{}',{},{},0,NULL)".format(location,count,count))
        conn.commit()
    hr("SUCCESFUL")

def data_out():
    hr("display existing data")
    L1=[]
    L2=[]
    L3=[]
    L4=[]
    L5=[]
    mycursor.execute("SELECT * FROM emergency_table")
    for i in mycursor:
        L1.append(i[0])
        L2.append(i[1])
        L3.append(i[2])
        L4.append(i[3])
        L5.append(i[4])
    d={"location":L1,"person_count":L2,"required":L3,"allocated":L4,"date_delivered":L5}
    print(DataFrame(d))
    print("resource units available: ",box)
    print("resource units required: ",r_r)
    if(r_r>0):
        print("resource units to be added: ",r_r-box)

def compute():
    hr("initiate computational updation")
    global box,r_r
    while True:
        mycursor.execute("SELECT COUNT(*) FROM emergency_table WHERE resources_required!=0")
        for i in mycursor:
            n=i[0]
        if(n==0 or box-n<0 or box==0):
            break
        mycursor.execute("UPDATE emergency_table SET resources_allocated=resources_allocated+1 WHERE resources_required>0")
        mycursor.execute("UPDATE emergency_table SET resources_required=resources_required-1 WHERE resources_required>0")
        conn.commit();
        box-=n
    mycursor.execute("SELECT SUM(resources_required) FROM emergency_table")
    for i in mycursor:
        r_r=i[0]
    hr("SUCCESFUL")

def reset():
    hr("reset computational updation")
    mycursor.execute("UPDATE emergency_table SET resources_required=person_count WHERE date_delivered IS NULL")
    mycursor.execute("UPDATE emergency_table SET resources_allocated=0 WHERE date_delivered IS NULL")
    conn.commit()
    hr("SUCCESFUL")

def edit():
    hr("update date_delivered for a location")
    location=input("enter location to be updated: ")
    date=input("enter date in (XX/XX/XXXX) format: ")
    mycursor.execute("UPDATE emergency_table SET resources_required=0 WHERE location='{}'".format(location))
    mycursor.execute("UPDATE emergency_table SET resources_allocated=0 WHERE location='{}'".format(location))
    mycursor.execute("UPDATE emergency_table SET date_delivered='{}' WHERE location='{}'".format(date,location))
    conn.commit()
    hr("SUCCESFUL")

def search():
    hr("search a location")
    location=input("enter location: ")
    L1=[]
    L2=[]
    L3=[]
    L4=[]
    L5=[]
    mycursor.execute("SELECT * FROM emergency_table WHERE location='{}'".format(location))
    for i in mycursor:
        L1.append(i[0])
        L2.append(i[1])
        L3.append(i[2])
        L4.append(i[3])
        L5.append(i[4])
    d={"location":L1,"person_count":L2,"required":L3,"allocated":L4,"date_delivered":L5}
    print(DataFrame(d))
    hr("")

def remove():
    hr("delete a location")
    location=input("enter location: ")
    mycursor.execute("DELETE FROM emergency_table WHERE location='{}'".format(location))
    conn.commit()
    hr("SUCCESFUL")

def clear():
    hr("delete existing data")
    mycursor.execute("DELETE FROM emergency_table")
    conn.commit()
    hr("SUCCESFUL")

def BOX():
    hr("increment resource units")
    global box
    n=int(input("enter number of resource units to be added: "))
    box+=n
    hr("SUCCESFUL")

def help():
    print("help")

def menu():
    hr("INPUT/OUTPUT TERMINAL")
    mycursor.execute('CREATE TABLE IF NOT EXISTS emergency_table(location varchar(100) PRIMARY KEY, person_count INT, resources_required INT, resources_allocated INT, date_delivered VARCHAR(10))')
    conn.commit()
    r=tkinter.Tk()
    f1=tkinter.Frame(r)
    f1.pack()
    label=tkinter.Label(f1,text='MENU', width=100,height=1,bg='white',fg='black')
    label.pack()
    b1=tkinter.Button(f1,text='insert fresh data',width=100,height=1,command=data_in,bg='black',fg='white')
    b1.pack()
    f2=tkinter.Frame(r)
    f2.pack(side=tkinter.TOP)
    b2=tkinter.Button(f2,text='display existing data',width=100,height=1,command=data_out,bg='black',fg='white')
    b2.pack()
    f3=tkinter.Frame(r)
    f3.pack(side=tkinter.TOP)
    b3=tkinter.Button(f3,text='initiate computational updation',width=100,height=1,command=compute,bg='black',fg='white')
    b3.pack()
    f4=tkinter.Frame(r)
    f4.pack(side=tkinter.TOP)
    b4=tkinter.Button(f4,text='reset computational updation',width=100,height=1,command=reset,bg='black',fg='white')
    b4.pack()
    f5=tkinter.Frame(r)
    f5.pack(side=tkinter.TOP)
    b5=tkinter.Button(f5,text='update date_delivered for a location',width=100,height=1,command=edit,bg='black',fg='white')
    b5.pack()
    f6=tkinter.Frame(r)
    f6.pack(side=tkinter.TOP)
    b6=tkinter.Button(f6,text='search a location',width=100,height=1,command=search,bg='black',fg='white')
    b6.pack()
    f7=tkinter.Frame(r)
    f7.pack(side=tkinter.TOP)
    b7=tkinter.Button(f7,text='delete a location',width=100,height=1,command=remove,bg='black',fg='white')
    b7.pack()
    f8=tkinter.Frame(r)
    f8.pack(side=tkinter.TOP)
    b8=tkinter.Button(f8,text='delete existing data',width=100,height=1,command=clear,bg='black',fg='white')
    b8.pack()
    f9=tkinter.Frame(r)
    f9.pack(side=tkinter.TOP)
    b9=tkinter.Button(f9,text='increment resource units',width=100,height=1,command=BOX,bg='black',fg='white')
    b9.pack()
    f10=tkinter.Frame(r)
    f10.pack(side=tkinter.TOP)
    b10=tkinter.Button(f10,text='help',width=100,height=1,command=help,bg='black',fg='white')
    b10.pack()
    r.mainloop()

def hr(s):
    print("-"*100,"\n")
    print(s)
    print("\n","-"*100)
    
menu()
