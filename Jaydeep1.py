import sensorsAccess
import lstmModel
import aimodelbegin
from plyer import gyroscope
from plyer import accelerometer
import taskManager
import push_notification
import managingDb
import RSAencryption
import usertemporary
from kivy.properties import ObjectProperty
import sqlite3
from kivy.utils import platform
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivymd_extensions.akivymd import *
from kivy.metrics import dp
from kivymd_extensions.akivymd.uix.charts import AKPieChart
import matplotlib.pyplot as plt
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from kivy.uix.widget import Widget
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from unicodedata import name
from kivymd.app import MDApp


# importing module which made for fulfilment of requirement


# importing encryption code for encrypting-decrypting database


# module import for adding new user


# module for a notification


# Library for ai model


# import module for ai model implementation


# import module for permission

Window.size = (320, 500)


class ScreenWallpaper(BoxLayout):
    pass


class LoginScreen(Screen):
    usr = ObjectProperty(None)
    psw = ObjectProperty(None)

    def signinBtn(self):

        # temporary store username and password
        u = self.ids["usr"].text
        p = self.ids["psw"].text

        # storing the temporary user in usertemporary

        usertemporary.save(u)

        # decrypting database data to check credential valid or not

        RSAencryption.decryptionfile()

        # connecting the database to use

        conn = sqlite3.connect('users.db')

        # cursor to excessing file

        c = conn.cursor()

        c.execute("""SELECT username, password FROM data""")

        items = c.fetchall()  # fetching all available usernames from sqldatabase
        for i in range(len(items)):

            if u == items[i][0] and p == items[i][1]:
                self.ids["usr"].text = ""
                self.ids["psw"].text = ""
                self.parent.current = "mainscreen"
            else:
                if u == items[i][0] and p != items[i][1]:
                    self.psw.text = "Invalid Password"

                else:
                    self.usn.text = "Invalid Username"

        conn.commit()

        conn.close()

        # encrypting again after excessing data
        RSAencryption.encryptionfile()
        self.usn.text = ""

    def signUpButton(self):

        self.parent.current = "signupscreen"


class Signup(Screen):
    usr = ObjectProperty(None)
    psw = ObjectProperty(None)
    cnf = ObjectProperty(None)

    def tologin(self):
        self.parent.current = "loginscreen"

    def createaccount(self):

        if self.ids["usr"].text and self.ids["psw"].text and self.ids["cnf"].text is not None:

            user = self.ids["usr"].text
            password = self.ids["psw"].text
            confirm = self.ids["cnf"].text

            # check wheather password is equal to confirm password
            if password == confirm:

                # if pasword and confirm password is same than store adduser

                managingDb.addUser(user, password)

                self.parent.current = "loginscreen"

            else:
                self.psw1.text = "password is not matching"

        else:
            self.psw1.text = "Invalid credential"
   # resets signup all details after storing it

        u = ""
        p = ""
        co = ""


class Main(Screen):

    # function to remind user about his/her selected motivation task
    # in the notification select by default 2 hour
    def remind_me_bttn(self):
        if self.mot1.active:
            tsk1 = self.ids.task1.text
            push_notification.repeatNotif()

            push_notification.startTimer()

        elif self.mot2.active:
            tsk2 = self.ids.task2.text
            push_notification.repeatNotif()

            push_notification.startTimer()

        elif self.mot3.active:
            tsk3 = self.ids.task3.text
            push_notification.repeatNotif()

            push_notification.startTimer()

        elif self.mot4.active:
            tsk4 = self.ids.task4.text
            push_notification.repeatNotif()

            push_notification.startTimer()

    # this will initiate the model which will start taking sensor data e.g. acceleromoter and gyroscope
    # feed the data to model

    def lstm_on(self):

        # enable lstm_on model

        if platform == "android":

            lstmModel.feedAI()
        else:
            aimodelbegin.Load_Model()
            aimodelbegin.predict2()

    # this will check out off the model

    def lstm_off(self):

        accelerometer.disable()
        gyroscope.disable()

    # fetching the first task and show it on motivation task card

    def motivation_task_1(self):
        return managingDb.getTask()[0]

    # fetching the second task and show it on motivation task card

    def motivation_task_2(self):
        return managingDb.getTask()[1]

    # fetching the third task and show it on motivation task card

    def motivation_task_3(self):
        return managingDb.getTask()[2]

    # fetching the fourth task and show it on motivation task card

    def motivation_task_4(self):
        return managingDb.getTask()[3]

    # funtion to stop notification popup

    def notification_pause(self):
        pass

    # on click start showing notification again

    def notification_unpause(self):
        taskManager.taskNotif("Here must be the selected task from the UI")

    def activityGraph(self):
        self.parent.current = "activitiygraph"

    def settingScreen(self):
        self.parent.current = "setting"


class ActivityGraph(Screen):
    def __init__(self, **kwargs):
        self.title = "KivyMD Examples - Bottom Navigation"
        super().__init__(**kwargs)

    items = [{"Python": 40, "Java": 30, "C++": 10, "PHP": 8, "Ruby": 12}]

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self):
        self.piechart = AKPieChart(
            items=self.items,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(dp(300), dp(300)),
        )
        self.ids.chart_box.add_widget(self.piechart)

    def update_chart(self):
        self.piechart.items = [{"Python": 70, "Dart": 10, "C#": 10, "Css": 10}]

    def remove_chart(self):
        self.ids.chart_box.remove_widget(self.piechart)


class Setting(Screen):

    # connecting to notification screen

    def notification(self):
        self.parent.current = "notification"

    # connecting to userdatasave screen

    def profile(self):
        self.parent.current = "editprofile"

    # function to connecting logout switch to main screen of login

    def backtologin(self):

        # on click logout button Notification Timer should be set default to 2 hour

        usertemporary.storeNotificationTimer(2)

        self.parent.current = "loginscreen"

    # function to get back to mainscreen

    def backward(self):
        self.parent.current = "mainscreen"

    # function to show user's entered data

    def displayData(self):

        self.parent.current = "userdatasave"


class EditProfile(Screen):
    name = ObjectProperty(None)
    age = ObjectProperty(None)
    weight = ObjectProperty(None)
    height = ObjectProperty(None)
    job = ObjectProperty(None)
    m = ObjectProperty(None)

    # function to store user new data

    def save(self):

        name = self.ids["name1"].text

        weight = self.ids["weight"].text
        h = self.ids["heigh"].text

        # Getting the job status from checkbox

        if self.ex1.active:
            job = "executive"

        elif self.manager.active:
            job = "manager"

        elif self.programmer.active:
            job = "programmer"

        # Getting age values from checkbox

        if self.age1.active:
            age = "21-30"

        elif self.age2.active:
            age = "31-40"

        elif self.age3.active:
            age = "41-50"

        elif self.age4.active:
            age = "51+"

        # Getting data related to gender

        if self.male.active:
            gender = "male"

        elif self.female.active:
            gender = "female"

        # storing data in to sqldatabase

        managingDb.addProfile(name, age, weight, h, job, gender)

        popup = Popup(
            title='Saved',
            content=Label(text='Your data has been saved securely'),
            size_hint=(0.5, 0.5)
        )

        popup.open()

    def backward(self):
        self.parent.current = "setting"


class NotificationScreen(Screen):

    # save function to store NotificationTimer

    def save(self):

        # if this checkbox active than set notification timer to 1 hour

        if self.oneH.active:
            usertemporary.storeNotificationTimer(1)

        # if this checkbox active than set notification timer to 2 hour

        elif self.twoH.active:
            usertemporary.storeNotificationTimer(2)

        # if this checkbox active than set notification timer to 3 hour

        elif self.threeH.active:
            usertemporary.storeNotificationTimer(3)

        # if this checkbox active than set notification timer to 4 hour

        elif self.fourH.active:
            usertemporary.storeNotificationTimer(4)

    # function to get back to setting

    def back(self):
        self.parent.current = "setting"


class UserDatascreen(Screen):

    if managingDb.userGender != None:

        # to show data store data in to variable

        username = StringProperty(managingDb.userName)
        userage = StringProperty(managingDb.userAge)
        usergender = StringProperty(managingDb.userGender)
        userweight = StringProperty(managingDb.userWeight)
        userheight = StringProperty(managingDb.userHeight)
        userposition = StringProperty(managingDb.userPosition)

    else:

        # show empty data in to userdata if there is not data into sqldatase

        username = StringProperty("empty")
        userage = StringProperty("empty")
        usergender = StringProperty("empty")
        userweight = StringProperty("empty")
        userheight = StringProperty("empty")
        userposition = StringProperty("empty")


class SystemPermissionScreen(Screen):

    # function to allow permission of accelerometer

    def allowAccelerometer(self):
        sensorsAccess.allowAccelero

    # function to allow permission of gyroscope

    def allowGyrometer(self):
        sensorsAccess.allowGyro

    # function to allow permission of excessing

    def allowStorage(self):
        sensorsAccess.memoryAccess


sm = ScreenManager()
sm.add_widget(LoginScreen(name='loginscreen'))
sm.add_widget(Signup(name='signupscreen'))
sm.add_widget(Main(name='mainScreen'))
sm.add_widget(ActivityGraph(name='ActivityGraphScreen'))
sm.add_widget(Setting(name='setting'))
sm.add_widget(EditProfile(name='editprofile'))
sm.add_widget(NotificationScreen(name="notification"))
sm.add_widget(UserDatascreen(name='userdatasave'))
sm.add_widget(SystemPermissionScreen(name='systempermission'))


class MainCard(MDCard):
    pass


class MovementAnalysisCard(MainCard):
    pass


class ControlAnalysisCard(MainCard):
    pass


class MotivationTaskCard(MainCard):
    pass


class MyApp(MDApp):  # inheriting the properties of App class from kivy library

    # if sqldatabase is not available than create one.

    managingDb.creatingTable()

    # if sqltaskmanager is not available than create one.

    managingDb.creatingTableTaskManager()

    # intinating sql database to store the user's movement profile

    managingDb.createTableStoreProfile()

    def build(self):
        self.theme_cls.theme_style = "Light"

        # loading kivymd file in to in to the app

        return Builder.load_file("myapp2.kv")


if __name__ == "__main__":
    MyApp().run()
