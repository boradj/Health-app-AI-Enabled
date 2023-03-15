

"""
    This module contains a function to temporarily take the user name,
    notification timer setting, and current chosen motivation task for reminder
    and store it into the different temporary text files which could over written everytime a 
    new user logins into the app.

"""


# function to store the temporary name into the text file tempUser.txt
def storeName(name):
    with open("tempUsername.txt","w") as file:
        file.write(name)


# function to read the name of temporary user from the file tempUser.txt
def readName():
    with open("tempUsername.txt","r") as file:
        return file.read()



""" It also stores the notification timer setting given by the user
and also resets the screens at the time of logout to 2 hours so that it stays
default"""
# this will store the notification timer until logout
def storeNotificationTimer(hours):
    with open("tempNotificationTimer.txt","w") as file:
        file.write(str(hours))


# this function gets the selected timer value by the user
def readNotificationTimer():
    with open("tempNotificationTimer.txt","r") as file:
        return file.read()

# this function stores the current motivation 
def storeMotivation(task):
    with open("tempMotivationTask.txt","w") as file:
        file.write(str(task))

# this function reads the current motivation
def readMotivation():
    with open("tempMotivationTask.txt","r") as file:
        return file.read()
