#rasberry 192.168.1.152 
#pc       192.168.1.202

# to send "checksum, resolutino_vertical, resolution_horizontal, mouseclick"

import socket 
import threading
import lighteless_gun_controller

HEADER = 64
PORT = 5050
SERVER = "192.168.1.152"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

CHECKSUM = "69"
REGUERST_MOUSE_MOVEMENT = "Mouse"
MOUSE_DATA_LENGTH = 32


class Lighteless_gun_server:
    
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.server_is_running = False
        self.send_count = 0

        self.gun = lighteless_gun_controller.Lightless_gun_controller() #open controller

    def run(self):
        print("[STARTING] server is starting...")
        self.server_is_running = True
        thread = threading.Thread(target=self.server_thread, args=())
        thread.start()

    def stop(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.client.send(DISCONNECT_MESSAGE.encode())
        self.server_is_running = False   

    def server_thread(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while self.server_is_running:
            conn, addr = self.server.accept() ## blokkaaava
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")


    def handle_client(self,conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected and self.server_is_running:
            msg = conn.recv(MOUSE_DATA_LENGTH).decode(FORMAT)
            #print("recv")
            #print(f"[{addr}] {msg}")
            if msg == REGUERST_MOUSE_MOVEMENT:
                self.send_count = self.send_count + 1
                #
                datastring = CHECKSUM + "," + self.gun.get_mouse_movement() 
                #               
                conn.send(datastring.encode(FORMAT))
            if msg == DISCONNECT_MESSAGE:
                connected = False
        conn.close()
        print(self.send_count)
        self.send_count = 0


    def start_calibration(self, resolution_horizontal = 1920, resolution_vertical = 1080):
        if self.server_is_running:
            self.stop()  ## stop server while calibrating
        self.gun.start_calibration(resolution_vertical = resolution_vertical,resolution_horizontal = resolution_horizontal)
        ##print(str(self.gun.calibration_data))
          

    def calibration_status(self):
        if hasattr(self.gun, 'calibration_status'):
            return self.gun.calibration_status
        else:
             return 69    
    def stop_calibration(self):
        self.gun.stop_calibration()

    
