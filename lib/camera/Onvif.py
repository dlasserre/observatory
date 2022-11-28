import cv2
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from onvif import ONVIFCamera


class QWidgetCameraONVIF:
    """ SIZE CAMERA WINDOW"""
    def __init__(self, ip: str, login: str, password: str, port: int = 2020, wsdl: str = None):
        self.ip = ip
        self.login = login
        self.password = password
        self.port = port
        self.wsdl = wsdl


class Camera:
    """ ONVIF CAMERA """

    def __init__(self, ip: str, login: str, password: str, port: int = 2020, wsdl: str = ''):
        self.login = login
        self.password = password
        self.ip = ip
        self.camera = ONVIFCamera(self.ip, port, self.login, self.password, wsdl)
        media_service = self.camera.create_media_service()
        self.profiles = media_service.GetProfiles()
        self.token = self.profiles[0].token
        self.stream = cv2.VideoCapture('rtsp://'+self.login+':'+self.password+'@'+self.ip+':554/stream1')

    def get_default_profile(self):
        return self.profiles

    def get_stream(self):
        ret, frame = self.stream.read()
        return ret, frame

    def get_camera(self):
        return self.camera

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(800, 600, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
