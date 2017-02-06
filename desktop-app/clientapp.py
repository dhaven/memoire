import kivy
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanelItem
import re

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

class My_t_p_i(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(My_t_p_i, self).__init__(**kwargs)
        self.source = 'grey.png'

    def on_state(self, widget, value):
        if value == 'down':
            self.background_down = 'white.png'
            widget.color = (0,0,0,1)
        else:
            self.background_down = 'grey.png'
            widget.color = (1,1,1,1)

#represents the dialog for uploading a file
class UploadDialog(FloatLayout):
    upload = ObjectProperty(None)
    cancel = ObjectProperty(None)

#custom button
class ButBrown(Button):
    pass

#represents the dialog for downloading an image
class DownloadDialog(FloatLayout):
    download = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    textFileName = StringProperty(None)


class HomeScreen(BoxLayout):
    username = ObjectProperty(None)
    layout_content = ObjectProperty(None)
    list_of_images = []

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.post_init, 1)
        for key, value in kwargs.iteritems():
            if key == 'session':
                self.s = value

    def post_init(self, *args):
        assert self.layout_content is not None
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))

    def dismiss_popup(self):
        self._popup.dismiss()

    # get the list of all pictures stored on the cloud and display
    # file names to the user
    def refresh(self):
        url = "http://127.0.0.1:8000/polls/list/{}".format(re.sub("Welcome ","",self.username.text))
        r = self.s.get(url, stream=True)
        dicImages =r.json()
        for key in dicImages.keys():
            for value in dicImages[key]:
                if value not in self.list_of_images:
                    btn = ButBrown(text=value, size_hint_y=None)
                    btn.bind(on_release=self.show_download_dialog)
                    self.list_of_images.append(value)
                    self.layout_content.add_widget(btn)

    def refresh_thread(self):
        threading.Thread(target=self.refresh).start()

    # show the upload dialog to the user
    def show_upload_dialog(self):
        content = UploadDialog(upload=self.uploadPicture_thread, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    # show the download dialog to the user
    def show_download_dialog(self, *args):
        content = DownloadDialog(download=self.download_thread, cancel=self.dismiss_popup, textFileName=args[0].text)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def download_thread(self, listTuple):
        threading.Thread(target=self.download, args=listTuple).start()
        self.dismiss_popup()

    # download a picture identified by "remoteFilename" and
    # save it locally as "localFilename"
    def download(self, path, remoteFilename, localFilename):
        url = "http://ec2-34-250-110-229.eu-west-1.compute.amazonaws.com/polls/image/{}".format(remoteFilename)
        s = requests.session()
        r = s.get(url, stream=True)
        with open(os.path.join(path, localFilename), 'wb') as stream:
            for chunk in r.iter_content(1024):
                stream.write(chunk)

        self.dismiss_popup()

    def uploadPicture_thread(self, listTuple):
        threading.Thread(target=self.uploadPicture, args=listTuple).start()
        self.dismiss_popup()

    # upload a picture to the cloud
    def uploadPicture(self, path, filename):
        self.image = {'file': open(os.path.join(path, filename[0]), 'rb')}
        url = "http://ec2-34-250-110-229.eu-west-1.compute.amazonaws.com/polls/"
        s = requests.session()
        r = s.get(url)
        headers = {'X-CSRFToken': s.cookies["csrftoken"]}
        r = s.post(url, files=self.image, cookies=s.cookies, headers=headers)
        self.image['file'].close()

    def logout(self):
        url = "http://127.0.0.1:8000/logout/"
        r = self.s.get(url,stream=True)
        self.clear_widgets()
        login_screen = Login_screen()
        self.add_widget(login_screen)

class Login_screen(BoxLayout):
    rootLogin = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Login_screen, self).__init__(**kwargs)
        url = "http://127.0.0.1:8000/login/"
        self.s = requests.session()
        r = self.s.get(url, stream=True)

    def home(self, username):
        self.clear_widgets()
        home = HomeScreen(session=self.s)
        self.add_widget(home)
        home.username.text = "Welcome {}".format(username)

    def login(self, username, password):
        if self.rootLogin.login_tab.error_login.text == 'username and/or password is wrong':
            self.rootLogin.login_tab.error_login.text = ''
        url = "http://127.0.0.1:8000/login/"
        payload = {'username': username, 'password': password}
        headers = {'X-CSRFToken': self.s.cookies["csrftoken"]}
        r = self.s.post(url, cookies=self.s.cookies, headers=headers, data=payload)
        if 'sessionid' in self.s.cookies:
            self.home(r.json()['username'])
        else:
            self.rootLogin.login_tab.error_login.text = "username and/or password is wrong"

class Root(BoxLayout):
    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        self.add_widget(Login_screen())

class Clientapp(App):
    pass

#Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    Clientapp().run()