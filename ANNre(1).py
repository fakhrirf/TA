import cv2.cv as cv     # import libarary openCV
import time
#import pyfirmata           # import libarary serial
from sklearn.neural_network import MLPClassifier
from sklearn import neighbors, datasets
import pandas as pd
import Tkinter
import sys

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video",
#        help="path to the (optional) video file")
#ap.add_argument("-b", "--buffer", type=int, default=64,
#        help="max buffer size")
#args = vars(ap.parse_args())

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
##colorLower = (99, 115, 150)
##colorUpper = (110, 255, 255)
#pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
#if not args.get("video", False):
#        camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
#else:
#        camera = cv2.VideoCapture(args["video"])
#capture = cv2.VideoCapture(0)
capture = cv.CaptureFromCAM(0)
cv.SetCaptureProperty(capture,3,600)
cv.SetCaptureProperty(capture,4,300)
#capture.set (3,640)
#capture.set (4,480)


# setting port serial arduino ke komputer
#board = pyfirmata.Arduino('COM37')
#servo_1= board.get_pin('d:5:p')
#servo_2= board.get_pin('d:6:p')
#servo_3= board.get_pin('d:9:p')
#servo_4= board.get_pin('d:10:p')
#servo_5= board.get_pin('d:11:p')
#time.sleep(1)

#Database koordinatdan gerak servo
FileDB = 'database.csv'
Database = pd.read_csv(FileDB)
print(Database)

#Declartion: X = data, y = target
X = Database[[u'Feature1', u'Feature2']] #ciri1, ciri2, dst
y1 = Database.Target1 #maju M 50
y2 = Database.Target2 #Kiri I 60
y3 = Database.Target3 #Kanan A 70
#y4 = Database.Target4 #Berhenti B 80
#y5 = Database.Target5

#Classify and trainning
clf1 = MLPClassifier(solver='lbfgs', alpha=1e-5,
                     hidden_layer_sizes=(20, 20), random_state=1)
clf1.fit(X, y1)
clf2 = MLPClassifier(solver='lbfgs', alpha=1e-5,
                     hidden_layer_sizes=(20, 20), random_state=1)
clf2.fit(X, y2)
clf3 = MLPClassifier(solver='lbfgs', alpha=1e-5,
                     hidden_layer_sizes=(20, 20), random_state=1)
clf3.fit(X, y3)
#
#clf4 = MLPClassifier(solver='lbfgs', alpha=1e-5,
 #                    hidden_layer_sizes=(20, 20), random_state=1)
#clf4.fit(X, y4)
#clf5 = MLPClassifier(solver='lbfgs', alpha=1e-5,
 #                    hidden_layer_sizes=(20, 20), random_state=1)
#clf5.fit(X, y5)

while True:
        # grab the current frame
#        (grabbed, frame) = camera.read()
#        frame = cv2.flip(frame, 1)
 
        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
#        if args.get("video") and not grabbed:
#                break
 
        # resize the frame, inverted ("vertical flip" w/ 180degrees),
        # blur it, and convert it to the HSV color space
 #       frame = imutils.resize(frame, width=600)
 #       frame = imutils.rotate(frame, angle=360)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
  #      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
   #     mask = cv2.inRange(hsv, colorLower, colorUpper)
   #     mask = cv2.erode(mask, None, iterations=2)
   #     mask = cv2.dilate(mask, None, iterations=2)
        
        
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
   #     cnts =

        #cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        #        cv2.CHAIN_APPROX_SIMPLE)[-2]
    #    center = None
        img = cv.QueryFrame(capture)
        cv.Smooth(img,img,cv.CV_BLUR,3)
        hue_img = cv.CreateImage(cv.GetSize(img),8,3)
        cv.CvtColor(img,hue_img,cv.CV_BGR2HSV)
        threshold_img=cv.CreateImage(cv.GetSize(hue_img),8,1)
        cv.InRangeS(hue_img,(90,115,150),(110,255,255),threshold_img)
        storage = cv.CreateMemStorage(0)
        cnts = cv.FindContours(threshold_img,storage,cv.CV_RETR_CCOMP,\
                                      cv.CV_CHAIN_APPROX_SIMPLE)

        points = []
        while cnts:
                rect = cv.BoundingRect(list(cnts))
                #prediksi
                mode1=clf1.predict([rect[0], rect[1]])
                mode2=clf2.predict([rect[0], rect[1]])
                mode3=clf3.predict([rect[0], rect[1]])
                #angle1=clf1.predict([rect[0], rect[1]])
                #angle2=clf2.predict([rect[0], rect[1]])
                #angle3=clf3.predict([rect[0], rect[1]])
                #angle4=clf4.predict([rect[0], rect[1]])
                #angle5=clf5.predict([rect[0], rect[1]])


                #print angle1, angle2, angle3, angle4, angle5
                print (mode1, mode2, mode3)
                teensy.write(mode1+"M".enconde())
                teensy.write(mode2+"A".enconde()) #
                teensy.write(mode3+"I".enconde())
                teensy.write("80B".enconde())

        
        #gerak robot arm
        #duty5 = float(angle5) / 18.0
        #servo_5.write(duty5)
        #duty1 = float(angle1) / 18.0
        #servo_1.write(duty1)
        #duty3 = float(angle3) / 18.0
        #servo_3.write(duty3)
        #duty2 = float(angle2) / 18.0
        #servo_2.write(duty2)
        #duty4 = float(angle4) / 18.0
        #servo_4.write(duty4)
        
                cnts = cnts.h_next()
                size = (rect[2]*rect[3])
                if size > 100:
                    pt1 = (rect[0],rect[1])
                    pt2 = (rect[0]+rect[2],rect[1]+rect[3])
                    cv2.Rectangle(img,pt1,pt2,(38,160,60))

        cv2.imshow("Colour Tracking", frame)
        if cv2.waitKey(10)==27:
                break
