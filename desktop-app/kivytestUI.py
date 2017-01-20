import kivy
from kivy.uix.boxlayout import BoxLayout

kivy.require('1.9.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
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


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ButBrown(Button):
    pass

class DownDialog(RelativeLayout):
    textFileName = StringProperty(None)
    download = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(BoxLayout):
    loadfile = ObjectProperty(None)
    layout_content = ObjectProperty(None)
    list_of_images = []

    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        Clock.schedule_once(self.post_init, 1)

    def post_init(self, *args):
        assert self.layout_content is not None
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))

    def dismiss_popup(self):
        self._popup.dismiss()

    def refresh(self):
        conn = client('s3')  # again assumes boto.cfg setup, assume AWS S3
        for key in conn.list_objects(Bucket='memoirebuckettest')['Contents']:
            if key['Key'] not in self.list_of_images:
                btn = ButBrown(text=key['Key'],size_hint_y=None)
                btn.bind(on_release=self.show_down)
                self.list_of_images.append(key['Key'])
                self.layout_content.add_widget(btn)

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_down(self,*args):
        print args[0].text
        content = DownDialog(textFileName=args[0].text,cancel=self.dismiss_popup)
        self._popup = Popup(title="Download file",
                            content=content,
                            size_hint=(0.5,0.5))
        self._popup.open()


    def load(self, path, filename):
        self.image = {'file':open(os.path.join(path, filename[0]),'rb')}
        #self.text_input.text = stream.read()
        threading.Thread(target=self.uploadPicture).start()

        self.dismiss_popup()

    def uploadPicture(self):
        url = "http://127.0.0.1:8000/polls/"
        s = requests.session()
        r = s.get(url)
        headers = {'X-CSRFToken': s.cookies["csrftoken"]}
        r = s.post(url, files=self.image, cookies=s.cookies, headers=headers)
        self.image['file'].close()



class Editor(App):
    pass

Factory.register('LoadDialog', cls=LoadDialog)


if __name__ == '__main__':
    Editor().run()