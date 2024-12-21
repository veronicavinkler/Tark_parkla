
#MATERJALID
#https://www.techwithtim.net/tutorials/python-module-walk-throughs/kivy-tutorial/object-properties
#https://www.geeksforgeeks.org/python-adding-image-in-kivy-using-kv-file/
#https://kivy.org/doc/stable/guide/packaging.html
#https://www.tutorialspoint.com/kivy/kivy-images.htm
#https://kivy.org/doc/stable/api-kivy.uix.label.html
#https://kivy.org/doc/stable/api-kivy.core.text.html
#https://kivy.org/doc/stable-2.2.0/api-kivy.uix.button.html

#https://www.geeksforgeeks.org/access-modifiers-in-python-public-private-and-protected/

#WINDOW KONFIGUREERIMINE
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '1024')

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.label import Label #widget
from kivy.uix.image import Image #widget
from kivy.uix.button import Button #widget
from kivy.uix.scrollview import ScrollView #widget
from kivy.clock import Clock
from random import randint

import threading
import time
from RPi import GPIO
import I2C_LCD_driver

GPIO.setwarnings(False)

class ParklaApp(App):
    #DEFINING
    free_num = 3
    error_num = 0
    parking_spaces = [False, False, False] #False-vaba, True- pole vaba
    error_spaces = [False, False, False] #False-korras, True- vigane
    ledred = [5, 22, 27]
    ledgreen = [26, 19, 13]
    TRIG = [24, 23, 18]
    ECHO = [21, 20, 16]
    speed_of_sound = 343.0 #because we don't know that

    def __init__(self, **kwargs):        
        super().__init__(**kwargs)
        self.running=True
        self.Initializing()
        self.flo = FloatLayout() #Siia hakkame lisama widgetit

        # Tausta piltide lisamine
        self.flo.add_widget(
            Image(
                source = 'C:/Users/veron/Ajaplaneerimine/back_2.png',
                size_hint = (0.4, 1),
                pos_hint = {"x": 0.60, "y": 0},
                allow_stretch = True))
        self.flo.add_widget(
            Image(
                source = 'C:/Users/veron/Ajaplaneerimine/back_1.jpg',
                size_hint = (0.6, 1),
                pos_hint = {"x": 0, "y": 0},
                allow_stretch = True))
        
        #Logi kirja flo-le lisamine
        self.log_messages = []
        self.log_label = Label( #LOG PEALKIRI
            text="Log sättib valmis...\n",
            halign='left',
            valign='top',
            size_hint=(1, None),
            text_size=(400, None)
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))

        log_scroll = ScrollView( #SCROLLAMISE OSA LOGILE lisamine
            size_hint=(0.4, 0.6),
            pos_hint={'x': 0.55, 'y': 0.3},
            do_scroll_x=False
        )
        log_scroll.add_widget(self.log_label) #Lisame ekraanile
        self.flo.add_widget(log_scroll)
        
        self.Pilt = [ #Autode algsed pildid
            'C:/Users/veron/Ajaplaneerimine/blackcar.png',
            'C:/Users/veron/Ajaplaneerimine/blackcar.png',
            'C:/Users/veron/Ajaplaneerimine/blackcar.png'
            ]
        self.PL = [] #Siia lisatakse pildid ja hakatakse neid vahetama
        for i in range(3):
            parking_lot = Image(
                source = self.Pilt[i],
                size_hint = (0.3, 0.3),
                pos_hint = {"x": (i - 0.26) * 0.2, "y": 0.6},
                allow_stretch = True
            )
            self.flo.add_widget(parking_lot)
            self.PL.append(parking_lot)
        #Ulesannete kaiviamine
        for i in range(3):
            threading.Thread(target=self.monitor_parking_space, args=(i,)).start()
        return self.flo

    def on_stop(self):
        self.running=False
        GPIO.cleanup()
    
    def monitor_parking_space(self, space_num):
        while self.running: #Kui kood jookseb
            dist = self.distance(space_num, self.TRIG, self.ECHO)
            status = self.status(dist)
            self.update_space(space_num, status)
            time.sleep(1) #Jalgitakse iga sekund
    
    def update_space(self, space_num, status):
        self.add_free_and_error()
        self.sum_free_and_error()
        self.add_to_led(space_num, status)
        self.add_to_app(space_num, status)
        self.add_to_screen()
        
    def Initializing(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ledred, GPIO.OUT)
        GPIO.setup(self.ledgreen, GPIO.OUT)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        
    def distance (self, space_num):
        #KAUGUSE MOOTMINE
        GPIO.output(self.TRIG[space_num], False)
        time.sleep(0.1)
        string = f"waiting {space_num} response... \n"
        self.add_to_log(string) #lisame logisse
            
        GPIO.output(self.TRIG[space_num], True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG[space_num], False)

        while GPIO.input(self.ECHO[space_num])==0:
            pulse_start=time.time()
        while GPIO.input(self.ECHO[space_num])==1:
            pulse_end=time.time()
        #MOOTMISTE ARVUTAMINE
        pulse_duration = pulse_end-pulse_start
        distance=(pulse_duration*self.speed_of_sound)/2
        distance = round(distance*100)/2
        return distance
    
    def status(self, distance):
        if distance < 0 or distance >25:
            return "viga"
        elif distance <= 15:
            return "voetud"
        elif distance < 25:
            return "vaba"
        return "wtf"   
        
    def add_free_and_error (self): #Tagastab
        for i in range(3):
            dist = self.distance(i)
            stat = self.status(dist)
            if stat == "voetud":
                self.parking_spaces[i]=True
            elif stat == ["viga","wtf"]:
                self.error_spaces[i]=True
            else:
                self.parking_spaces[i]=False
                self.error_spaces[i]=False
   
    def sum_free_and_error(self):
        self.free_num = self.parking_spaces.count(False)
        self.error_num = self.error_spaces.count(True)
        
    def add_to_led(self, space_num, status):
        if status == "viga":
            for i in range(5):
                GPIO.output(self.ledred[space_num], True)
                GPIO.output(self.ledgreen[space_num], True)
                time.sleep(0.5)
                GPIO.output(self.ledred[space_num], False)
                GPIO.output(self.ledgreen[space_num], False)
                time.sleep(0.5)
                i +=1
        elif status == "voetud": #led punane
            GPIO.output(self.ledred[space_num], True) #LED
            GPIO.output(self.ledgreen[space_num], False) #LED
        elif status == "vaba":#LED roheline pannakse polema
            GPIO.output(self.ledred[space_num], False)
            GPIO.output(self.ledgreen[space_num], True)
        else:
            for i in range(5): #Kaivitame blinkimise
                GPIO.output(self.ledred[space_num], True)
                GPIO.output(self.ledgreen[space_num], True)
                time.sleep(0.5)
                GPIO.output(self.ledred[space_num], False)
                GPIO.output(self.ledgreen[space_num], False)
                time.sleep(0.5)
                i +=1
    
    def add_to_screen(self): #Lisame teavituse I2C ekraanile
        string = f"{self.free_num} spaces is free"
        mylcd = I2C_LCD_driver.lcd()
        mylcd.lcd_display_string(string, 1)
        string = f"{self.free_num} spaces has error"
        mylcd.lcd_display_string(string, 2)
        
    def add_to_app(self, space_num, status):
        if status == "viga":
            string = f"Parkimise kohal {space_num} in VIGA" #STRING LOG jaoks
            self.PL[space_num-1].source = 'C:/Users/veron/Ajaplaneerimine/blackcar.png' #APP Pilt
        elif status == "voetud":
            string = f"Parkimise koht {space_num+1} on võetud" #STRING LOG jaoks
            self.PL[space_num-1].source = 'C:/Users/veron/Ajaplaneerimine/redcar.png' #APP Pilt
        elif status == "vaba":
            string = f"Parkimise koht {space_num} on vaba" #STRING LOG jaoks
            self.PL[space_num-1].source = 'C:/Users/veron/Ajaplaneerimine/greencar.png' #APP Pilt
        else:
            string = "Wtf"
        self.add_to_log(string) #Kasutaame funktsiooni, et lisadateavituse

    def add_to_log(self, message):
        string = f"[b][color=#6E4B34]{message}[/color][/b]" #lisame teksti boldi ja värvime pruuniks
        self.log_messages.append(string) #lisame teavituse build meetodisse olevasse listi
        Clock.schedule_once(lambda dt: self.update_log_label(string))

    def update_log_label(self, string):
        self.log_label.text += string + "\n" #lisame rea
        self.log_label.markup = True #enabling markup label-jaoks

if __name__ == '__main__': 
    ParklaApp().run()

