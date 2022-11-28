from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from lib.camera.Onvif import Camera, QWidgetCameraONVIF
from gui.utilities.Label import Label


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, ip: str, login: str, password: str, port: int = 2020, wsdl: str = None):
        super().__init__()
        self._run_flag = True
        self.camera = Camera(ip, login, password, port, wsdl)

    def run(self):

        while self._run_flag:
            ret, cv_img = self.camera.get_stream()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        self.camera.get_camera().release()


class QWidgetCameraSize:
    """ SIZE CAMERA WINDOW"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


class CameraStream(QWidget):
    def __init__(self, camera: QWidgetCameraONVIF, size: QWidgetCameraSize):
        super().__init__()
        self.setWindowTitle("Camera")
        self.display_width = size.width
        self.display_height = size.height
        self.image_label = Label()
        self.image_label.resize(self.display_width, self.display_height)
        self.thread = VideoThread(camera.ip, camera.login, camera.password, camera.port, camera.wsdl)
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        self.setLayout(vbox)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
