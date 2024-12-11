
#MATERJALID
#https://www.techwithtim.net/tutorials/python-module-walk-throughs/kivy-tutorial/object-properties
#https://www.geeksforgeeks.org/python-adding-image-in-kivy-using-kv-file/
#https://kivy.org/doc/stable/guide/packaging.html
#https://www.tutorialspoint.com/kivy/kivy-images.htm
#https://kivy.org/doc/stable/api-kivy.uix.label.html
#https://kivy.org/doc/stable/api-kivy.core.text.html
#https://kivy.org/doc/stable-2.2.0/api-kivy.uix.button.html


from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '1024')

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from random import randint

from time import *
from time import sleep
import threading
import time



#IMPORTANT STUFF
#GPIO.setwarnings(False)

#SETUP
#ledred = [5, 22, 27]
#ledgreen = [26, 19, 13]
#TRIG = [24, 23, 18]
#ECHO = [21, 20, 16]

speed_of_sound = 343.0


print("Distance in measurement")

#GPIO.setmode(GPIO.BMC)
#GPIO.setup(ledred, GPIO.OUT)
#GPIO.setup(ledgreen, GPIO.OUT)
#GPIO.setup(TRIG, GPIO.OUT)
#GPIO.setup(ECHO, GPIO.IN)

#import I2C_LCD_driver
#mylcd = I2C_LCD_driver.lcd()

class ParklaApp(App):
    def build(self):
        self.flo = FloatLayout()

        # Background Image
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
        # Log Section
        self.log_messages = []
        self.log_label = Label(
            text="Log sättib valmis...\n",
            halign='left',
            valign='top',
            size_hint=(1, None),
            text_size=(400, None)
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))

        log_scroll = ScrollView(
            size_hint=(0.4, 0.6),
            pos_hint={'x': 0.55, 'y': 0.3},
            do_scroll_x=False
        )
        log_scroll.add_widget(self.log_label)
        self.flo.add_widget(log_scroll)
        
        #MINI SETUP
        self.Parking_spaces = [False, False, False]
        self.Pi = [
            'C:/Users/veron/Ajaplaneerimine/blackcar.png',
            'C:/Users/veron/Ajaplaneerimine/blackcar.png',
            'C:/Users/veron/Ajaplaneerimine/blackcar.png'
            ]
        #PARKING LOTS
        self.PL = []
        for i in range(3):
            parking_lot = Image(
                source = self.Pi[i],
                size_hint = (0.3, 0.3),
                pos_hint = {"x": (i - 0.26) * 0.2, "y": 0.6},
                allow_stretch = True
            )
            self.flo.add_widget(parking_lot)
            self.PL.append(parking_lot)
        #BUTTONS
        for i in range(3):
            green_b = Button(
                background_normal = 'C:/Users/veron/Ajaplaneerimine/greenbutton.png',
                size_hint = (0.1, 0.1),
                pos_hint = {"x": 0.05 + i * 0.2, "y": 0.5},
            )
            self.flo.add_widget(green_b)
            red_b = Button(
                background_normal = 'C:/Users/veron/Ajaplaneerimine/redbutton.png',
                size_hint = (0.1, 0.1),
                pos_hint = {"x": 0.05 + i * 0.2, "y": 0.35},
            )
            self.flo.add_widget(red_b)
            black_b = Button(
                background_normal = 'C:/Users/veron/Ajaplaneerimine/blackbutton.png',
                size_hint = (0.1, 0.1),
                pos_hint = {"x": 0.05 + i * 0.2, "y": 0.2},
            )
            self.flo.add_widget(black_b)


        for i in range(3):
            threading.Thread(target=self.mp, args=(i,)).start()
            #Free_p_s_string = str(Free_parking_spaces) + " Parking spaces is free"
            #mylcd.lcd_display_string(Free_p_s_string, 1)
            #GPIO.cleanup()        
        return self.flo
        
    def mp (self, space_num):
        while(True):
            #setup
            #GPIO.output(trig, False)
            #print("waiting ", self.space_num, "\n")
            
            #GPIO.output(trig, True)
            #time.sleep(0.00001)
            #GPIO.output(trig, False)

            #while GPIO.input(echo)==0:
            #    pulse_start=time()
            #while GPIO.input(echo)==1:
            #    pulse_end=time.time()

            #pulse_duration = pulse_end-pulse_start
            #distance=(pulse_duration*speed_of_sound)/2
            #distance = round(distance*100)/2
            print("Ootan vastust... ")
            distance = randint(0, 30)
            status = self.p_checking(distance)
            Clock.schedule_once(lambda dt: self.ubuntu(space_num, status, distance))
            time.sleep(2)

    def p_checking(self, distance):
        if distance < 0 or distance >25:
            return "viga"
        elif distance <= 15:
            return "voetud"
        elif distance < 25:
            return "vaba"
        return "lol wtf"

    def ubuntu(self, space_num, status, distance):
        if status == "viga":
            m = f"Parkimise kohal {space_num + 1} in VIGA"
            self.PL[space_num].source = 'C:/Users/veron/Ajaplaneerimine/blackcar.png'
            #mylcd_display_string(f"Viga kohal{space_num + 1}")
            for i in range(5):
                #GPIO.output(led_r, True)
                #GPIO.output(led_g, True)
                i=i+1
        elif status == "voetud":
            m = f"Parkimise koht {space_num + 1} on võetud"
            self.PL[space_num].source = 'C:/Users/veron/Ajaplaneerimine/redcar.png'
            self.Parking_spaces[space_num] = False
        elif status == "vaba":
            m = f"Parkimise koht {space_num + 1} on vaba"
            self.PL[space_num].source = 'C:/Users/veron/Ajaplaneerimine/greencar.png'
            self.Parking_spaces[space_num] = True
        else:
            m= "Wtf"
        self.add_to_log(m)

    def add_to_log(self, message):
        fm = f"[b][color=#6E4B34]{message}[/color][/b]" #lisame teksti boldi ja värvime pruuniks
        self.log_messages.append(fm)
        self.log_label.text += fm + "\n" #lisame rea
        self.log_label.markup = True #enabling markup label-jaoks

if __name__ == '__main__': 
    ParklaApp().run()

