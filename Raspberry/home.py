from flask import Flask, render_template, request
import Lightless_gun_server

app = Flask(__name__)

serverStatus = 0

lgserver = Lightless_gun_server.Lighteless_gun_server() 

@app.route("/")
def index():

    serverStatus = lgserver.server_is_running 
    serverStatus = 0

    templateData = {
      	'Serverstatus'  : serverStatus
      	}
    return render_template('index.html', **templateData)


@app.route("/<controll>/<action>")
def serverControll(controll, action):
    if controll == 'server':
        if action == 'start':
            print("server.start")
            lgserver.run()
        elif action == 'stop' and lgserver.server_is_running:
            print("server.stop")
            lgserver.stop()
            
        
    if controll == 'calibration':
        if action == 'start':
            print("starting calibration")
            lgserver.start_calibration()
        if action == 'stop':
            print("stopping calibration")
            lgserver.stop_calibration() 

    serverStatus = lgserver.server_is_running           
                
    templateData = {
      		'Serverstatus'  : serverStatus
      	}



    return render_template('index.html', **templateData)      
         


if __name__ == "__main__":
    app.run(host="192.168.1.152")