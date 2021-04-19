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


@app.route("/<server>/<action>")
def serverControll(server, action):
    if server == 'server':
        if action == 'start':
            print("server.start")
            lgserver.run()
            serverStatus = lgserver.server_is_running
        elif action == 'stop':
            print("server.stop")
            lgserver.stop()
            serverStatus = lgserver.server_is_running
        
        
    templateData = {
      		'Serverstatus'  : serverStatus
      	}

    return render_template('index.html', **templateData)      
         

@app.route("/calibration")
def calibration():

    return render_template('calibration.html')

@app.route("/calibration/<action>")
def startCalibration(action):

    if action == 'start':
        print("starting calibration")
        lgserver.start_calibration()
    if action == 'stop':
        print("stopping calibration")
        lgserver.stop_calibration()    

    return render_template('calibration.html')    

@app.route("/test")
def testingSite():

    return render_template('test.html')


if __name__ == "__main__":
    app.run()