import cv2
#from imutils.video.pivideostream import PiVideoStream
#import imutils
import time
import numpy as np

class VideoCamera(object):
    def __init__(self, flip = False):
        #self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)
        

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self,frame,kind=1):
        if(kind==0):
            detector = cv2.ORB_create()
            keypoints = detector.detect(frame)
            frame = cv2.drawKeypoints(frame,keypoints,None)
        elif(kind==1):
            cascade = cv2.CascadeClassifier("models/facial_recognition_model.xml") # an opencv classifier
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))
            for (x, y, w, h) in face:
                cv2.rectangle(frame, (x, y), (x + w, y+h), (0,0,200), 3)
        else:
        	pass
        
        ret, jpeg = cv2.imencode('.jpg',frame)
        return jpeg.tobytes()

    def get_object(self, classifier):
        found_objects = False
        frame = self.flip_if_needed(self.vs.read()).copy() 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        objects = classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        #objects = classifier.detectMultiScale(gray)
        if len(objects) > 0:
            found_objects = True

        # Draw a rectangle around the objects
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return (jpeg.tobytes(), found_objects)


