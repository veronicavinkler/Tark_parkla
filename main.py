import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *

#MATERJALID
#https://www.techwithtim.net/tutorials/python-module-walk-throughs/kivy-tutorial/object-properties
#https://www.geeksforgeeks.org/python-adding-image-in-kivy-using-kv-file/
#https://kivy.org/doc/stable/guide/packaging.html
#https://www.tutorialspoint.com/kivy/kivy-images.htm
#https://kivy.org/doc/stable/api-kivy.uix.label.html
#https://kivy.org/doc/stable/api-kivy.core.text.html
#https://kivy.org/doc/stable-2.2.0/api-kivy.uix.button.html


class My(Widget):
    pass

class MyApp(App):
    def build(self):
        return My()

if __name__ == '__main__':
    MyApp().run()
