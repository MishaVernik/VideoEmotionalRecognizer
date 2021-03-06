import os

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QHBoxLayout, QProgressBar
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from imutils import face_utils
import dlib
import cv2
import sys
from random import randrange
from PyQt5 import QtCore, QtGui, QtWidgets


# landmarks on this detected face
class Recognizer:
    '''
        @method: __init__
            @__init__ : initialize data to the class Recognizer
        @params: path, progressBar
            @path : OS system path to the project (or to the file main.py)
            @progressBar : object that contains UI progressBar
    '''

    def __init__(self, path, progressBar):

        self.path = path
        self.progressBar = progressBar

    '''
        @method: recognize_frames
            @recognize_frames : receives before generated shape_predictor_68_face_landmarks.dat + takes 
            haarcascade_frontalface_alt2.xml to recognize 68 points on the face.               
    '''

    def recognize_frames(self):
        try:

            self.number_of_all_frames = self.count_frames_manual(self.path)
            print(self.number_of_all_frames)
            face_cascade = cv2.CascadeClassifier('venv/Lib/site-packages/cv2/data/haarcascade_frontalface_alt2.xml')
            # p = our pre-treined model directory, on my case, it's on the same script's diretory.
            self.p = "shape_predictor_68_face_landmarks.dat"
            self.detector = dlib.get_frontal_face_detector()
            self.predictor = dlib.shape_predictor(self.p)

            self.cap = cv2.VideoCapture(self.path)
            self.cnt = 0
            if self.cap.isOpened() == False:
                print("Error opening video stream or file")

            if 1:
                while self.cap.isOpened():# Getting out image bx y webcam
                    self._, self.image = self.cap.read()
                    self.tmp_image = self.image
                    # Converting the image to gray scale
                    self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                    # Get faces into webcam's image
                    self.rects = self.detector(self.gray, 0)
                    # For each detected face, find the landmark.

                    # Getting out image bx y webcam
                    # Converting the image to gray scale
                    # Get faces into webcam's image
                    # For each detected face, find the landmark.
                    self.face = 0
                    print(self.rects)
                    for (i, rect) in enumerate(self.rects):
                        # Make the prediction and transfom it to numpy array
                        shape = self.predictor(self.gray, rect)
                        shape = face_utils.shape_to_np(shape)
                        top = 99999
                        bot = 0
                        left = 99999
                        right = 0
                        for (x, y) in shape:
                            top = min(y, top)
                            bot = max(y, bot)
                            left = min(x, left)
                            right = max(x, right)

                        right += 20
                        left -= 20
                        top -= 20
                        bot += 20

                        while (right - left) / (bot - top) > 3 / 4:
                            top -= 1
                            bot += 1

                        cv2.rectangle(self.image, (left, top), (right, bot), (255, 0, 0), 2)

                        w = right - left
                        h = bot - top

                        # cv2.rectangle(image, (x, y), (end_cord_x_width, end_cord_y_height), color, stroke)

                        face = self.image[top:bot, left:right]

                        # Show the image
                        # cv2.imshow("Output", face)
                        prev_x = 0
                        prev_y = 0
                        if self.cnt % 10 == 0:

                            cv2.imwrite("data/photos/" + str(self.cnt) + ".png", face)

                            w = right - left
                            h = bot - top
                            with open("data/coordinates/" + str(self.cnt) + ".txt", "w") as o:
                                '''
                                    Points that define whole face of dots: 
                                        Jawline  : [1 - 17]
                                        Eyes     : [37 - 42] (left-eye)
                                        Eyes     : [43 - 48] (right-eye) 
                                        Eyebrows : [18 - 22] (left-eyebrow)
                                        Eyebrows : [23 - 27] (right-eyebrow)
                                        Nose     : [28 - 36]
                                        Mouth    : [49 - 68]                              
                                '''
                                point_counter = 1

                                introduction_label = True
                                prev_point_x = -1
                                prev_point_y = -1
                                color_state = (255, 255,0);
                                for (x, y) in shape:
                                    if 1 <= point_counter <= 17 and introduction_label == True:
                                        introduction_label = False
                                        prev_point_x = -1
                                        prev_point_y = -1
                                        o.write("\nJawLine\n (")
                                        color_state = (255, 255, 0)
                                    elif 18 <= point_counter <= 22 and introduction_label == False:
                                        introduction_label = True
                                        prev_point_x = -1
                                        prev_point_y = -1
                                        o.write(")\nLeft-eyebrow\n (")
                                        color_state = (0, 76, 153)
                                    elif 23 <= point_counter <= 27 and introduction_label == True:
                                        introduction_label = False
                                        prev_point_x = -1
                                        prev_point_y = -1
                                        o.write(")\nRight-eyebrow\n (")
                                        cv2.circle(self.image, (x, y), 2, (0, 76, 153), -1)
                                        color_state = (0, 76, 153)
                                    elif 28 <= point_counter <= 36 and introduction_label == False:
                                        introduction_label = True
                                        prev_point_x = -1
                                        prev_point_y = -1
                                        o.write(")\nNose\n (")
                                        color_state = (255, 51, 51)
                                    elif 37 <= point_counter <= 42 and introduction_label == True:
                                        introduction_label = False
                                        prev_point_x = -1
                                        prev_point_y = -1
                                        o.write(")\nLeft-eye\n (")
                                        color_state = (204, 204, 0)
                                    elif 43 <= point_counter <= 48 and introduction_label == False:
                                        introduction_label = True
                                        prev_point_x = -1
                                        prev_point_y = -1
                                        o.write(")\nRight-eye\n (")
                                        color_state = (204, 204, 0)
                                    elif 49 <= point_counter <= 68 and introduction_label == True:
                                        introduction_label = False
                                        prev_point_x = -1
                                        prev_point_y = -1
                                        o.write(")\nMouth\n (")
                                        color_state = (0, 255, 0)
                                    # Printing dots
                                    # Important!!
                                    # x and y are the points of the original picture
                                    # so that, they look like (543, 211) instead of
                                    # new_x and new_y = (0,12312335; 0,381238323)
                                    # because new points normalized
                                    cv2.circle(self.image, (x, y), 2, color_state, -1)
                                    if prev_point_y != -1 and prev_point_x != -1:
                                        cv2.circle(self.image, (int((x + prev_x) / 2),  int((y + prev_y) / 2)), 2,
                                                   color_state, -1)
                                    if prev_point_x == -1 and prev_point_y == -1:
                                        prev_point_x = (x - left) / w
                                        prev_point_y = (y - top) / h
                                        prev_x = x
                                        prev_y = y
                                    else:
                                        # interpolating points
                                        o.write(',[' + str((prev_point_x + (x - left) / w) / 2) + " " + str(
                                            (prev_point_y + (y - top) / h) / 2) + "],")
                                        prev_point_x = (x - left) / w
                                        prev_point_y = (y - top) / h
                                        prev_x = x
                                        prev_y = y
                                    o.write('[' + str(((x - left) / w)) + " " + str(((y - top) / h)) + "]")

                                    point_counter += 1
                                    if point_counter == 68:
                                        o.write(')')


                            face = self.image[top:bot, left:right]
                            cv2.imwrite("data/dots/" + str(self.cnt) + ".png", face)
                    if int((100 * self.cnt) / self.number_of_all_frames) >= 100:
                        self.progressBar.setValue(100)
                    else:
                        self.progressBar.setValue(int(100 * self.cnt / self.number_of_all_frames) + 1)


                    self.cnt += 1

                    k = cv2.waitKey(5) & 0xFF
                    if k == 27:
                        break

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        cv2.destroyAllWindows()
        self.cap.release()

    '''
           @method: show_recognized_video
               @recognize_frames : shows generated video          
    '''

    def show_recognized_video(self):
        self.face_cascade = cv2.CascadeClassifier('venv/Lib/site-packages/cv2/data/haarcascade_frontalface_alt2.xml')
        # p = our pre-treined model directory, on my case, it's on the same script's diretory.
        self.p = "shape_predictor_68_face_landmarks.dat"
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.p)

        self.cap = cv2.VideoCapture(self.path)
        self.cnt = 0

        if self.cap.isOpened() == False:
            print("Error opening video stream or file")
        try:
            while self.cap.isOpened():
                # Getting out image bx y webcam
                self._, self.image = self.cap.read()
                # Converting the image to gray scale
                self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                # Get faces into webcam's image
                self.rects = self.detector(self.gray, 0)
                # For each detected face, find the landmark.
                self.face = 0
                print(self.rects)
                for (i, rect) in enumerate(self.rects):
                    # Make the prediction and transfom it to numpy array
                    shape = self.predictor(self.gray, rect)
                    shape = face_utils.shape_to_np(shape)
                    top = 99999
                    bot = 0
                    left = 99999
                    right = 0
                    for (x, y) in shape:
                        top = min(y, top)
                        bot = max(y, bot)
                        left = min(x, left)
                        right = max(x, right)

                    right += 20
                    left -= 20
                    top -= 20
                    bot += 20

                    while (right - left) / (bot - top) > 3 / 4:
                        top -= 1
                        bot += 1

                    # cv2.rectangle(self.image, (left, top), (right, bot), (255, 0, 0), 2)

                    # Draw on our image, all the found cordinate points (x,y)
                    for (x, y) in shape:
                        cv2.circle(self.image, (x, y), 2, (0, 255, 0), -1)

                        # cv2.rectangle(image, (x, y), (end_cord_x_width, end_cord_y_height), color, stroke)

                    # face = self.image[top:bot, left:right]

                    # Show the image

                self.cnt += 1
                cv2.imshow("Output", self.image)

                k = cv2.waitKey(5) & 0xFF
                if k == 27:
                    break
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)

        cv2.destroyAllWindows()
        self.cap.release()

    '''
        @method: count_frames_manual
            @count_frames_manual : counts all frames in the video to define 100 % progress bar line 
        @params: path
            @path : OS system path to the project (or to the file main.py)             
    '''

    def count_frames_manual(self, path):
        video = cv2.VideoCapture(path)
        cnt = 0
        if video.isOpened() == False:
            print("Error opening video stream or file")
        # initialize the total number of frames read
        total = 0
        # loop over the frames of the video
        while True:
            # grab the current frame
            (grabbed, frame) = video.read()

            # check to see if we have reached the end of the
            # video
            if not grabbed:
                break

            # increment the total number of frames read
            total += 1

        # return the total number of frames in the video file
        return total


class UIapp(QWidget):

    def __init__(self):
        super().__init__()
        self.path = ""
        self.initUI()

    def start(self):
        recognizer = Recognizer(self.path, self.pbar)
        recognizer.recognize_frames()

    def show_video(self):
        recognizer = Recognizer(self.path, self.pbar)
        recognizer.show_recognized_video()
        print(1)

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "QFileDialog.getOpenFileName()",
                                                  "",
                                                  "All Files (*);;Video Files (*.mp4)",
                                                  options=options)
        if fileName:
            print(fileName)
            self.path = fileName

    def initUI(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(120, 300, 400, 35)

        self.setGeometry(300, 300, 600, 420)
        self.setWindowTitle('eMotion video recogNizer')
        self.setWindowIcon(QIcon('icon.jpg'))
        # Button Show video
        qbtnSelectShowVideo = QPushButton('Show video', self, objectName="GreenButton", minimumHeight=48)
        qbtnSelectShowVideo.clicked.connect(self.show_video)
        qbtnSelectShowVideo.resize(qbtnSelectShowVideo.sizeHint())
        qbtnSelectShowVideo.move(370, 100)
        # Button Select file
        qbtnSelectFile = QPushButton('Select file', self, objectName="GreenButton", minimumHeight=48)
        qbtnSelectFile.clicked.connect(self.openFile)
        qbtnSelectFile.resize(qbtnSelectFile.sizeHint())
        qbtnSelectFile.move(270, 200)
        # Button Start
        qbtnStart = QPushButton('Start', self, objectName="GreenButton", minimumHeight=48)
        qbtnStart.clicked.connect(self.start)
        qbtnStart.resize(qbtnStart.sizeHint())
        qbtnStart.move(270, 150)
        # Button Quit
        qbtnQuit = QPushButton('Quit', self, objectName="GreenButton", minimumHeight=48)
        qbtnQuit.clicked.connect(QCoreApplication.instance().quit)
        qbtnQuit.resize(qbtnQuit.sizeHint())
        qbtnQuit.move(270, 250)
        layout = QHBoxLayout(self)
        layout.addWidget(qbtnSelectFile)
        layout.addWidget(qbtnStart)
        layout.addWidget(qbtnQuit)
        layout.addWidget(qbtnSelectShowVideo)

        self.show()


StyleSheet = '''
MainWindow {
        background-image: url("icon.jpg"); 
        background-repeat: no-repeat; 
        background-position: center;
}
QPushButton {
    border: none;
}
QPushButton#RedButton {
    background-color: #f44336;
}
#RedButton:hover {
    background-color: #e57373; 
    color: #fff;
}
#RedButton:pressed { 
    background-color: #ffcdd2; 
}
#GreenButton {
    background-color: #4caf50;
    border-radius: 5px;       
}
#GreenButton:hover {
    background-color: #81c784;
    color: #fff;              
}
#GreenButton:pressed {
    background-color: #c8e6c9;
}
#BlueButton {
    background-color: #2196f3;
    min-width:  96px;
    max-width:  96px;
    min-height: 96px;
    max-height: 96px;
    border-radius: 48px;        
}
#BlueButton:hover {
    background-color: #64b5f6;
}
#BlueButton:pressed {
    background-color: #bbdefb;
}
#OrangeButton {
    max-height: 48px;
    border-top-right-radius:   20px;   
    border-bottom-left-radius: 20px;   
    background-color: #ff9800;
}
#OrangeButton:hover {
    background-color: #ffb74d;
}
#OrangeButton:pressed {
    background-color: #ffe0b2;
}

QPushButton[text="purple button"] {
    color: white;                    
    background-color: #9c27b0;
}
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    ex = UIapp()
    sys.exit(app.exec_())
    # video_recognizer = Recognizer()
