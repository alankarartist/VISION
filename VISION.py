from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
import os 
import sys 
import time 
import pyttsx3

class Vision(QMainWindow): 

	def __init__(self): 
		super().__init__() 
		self.setGeometry(100, 100, 
						800, 600) 
        
		self.setStyleSheet('background : black;\ncolor:white;\nfont: 75 12pt "LEMON MILK";') 
		self.availableCameras = QCameraInfo.availableCameras() 
		if not self.availableCameras: 
			sys.exit() 
		self.status = QStatusBar()
		self.status.setStyleSheet('background : black;\ncolor:white;\nfont: 75 12pt "LEMON MILK";') 
		self.setStatusBar(self.status) 
		self.savePath = os.getcwd()+'\Vision' 
		self.viewfinder = QCameraViewfinder() 
		self.viewfinder.show() 
		self.setCentralWidget(self.viewfinder) 
		self.selectCamera(0) 
		toolbar = QToolBar("CAMERA TOOL BAR") 
		self.addToolBar(toolbar) 
		clickAction = QAction("CLICK PHOTO", self) 
		clickAction.setStatusTip("PICTURE WILL BE CAPTURED") 
		clickAction.setToolTip("CAPTURE PICTURE") 
		clickAction.triggered.connect(self.clickPhoto) 
		toolbar.addAction(clickAction) 
		changeFolderAction = QAction("CHANGE SAVE LOCATION", 
									self) 
		changeFolderAction.setStatusTip("FOLDER LOCATION WHERE PICTURE WILL BE SAVED") 
		changeFolderAction.setToolTip("CHANGE SAVE LOCATION") 
		changeFolderAction.triggered.connect(self.changeFolder) 
		toolbar.addAction(changeFolderAction) 
		cameraSelector = QComboBox() 
		cameraSelector.setStatusTip("CHOOSE CAMERA TO TAKE PICTURES") 
		cameraSelector.setToolTip("SELECT CAMERA") 
		cameraSelector.setToolTipDuration(2500) 
		cameraSelector.addItems([camera.description() 
								for camera in self.availableCameras]) 
		cameraSelector.currentIndexChanged.connect(self.selectCamera) 
		toolbar.addWidget(cameraSelector) 
		toolbar.setStyleSheet('QToolTip { background-color: black; color: white; border: black solid 1px }\nbackground : black;\ncolor:white;\nfont: 75 12pt "LEMON MILK";')
		toolbar.setMovable(False)
		self.setWindowTitle("VISION") 
		self.show() 

	def speak(self,audio):
            engine = pyttsx3.init('sapi5')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            engine.say(audio)
            engine.runAndWait()

	def selectCamera(self, i): 
		self.camera = QCamera(self.availableCameras[i]) 
		self.camera.setViewfinder(self.viewfinder) 
		self.camera.setCaptureMode(QCamera.CaptureStillImage) 
		self.camera.error.connect(lambda: self.alert(self.camera.errorString())) 
		self.camera.start() 
		self.capture = QCameraImageCapture(self.camera) 
		self.capture.error.connect(lambda error_msg, error, 
								msg: self.alert(msg)) 
		self.capture.imageCaptured.connect(lambda d, 
										i: self.status.showMessage("IMAGE CAPTURED : "
																	+ str(self.saveSeq))) 
		self.currentCameraName = self.availableCameras[i].description() 
		self.saveSeq = 0

	def clickPhoto(self): 
		timestamp = time.strftime("%d-%b-%Y-%H_%M_%S") 
		self.capture.capture(os.path.join(self.savePath, "%s-%04d-%s.jpg" % ( 
			self.currentCameraName, 
			self.saveSeq, 
			timestamp 
		))) 
		self.saveSeq += 1
		self.speak('Image has been saved.')

	def changeFolder(self): 
		path = QFileDialog.getExistingDirectory(self, "PICTURE LOCATION", "") 
		if path: 
			self.savePath = path 
			self.saveSeq = 0

	def alert(self, msg): 
		error = QErrorMessage(self) 
		error.showMessage(msg.upper()) 
		error.setWindowTitle("VISION ERROR")

if __name__ == "__main__" : 
    App = QApplication(sys.argv) 
    window = Vision() 
    sys.exit(App.exec()) 