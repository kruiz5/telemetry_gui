from tkinter import *
import serial
import RPi.GPIO as GPIO
import time
import threading

    
class DashBoard(object):
    def _init_(self):
        self.root = None
        
        self.temp = 0         #
        self.gear = 0         #0=0, 1=r, 2=n, 3=d, 4=l
        self.voltage = 0      #56V max, 46V min; setting min threshold to 48V
        self.speed1 = ' '
        self.speed2 = 0
        
        self.label100 = None
        sel.label80 = None
        self.label60 = None
        self.label40 = None
        self.label20 = None
        self.labelBV = None
        
        self.labelSpeed = None
        self.labelMPH = None
        
        self.park = None
        self.reverse = None
        self.neutral = None
        self.drive= None
        self.low = None
        
        self.label100deg = None
        sel.label80deg = None
        self.label60deg = None
        self.label40deg = None
        self.label20deg = None
        
        self.Read_thread = None
        self.BatteryVoltage_thread = None
        self.Speed_thread = None
        self.BatteryTemperature_thread = None
        self.GearShift_thread = None
        
        
    def initScreen(self):
        self.root = Tk() #Create GUI window
        self.root.title("GUI Application") #set name of tkinter GUI window
        self.root.configure(background = "white") #set background color of GUI window
        self.root.geometry("600x350") #set configuration of GUI window

        self.label100 = Label(self.root, text = "       ", fg="green", bg="green")
        self.label80 = Label(self.root, text = "       ", fg="green", bg="green")
        self.label60 = Label(self.root, text = "       ", fg="green", bg="green")
        self.label40 = Label(root, text = "       ", fg="green", bg="green")
        self.label20 = Label(self.root, text = "       ", fg="green", bg="green")
        self.labelBV = Label(self.root, font= ('times', 10), bg = 'white')
        self.labelBV.config(text = 'Battery Voltage')
        self.label100.place(x=25, y=20)
        self.label80.place(x=25, y=40)
        self.label60.place(x=25, y=60)
        self.label40.place(x=25, y=80)
        self.label20.place(x=25, y=100)
        self.labelBV.place(x=23, y=120)
        
        self.speed1 = ''
        self.labelSpeed= Label(self.root, font=('times', 30, 'bold'), bg='white')
        self.labelSpeed.place(x = 150, y = 50)
        self.labelMPH = Label(self.root, font= ('times', 20), bg = 'white')
        self.labelMPH.place(x = 150, y = 100)
        self.labelMPH.config(text = 'MPH')


        self.park = Label(self.root, font= ('times', 15), bg = 'gray')
        self.park.config(text = 'P')
        self.park.place( x =100, y = 150)
        self.reverse = Label(self.root, font= ('times', 15), bg = 'white')
        self.reverse.config(text = 'R')
        self.reverse.place( x =120, y = 150)
        self.neutral = Label(self.root, font= ('times', 15), bg = 'white')
        self.neutral.config(text = 'N')
        self.neutral.place( x =140, y = 150)
        self.drive = Label(self.root, font= ('times', 15), bg = 'white')
        self.drive.config(text = 'D')
        self.drive.place( x =160, y = 150)
        self.low = Label(self.root, font= ('times', 15), bg = 'white')
        self.low.config(text = 'L')
        self.low.place( x =180, y = 150)

        self.label100deg = Label(self.root, text = "       ", fg="gray", bg="gray")
        self.label80deg = Label(self.root, text = "       ", fg="gray", bg="gray")
        self.label60deg = Label(self.root, text = "       ", fg="gray", bg="gray")
        self.label40deg = Label(self.root, text = "       ", fg="gray", bg="gray")
        self.label20deg = Label(self.root, text = "       ", fg="gray", bg="gray")
        self.labelBT = Label(self.root, font= ('times', 10), bg = 'white')
        self.labelBT.config(text = 'Battery Temperature')
        self.label100deg.place(x=300, y=20)
        self.label80deg.place(x=300, y=40)
        self.label60deg.place(x=300, y=60)
        self.label40deg.place(x=300, y=80)
        self.label20deg.place(x=300, y=100)
        self.labelBT.place(x=270, y=120)
        
        self.root.update_idletasks()
        self.root.update()
        
        
        def update_GearShift(self):
            #self.gear = int(ser.readline().strip())
            if (self.gear == 0):
                self.park.config(bg = 'gray')
                self.reverse.config(bg = 'white')
                self.neutral.config(bg = 'white')
                self.drive.config(bg = 'white')
                self.low.config(bg = 'white')
            elif (self.gear == 1):
                self.park.config(bg = 'white')
                self.reverse.config(bg = 'gray')
                self.neutral.config(bg = 'white')
                self.drive.config(bg = 'white')
                self.low.config(bg = 'white')
            elif (self.gear == 2):
                self.park.config(bg = 'white')
                self.reverse.config(bg = 'white')
                self.neutral.config(bg = 'gray')
                self.drive.config(bg = 'white')
                self.low.config(bg = 'white')
            elif (self.gear == 3):
                self.park.config(bg = 'white')
                self.reverse.config(bg = 'white')
                self.neutral.config(bg = 'white')
                self.drive.config(bg = 'gray')
                self.low.config(bg = 'white')
            elif (self.gear == 4):
                self.park.config(bg = 'white')
                self.reverse.config(bg = 'white')
                self.neutral.config(bg = 'white')
                self.drive.config(bg = 'white')
                self.low.config(bg = 'gray') 
            
            self.root.update_idletasks()
            self.root.update()
            
        def update_Voltage(sel):
            #self.voltage = int(ser.readline().strip())
            if (self.voltage >= 56):
                self.label100.config(bg = "green")
                self.label80.config(bg = "green")
                self.label60.config(bg = "green")
                self.label40.config(bg = "green")
                self.label20.config(bg = "green")
            elif (self.voltage < 56  and self.voltage >= 54):
                self.label100.config(bg = "gray")
                self.label80.config(bg = "green")
                self.label60.config(bg = "green")
                self.label40.config(bg = "green")
                self.label20.config(bg = "green")
            elif (self.voltage < 54 and self.voltage >= 52):
                self.label100.config(bg = "gray")
                self.label80.config(bg = "gray")
                self.label60.config(bg = "green")
                self.label40.config(bg = "green")
                self.label20.config(bg = "green")
            elif (self.voltage < 52 and self.voltage >= 50):
                self.label100.config(bg = "gray")
                self.label80.config(bg = "gray")
                self.label60.config(bg = "gray")
                self.label40.config(bg = "green")
                self.label20.config(bg = "green")
            elif (self.voltage < 50 and self.voltage >= 48):
                self.label100.config(bg = "gray")
                self.label80.config(bg = "gray")
                self.label60.config(bg = "gray")
                self.label40.config(bg = "gray")
                self.label20.config(bg = "green")
            elif ( self.voltage < 48 ):
                self.label100.config(bg = "gray")
                self.label80.config(bg = "gray")
                self.label60.config(bg = "gray")
                self.label40.config(bg = "gray")
                self.label20.config(bg = "gray")    
            
            self.root.update_idletasks()
            self.root.update()
            
        def update_Temperature(self):
            #self.temp = int(ser.readline().strip())        
            if (self.temp > 800):
                self.label100deg.config(bg = "red")
                self.label80deg.config(bg = "red")
                self.label60deg.config(bg = "red")
                self.label40deg.config(bg = "red")
                self.label20deg.config(bg = "red")
            elif (temp<= 800 and temp>600):
                self.label100deg.config(bg = "gray")
                self.label80deg.config(bg = "yellow")
                self.label60deg.config(bg = "yellow")
                self.label40deg.config(bg = "yellow")
                self.label20deg.config(bg = "yellow")
            elif (temp<=600 and temp>400):
                self.label100deg.config(bg = "gray")
                self.label80deg.config(bg = "gray")
                self.label60deg.config(bg = "green")
                self.label40deg.config(bg = "green")
                self.label20deg.config(bg = "green")
            elif (temp<=400 and temp>200):
                self.label100deg.config(bg = "gray")
                self.label80deg.config(bg = "gray")
                self.label60deg.config(bg = "gray")
                self.label40deg.config(bg = "blue")
                self.label20deg.config(bg = "blue")
            elif (temp<=200 and temp>50):
                self.label100deg.config(bg = "gray")
                self.label80deg.config(bg = "gray")
                self.label60deg.config(bg = "gray")
                self.label40deg.config(bg = "gray")
                self.label20deg.config(bg = "blue")
            elif (temp<=50):
                self.label100deg.config(bg = "gray")
                self.label80deg.config(bg = "gray")
                self.label60deg.config(bg = "gray")
                self.label40deg.config(bg = "gray")
                self.label20deg.config(bg = "gray")
            
            self.root.update_idletasks()
            self.root.update()
                
        def update_Speed(self):
            #self.speed2 = int(ser.readline().strip())
            # if time string has changed, update it
            if self.speed2 != self.speed1:
                self.speed1 = self.speed2
                self.speed.config(text=self.speed2)
                
            self.root.update_idletasks()
            self.root.update()
            
        def start_Read(self):
            #read incoming serial data and assign to variables
            #for now focus on voltage, temp, and speed
            """
            self.gear =
            """
            data = int(ser.readline().strip())
            self.speed2 = data % 100
            self.temp = (data % 10000) - self.speed2
            self.voltage = data - (self.temp * 100) - self.speed2
            
            
        
        def start_thread(self):
            self.Read_thread = threading.Thread(target = self.start_Read, name = 'read data', args = ())
            self.Read_thread = setDaemon(True)
            self.Read_thread.start()
            
            self.BatteryVoltage_thread = threading.Thread(target = self.update_Speed, name = 'update Voltage', args = ())
            self.BatteryVoltage_thread = setDaemon(True)
            self.BatteryVoltage_thread.start()
            
            self.Speed_thread = threading.Thread(target = self.update_Voltage, name = 'update speed', args = ())
            self.Speed_thread = setDaemon(True)
            self.Speed_thread.start()
            
            self.BatteryTemperature_thread = threading.Thread(target = self.update_Temperature, name = 'update temperature', args = ())
            self.BatteryTemperature_thread = setDaemon(True)
            self.BatteryTemperature_thread.start()
        
            self.GearShift_thread = threading.Thread(target = self.update_GearShift, name = 'update speed', args = ())
            self.GearShift_thread = setDaemon(True)
            self.GearShift_thread.start()


if __name__ == '__main__':
    ser = serial.Serial("/dev/ttyUSB0", 9600) #change ACM number as found
    ser.baudrate = 9600
    GPIO.setmode(GPIO.BOARD)
    
    dash = DashBoard()
    dash.initScreen()
    
    while True:                
        dash.start_threads()
        
 