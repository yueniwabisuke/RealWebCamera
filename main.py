import cv2
import sys
#from mail import sendEmail
from flask import Flask, render_template, Response
from camera import VideoCamera
from flask_basicauth import BasicAuth
import time
import threading

#email_update_interval = 600 # sends an email only once in this time interval
video_camera = VideoCamera(flip=True) # creates a camera object, flip vertically
object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml") # an opencv classifier

# App Globals (do not edit)
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'nsw'
app.config['BASIC_AUTH_PASSWORD'] = 'ishida'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)
last_epoch = 0
kind_front = 1
cap = cv2.VideoCapture(0)

def check_for_objects():
	#global last_epoch
	while True:
		#frame, found_obj = video_camera.get_object(object_classifier)
		
		try:
			frame, found_obj = video_camera.get_object(object_classifier)
			#if fullbody_recognition_modeld_obj and (time.time() - last_epoch) > email_update_interval:
				#last_epoch = time.time()
				#print "Sending email..."
				#sendEmail(frame)
				#print "done!"
		except:
			#print "Error sending email: ", sys.exc_info()[0]
			pass
		

@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        check,frame1 = cap.read()
        frame = camera.get_frame(frame1,kind_front)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/kind',methods=['POST'])
def kind():
	if request.method == 'POST':
		global kind_front
		kind_front = request.form['kind']
		print(kind_front)

if __name__ == '__main__':
    """
    t = threading.Thread(target=check_for_objects, args=())
    t.daemon = True
    t.start()
    """
    app.run(host='0.0.0.0', debug=False)
