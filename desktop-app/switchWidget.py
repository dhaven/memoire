import kivy
from kivy.uix.boxlayout import BoxLayout

kivy.require('1.9.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button

from boto3 import client
import os
import requests
import threading

#custom button
class HomeScreen(BoxLayout):
    username = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        for key, value in kwargs.iteritems():
            if key == 'session':
                self.s = value
    def logout(self):
        url = "http://127.0.0.1:8000/logout/"
        r = self.s.get(url,stream=True)
        self.clear_widgets()
        login_screen = Login_screen()
        self.add_widget(login_screen)

class Login_screen(BoxLayout):
    error_login = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Login_screen, self).__init__(**kwargs)
        url = "http://127.0.0.1:8000/login/"
        self.s = requests.session()
        r = self.s.get(url, stream=True)

    def home(self,username):
        self.clear_widgets()
        home = HomeScreen(session=self.s)
        self.add_widget(home)
        home.username.text = "Welcome {}".format(username)

    def login(self,username,password):
        if self.error_login.text == 'username and/or password is wrong':
            self.error_login.text = ''
        url = "http://127.0.0.1:8000/login/"
        payload = {'username':username, 'password':password}
        headers = {'X-CSRFToken': self.s.cookies["csrftoken"]}
        r = self.s.post(url, cookies=self.s.cookies, headers=headers,data=payload)
        if 'sessionid' in self.s.cookies:
            self.home(r.json()['username'])
        else:
            self.error_login.text = "username and/or password is wrong"

class Root(BoxLayout):
    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        self.add_widget(Login_screen())

class Switch(App):
    pass

#Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    Switch().run()