import mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root',password='password',database='voting')
mycursor=mydb.cursor()

def shownames():
    mycursor.execute('select showname from shows')
    data=mycursor.fetchall()
    for datum in data:
        print(datum[0])

def addUser():
    name = input("Enter your name: ")
    mobile = input("Enter your mobile number: ")
    email = input("Enter your email: ")
    password = input("Set your password: ")
    mycursor.execute('select mobile,email from userdetails')
    data = mycursor.fetchall()
    status = True
    for datum in data:
        if datum[0] == mobile or datum[1] == email:
            print("OOPS!!!,User already exist\nRun as an existing user")
            destination=2
            status = False
            break
    if status:
        mycursor.execute('insert into userdetails (userid,name,mobile,email,password) values(NULL,%s,%s,%s,%s)',
                         (name, mobile, email, password))
        mydb.commit()
    return True

def validateLogin():
    mail = input("Enter your mail id: ")
    password = input("Enter your password: ")
    mycursor.execute('select email,password from userdetails')
    data = mycursor.fetchall()
    status = False
    for datum in data:
        if datum[0] == mail and datum[1] == password:
            status = True
            break
    return status

def adminLogin(mail,password):
    mycursor.execute('select email,password from admin')
    data=mycursor.fetchall()
    for datum in data:
        if datum[0]==mail and datum[1]==password:
            return True
            break
    return False

def showDetails(entity):
    if entity == 'shows':
        mycursor.execute('select * from shows order by showid')
    elif entity == 'wildcard':
        mycursor.execute('select * from wildcard order by scores desc')
    elif entity == 'contestantdetails':
        mycursor.execute('select * from contestantdetails')
    else:
        mycursor.execute('select * from userdetails')
    data = mycursor.fetchall()
    for datum in data:
        for ele in datum:
            print(ele, end=" ")
        print()

def wildcardVoting(showname):
    print("\n\nThe wildcard contestants are: ")
    mycursor.execute('select cont_name,scores,peoplevotes from wildcard where cont_show like %s', (showname,))
    data = mycursor.fetchall()
    for datum in data:
        print(datum[0], "has score of", datum[1], "and the votes received by people is", datum[2])
    voted = input("Enter the contestant name you want to vote")
    mycursor.execute('select peoplevotes from wildcard where cont_name like %s', (voted,))
    value = int(mycursor.fetchone()[0]) + 1
    value = str(value)
    mycursor.execute('update wildcard set peoplevotes = %s where cont_name like %s', (value, voted,))
    mydb.commit()
    return voted

def vote():
    print("The currently running shows are:\n")
    shownames()
    selectedShow=input("Enter the show you want to see about: ").lower()
    print("Enter 1 to see the contestant details\nEnter 2 to vote for the wildcard contestants\n")
    userwants=int(input())
    if userwants==1:
        print("The contestants and their current scores are: ")
        mycursor.execute('select cont_name,scores from contestantdetails where cont_show like %s',(selectedShow,))
        data = mycursor.fetchall()
        for datum in data:
            print(datum[0],'has scored',datum[1])
    if userwants==2:
        contestantName=wildcardVoting(selectedShow)

        print("You have voted for",contestantName.capitalize())
        print("Thank you!!!\U0001F600")

def updateScore():
    pass




if __name__=='__main__':

    print("Welcome to voting")
    print("If your a new user, press 1\nIf you are an existing user, press 2\nIf you are an admin, press 3")
    global destination
    destination=int(input())
    if destination==1:
        if addUser():
            print("Registration success!!!")
            vote()

    if destination==2:
        if validateLogin():
            vote()
        else:
            print("User doesn't exist!")

    if destination==3:
        email=input("Enter your mail: ")
        password=input("Enter your password: ")
        if adminLogin(email,password):
            print("Enter 1 to see show details\nEnter 2 to see wildcard details\nEnter 3 to contestant details\nEnter 4 to see user details\nEnter 5 to exit")
            operation=int(input())
            if operation==1:
                showDetails('shows')

            elif operation==2:
                showDetails('wildcard')

            elif operation==3:
                showDetails('contestantdetails')

            elif operation==4:
                showDetails('userdetails')

            else:
                print("Exiting...")
    updateScores()
