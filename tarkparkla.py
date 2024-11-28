from RPi import GPIO
from time import *
from time import sleep

import threading
import time
#I2C Libraries
import I2C_LCD_driver

GPIO.setwarnings(False)
#setup
ledred=[5,22,27]
ledgreen=[26,19,13]
TRIG=[24,23,18]
ECHO=[21,20,16]

print("Distance in measurement")

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledred, GPIO.OUT)
GPIO.setup(ledgreen, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
speed_of_sound = 343.0

Parking_spaces = [False, False, False]
mylcd = I2C_LCD_driver.lcd()

def parkla (space_num, parking_spaces, led_r, led_g, trig, echo):
  #setup
  GPIO.output(trig, False)
  print("waiting ", space_num, "\n")
  time.sleep(2)
  GPIO.output(trig, True)
  time.sleep(0.00001)
  GPIO.output(trig, False)

  while GPIO.input(echo)==0:
    pulse_start=time()
  while GPIO.input(echo)==1:
    pulse_end=time.time()

  pulse_duration = pulse_end-pulse_start
  distance=(pulse_duration*speed_of_sound)/2
  distance = round(distance*100)/2

  if distance < 0 or distance > 25: #display error when distance is smaller than 0 or bigger than 25cm
    print("error or car too close at parking space",space_num," car distance: ",distance,"cm/n")
    for i in range(5):
      GPIO.output(led_r, True)
      GPIO.output(led_g, True)
      sleep(0.2)
      i = i+1
      parking_spaces = False
      mylcd_display_string("Parking space error",2,"\n")
  
  if distance>0 and distance<25: #distance at the moment
    print("car distance at parking space ",space_num,":",distance,"cm\n")

if distance>0 and distance<15: #parking space occupied when 0-15cm distance
  print("parking space ",space_num," taken\n")
  GPIO.output(led_r, True)
  GPIO.output(led_g, False)
  sleep(1)
  parking_spaces = False

if distance>15 and distance<25: #parking space free when 15-25cm distance
  print("parking space ", space_num," is free")
  GPIO.output(led_r, False)
  GPIO.output(led_g, True)
  parking_spaces = True
  sleep(1)
return(0)
    
    
#Main code
if __name__=="__main__":
  while(True):
    t1=threading.Thread(target=parkla, args=(1, Parking_spaces[0], ledred[0], ledgreen[0], TRIG[0], ECHO[0]))
    t2=threading.Thread(target=parkla, args=(2, Parking_spaces[1], ledred[1], ledgreen[1], TRIG[1], ECHO[1]))
    t3=threading.Thread(target=parkla, args=(3, Parking_spaces[2], ledred[2], ledgreen[2], TRIG[2], ECHO[2]))

    t1.start()
    time.sleep(1)#et oleks lihtsam logi lugeda
    t2.start()
    time.sleep(2)#et oleks lihtsam logi lugeda
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    Free_parking_spaces = 0
    for i in Parking_spaces:
      if i == True:
        Free_parking_spaces += 1
    Free_p_s_string = str(Free_parking_spaces) + " Parking spaces is free"
    mylcd.lcd_display_string(Free_p_s_string, 1)
    
GPIO.cleanup()
