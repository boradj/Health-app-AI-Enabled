""" Requirement: The manager should use an own database (table) to select motivation tasks according to 
job type, gender, age and the  actual movement profile. 
The database can be a separate file, which is read by the application."""

import sqlite3
import push_notification


# This function will get the task from the taskmanager databse using input parameters.
# The 4 output tasks will be displayed in the card widget
def getTask(jobType, gender, age):

    movementProfile = "Get the movement profile from the ai, using its function"
    
    # connect to the database here and input the above parameters to get the task

    # return 4 tasks using the input data, and each return can be used in for/while loop and entered in the UI card
    # return Task1
    # return Task2
    # return Task3   
    # return Task4


    # a new database must be created which contains job type, gender, age, actual movement profile (from ai)
    # I call this function anywhere and pass in the above parameters, BUT, movementProfile will come only from ai while other 3 will come from userinput
    

# This function only pushes the task which has been selected by user and activates after "Remind me button"
def taskNotif(Task):
    push_notification.pushNotif(Task)