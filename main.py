
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

    def build(self):        
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
        t1 = threading.Thread(target=self.mp, args=(1, TRIG[0], ECHO[0]))
        t2 = threading.Thread(target=self.mp, args=(2, TRIG[1], ECHO[1]))
        t3 = threading.Thread(target=self.mp, args=(3, TRIG[2], ECHO[2]))
        
        t1.start()
        time.sleep(1)
        t2.start()
        time.sleep(2)
        t3.start()
        time.sleep(3)
        
        self.add_free(self)
        return self.flo
    
    def Initializing(self, ledred, ledgreen, TRIG, ECHO):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ledred, GPIO.OUT)
        GPIO.setup(ledgreen, GPIO.OUT)
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
    
    def add_free_and_error (self, trig, echo): #Tagastab
        for i in range(3):
            d = distance(i, trig[i-1], echo[i-1])
            stat = status(d)
            if stat == "voetud":
                parking_spaces[i-1]=True
            elif stat == "viga" or "wtf":
                error_spaces[i-1]=True
   
    def sum_free_and_error(self, parking_spaces, error_spaces, free_num, error_num):
        free_num = parking_spaces.count(False)
        error_num = error_spaces.count(True)
            
    def distance (self, space_num, trig, echo):
        #KAUGUSE MOOTMINE
        GPIO.output(trig, False)
        time.sleep(0.1)
        string = f"waiting {self.space_num} response... \n"
        self.add_to_log(string) #lisame logisse
            
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)

        while GPIO.input(echo)==0:
            pulse_start=time.time()
        while GPIO.input(echo)==1:
            pulse_end=time.time()
            
        #MOOTMISTE ARVUTAMINE
        pulse_duration = pulse_end-pulse_start
        distance=(pulse_duration*speed_of_sound)/2
        distance = round(distance*100)/2
            
        string = f"Ootan vastust parkimise kohalt {space_num}"
        self.add_to_log(string)
            
        status = self.p_checking(distance)
        add_to_led(space_num, status, ledred, ledgreen)
        time.sleep(2)

    def status(self, distance):
        if distance < 0 or distance >25:
            return "viga"
        elif distance <= 15:
            return "voetud"
        elif distance < 25:
            return "vaba"
        return "wtf"
        
    def add_to_led(self, space_num, status, ledred, ledgreen):
        if status == "viga":
            for i in range(5):
                GPIO.output(ledred[space_num-1], True)
                GPIO.output(ledgreen[space_num-1], True)
                time.sleep(0.5)
                GPIO.output(ledred[space_num-1], False)
                GPIO.output(ledgreen[space_num-1], False)
                time.sleep(0.5)
                i +=1
        elif status == "voetud":
            GPIO.output(ledred[space_num-1], True) #LED
            GPIO.output(ledgreen[space_num-1], False) #LED
        elif status == "vaba":
            GPIO.output(ledred[space_num-1], False)
            GPIO.output(ledgreen[space_num-1], True)
        else:
            for i in range(5):
                GPIO.output(ledred[space_num-1], True)
                GPIO.output(ledgreen[space_num-1], True)
                time.sleep(0.5)
                GPIO.output(ledred[space_num-1], False)
                GPIO.output(ledgreen[space_num-1], False)
                time.sleep(0.5)
                i +=1
    def add_to_screen(self)
    def ubuntu(self, space_num, status, distance, ledred, ledgreen, Parking_spaces):
        if status == "viga":
            string = f"Parkimise kohal {space_num} in VIGA"
            self.PL[space_num].source = 'C:/Users/veron/Ajaplaneerimine/blackcar.png' #APP Pilt
            for i in range(5): #VEA EFFEKTI GENEREERIMINE LED
            self.Parking_spaces[space_num-1] = True #Parkimise koha seisund
        elif status == "voetud":
            string = f"Parkimise koht {space_num+1} on võetud" #STRING LOG jaoks
            #PILDIVAHETAMINE VASTAVALTSEISUNDILE
            self.PL[space_num].source = 'C:/Users/veron/Ajaplaneerimine/redcar.png' #APP Pilt
            self.Parking_spaces[space_num-1] = False #Parkimise koha seisund
        elif status == "vaba":
            string = f"Parkimise koht {space_num} on vaba" #STRING LOG jaoks
            self.PL[space_num-1].source = 'C:/Users/veron/Ajaplaneerimine/greencar.png' #APP Pilt
            self.Parking_spaces[space_num-1] = True #Parkimise koha seisund
        else:
            string = "Wtf"
        self.add_to_log(string) #SONUMI LISAMINE LOGI

    def add_to_log(self, message):
        string = f"[b][color=#6E4B34]{message}[/color][/b]" #lisame teksti boldi ja värvime pruuniks
        self.log_messages.append(string)
        self.log_label.text += string + "\n" #lisame rea
        self.log_label.markup = True #enabling markup label-jaoks

if __name__ == '__main__': 
    ParklaApp().run()

