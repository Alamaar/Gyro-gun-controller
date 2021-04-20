import serial
import re
import string
import ast
import json
import pynput
import time
import threading

FORMAT = 'utf-8'

class Lightless_gun_controller:

    calibration_data = {  #default values
    "-vertical" : -50,
    "+vertical" : +50,
    "-horizontal" : +50,
    "+horizontal" : -50,
    "vertical_res" : 1920,
    "horizontal_res" : 1080
    }

    def __init__(self):
        self.setup()

    def remap(self, x, oMin, oMax, nMin, nMax ):
        ## 0.00000762551 avg time
        # add out off range option here or somewhere
        #
        #check reversed input range
        reverseInput = False
        oldMin = min( oMin, oMax )
        oldMax = max( oMin, oMax )
        if not oldMin == oMin:
            reverseInput = True

        #check reversed output range
        reverseOutput = False   
        newMin = min( nMin, nMax )
        newMax = max( nMin, nMax )
        if not newMin == nMin :
            reverseOutput = True

        portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
        if reverseInput:
            portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

        result = portion + newMin
        if reverseOutput:
            result = newMax - portion

        return result

    #
    def convertToPix(self,horizontal,vertical):
        horizontal = self.remap(horizontal,self.calibration_data["-horizontal"],self.calibration_data["+horizontal"],0,self.calibration_data["horizontal_res"])
        vertical = self.remap(vertical,self.calibration_data["-vertical"],self.calibration_data["+vertical"],0,self.calibration_data["vertical_res"])
        return horizontal, vertical
    #
    def get_Calibration_Data(self):
        try:
            data = open("Calibration_data")
            temp = str(data.read())
            self.calibration_data = ast.literal_eval(temp)  
            data.close()   
        except:
            print("Error getting calibration data")    
    #
    def run(self):
        pass

    def setup(self):
        while True:
            try:
                self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=3)
                self.ser.flush()
                time.sleep(0.5)
                break
            except:
                print("Error getting serial port")
                time.sleep(2)   
            self.get_Calibration_Data()     

    def get_mouse_movement(self):
         #to send "checksum,  resolution_horizontal, resolution_vertical,  mouseclick"
         while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode(FORMAT)
                if line.startswith(":"):
                    data = line.split(",")
                    if len(data) == 5:
                        roll = int(data[1])
                        pitch = int(data[2])
                        yawn = int(data[3])
                        mClick = int(data[4])
                        print(yawn)
                        print(pitch)
                        print("-")
                        horizontal, vertical = self.convertToPix(yawn, pitch)
                        datastring = f"{horizontal:.0f},{vertical:.0f},{mClick}"
                        print(datastring)                     
                        return datastring
                        break

    def get_mouse_movement_new(self):

         data_list = self.get_raw_sensor_data() ##[roll, pitch, yawn, mClick]
         horizontal, vertical = self.convertToPix(data_list[2], data_list[1])
         datastring = f"{horizontal:.0f},{vertical:.0f},{data_list[3]}"  
         return datastring

    def get_raw_sensor_data(self): ##[roll, pitch, yawn, mClick]
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode(FORMAT)
                if line.startswith(":"):
                    data = line.split(",")
                    if len(data) == 5:
                        roll = int(data[1])
                        pitch = int(data[2])
                        yawn = int(data[3])
                        mClick = int(data[4])  

                        data_list = [roll, pitch, yawn, mClick]
                        return data_list
                        break             
    
    def start_calibration(self, resolution_vertical = 1920 , resolution_horizontal = 1080):
        ##start calibration routine for the controller, user has to point 4 corners of the screen 
        ## and press the trigger in sequency to going from upper left counter-clockwise
        self.calibration_status = 0

        self.calibration_data["vertical_res"] = resolution_vertical
        self.calibration_data["horizontal_res"] = resolution_horizontal

        self.thread = threading.Thread(target=self.calibration_routine, args=())
        self.thread.start()

    def stop_calibration(self):
        self.calibration_status =  69
        self.thread.join()

    def calibration_routine(self):

        calibration_data_list = []  ##[0]---[3]
                                    ##---------  
                                    ##[1]---[2]   <-- screen
                            ##raw data = [roll, pitch, yawn, mClick]  
        mouse_flag = 0
        while self.calibration_status < 4:
            raw_data = self.get_raw_sensor_data()
            ##print(raw_data)

            if raw_data[3] == 1 and mouse_flag == 0:
                mouse_flag = 1
                ## save raw data to calib data list
                calibration_data_list.insert(self.calibration_status,raw_data)
                print(raw_data)

            if mouse_flag == 1 and raw_data[3] == 0:
                ## move to next iteration...
                mouse_flag = 0
                self.calibration_status = self.calibration_status + 1
                #time.sleep(0.5)  ##litle wait time maybe not needed        
        ##end while

        #take two values and calculate avrg
        if self.calibration_status == 4:   ## only go if no external interupst to calibration routine    
            self.calibration_data["-vertical"] = -(calibration_data_list[0][2] + calibration_data_list[1][2]) / 2
            self.calibration_data["+vertical"] = -(calibration_data_list[2][2] + calibration_data_list[3][2]) / 2
            self.calibration_data["-horizontal"] = (calibration_data_list[1][1] + calibration_data_list[2][1]) / 2
            self.calibration_data["+horizontal"] = (calibration_data_list[0][1] + calibration_data_list[3][1]) / 2

            # write calib data to file....
            self.write_Calibration_Data()
        else:
            print("Calibration failed")

    def write_Calibration_Data(self):
        try:
            data = open("Calibration_data","w") 
            data.write(str(self.calibration_data))
            data.close()
        except:
            print("Error writing file")    



if __name__ == '__main__':
    pass



                            