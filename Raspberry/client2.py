#rasberry 192.168.1.152 
#pc       192.168.1.202

import socket
import threading
from pynput.mouse import Button, Controller
import time

#Defaults 
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.152"
ADDR = (SERVER, PORT)

CHECKSUM = "69"
REGUERST_MOUSE_MOVEMENT = "Mouse"
MOUSE_DATA_LENGTH = 32


class Client:

    ErrorLog = {
        "recv_errors" : 0
    }

    def __init__(self):
        self._is_running = False
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.mouse_btn_state = 0
        self.mouse = Controller()
        self.recv_count = 0
        self.recv_count_mouse = 0
        self.last_mouse_position = self.mouse.position
        self.new_mouse_position = self.last_mouse_position

    def move_mouse(self,data_string):
         # to send "checksum, , resolution_horizontal, resolution_vertical  mouseclick"
        #mousepressed = 0/1
        # Button.left	
        #dx (int) – The horizontal offset.
        #dy (int) – The vertical offset.
        mouse_press = self.mouse_btn_state
        #print(data_string) #debug
        #print("\n") #debug
        
        if data_string.startswith(CHECKSUM):
            self.recv_count = self.recv_count + 1
            data = data_string.split(",")
            if (len(data) == 4):
                try:
                    #print(data_string)
                    self.recv_count_mouse = self.recv_count_mouse + 1                  
                    self.new_mouse_position = int(data[1]), int(data[2])  #horizontal vertical
                    if self.new_mouse_position != self.last_mouse_position:
                        self.mouse.position = self.new_mouse_position
                        self.last_mouse_position = self.new_mouse_position
                
                    mouse_press = int(data[3])
                    if mouse_press != self.mouse_btn_state:
                        if mouse_press == 1:
                            self.mouse.press(Button.left)
                        else:
                            self.mouse.release(Button.left)
                except TypeError:
                    print("Type-error")

        self.mouse_btn_state = mouse_press

    def stop(self):
        self._is_running = False

    def run(self):
        thread = threading.Thread(target=self.mouse_movement_thread, args=())
        print("thread start")
        thread.start()

    def mouse_movement_thread(self):
        self._is_running = True
        print("running")
        while(self._is_running):
            self.client.send(REGUERST_MOUSE_MOVEMENT.encode(FORMAT))
            datarecv = self.client.recv(MOUSE_DATA_LENGTH).decode(FORMAT)
            self.move_mouse(datarecv)

        print("stopd")
            
            

    def send(self,msg): ##UNUSED
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        #self.client.send(send_length)
        self.client.send(message)
        #print(self.client.recv(2048).decode(FORMAT))          #vastaanotto

    def recv(self): ##UNUSED
        msg = "asdas"
        message = msg.encode(FORMAT)
        print("sending")
        self.client.send(message)
        datarecv = self.client.recv(2048).decode(FORMAT)
        self.move_mouse(datarecv)
        print("recived")


client = Client()

client.run()

print("Press ENTER to stop Client")
input()
client.stop()
print(client.recv_count)
print(client.recv_count_mouse)
print(str(client.ErrorLog))

client.send(DISCONNECT_MESSAGE)

