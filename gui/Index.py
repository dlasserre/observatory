from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from gui.Camera import CameraStream, QWidgetCameraSize
from lib.camera.Onvif import QWidgetCameraONVIF
from lib.ipx800.Ipx800 import Ipx800


class Index(QMainWindow):
    """ INDEX """
    _wsdl = 'C:\\Users\\damie\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\\LocalCache\\local-packages\\lib\\site-packages\\wsdl'

    def _get_camera_widget(self, camera: QWidgetCameraONVIF) -> CameraStream:
        size = QWidgetCameraSize(400, 300)
        return CameraStream(
            camera,
            size
        )

    @staticmethod
    def _apply_default_button_style(button: QPushButton):
        button.setStyleSheet("QPushButton { background-color: #badcac;"
                             "height: 50px;"
                             "border-radius: 5px;"
                             "box-shadow: 5px 5px 5px grey;"
                             "font-size: 20px;"
                             "text-align:center}")

    def _create_button(self, name, callback=None) -> QPushButton:
        button = QPushButton(name)
        button.resize(200, 40)
        self._apply_default_button_style(button)
        if callback is not None:
            button.clicked.connect(lambda: callback(button))

        return button

    def __init__(self, width: int, height: int):
        super().__init__()
        self.ipx = Ipx800("192.168.1.88")
        self.setWindowTitle('Melodia Observatory')
        self.setMouseTracking(True)
        self.show()
        self.resize(width, height)
        self._tool_bars()

        _global_widget = QWidget()
        _global_layout = QHBoxLayout(_global_widget)

        _camera_layout = QVBoxLayout()
        _camera_layout.addWidget(self._get_camera_widget(
            QWidgetCameraONVIF('192.168.1.181', 'dlasserre', 'XnyexbUF78!!', 2020, self._wsdl)))
        _camera_layout.addWidget(self._get_camera_widget(
            QWidgetCameraONVIF('192.168.1.138', 'dlasserre', 'XnyexbUF78!!', 2020, self._wsdl)))

        _hub_layout = QVBoxLayout()
        light_status = self.ipx.get_output_status('03')
        _hub_layout.addWidget(self._create_button(('Open' if light_status else 'Close')+' lights', self._turn_light))
        _hub_layout.addWidget(self._create_button('Open Telescope'))
        _hub_layout.addWidget(self._create_button('Open Roof'))


        # _hub_layout.addWidget(QPushButton('&Open Telescope'))
        # _hub_layout.addWidget(QPushButton('&Open Roof'))

        _global_layout.addLayout(_hub_layout)
        _global_layout.addLayout(_camera_layout)

        self.setCentralWidget(_global_widget)

    def _turn_light(self, button: QPushButton):
        if self.ipx.get_output_status('03') == '1':
            self.ipx.turn_off('03')
            button.setText('Open lights')
            return False
        self.ipx.turn_on('03')
        button.setText('Close lights')
        return True


    def _tool_bars(self):

        tools = self.addToolBar("tools")

        self.camera = QAction(QIcon(":camera.svg"), '&Camera')
        tools.addAction(self.camera)

        self.hub = QAction(QIcon(":hub.svg"), '&Hub')
        tools.addAction(self.hub)

        self.scope = QAction(QIcon(":telescope.svg"), '&Telescope')
        tools.addAction(self.scope)

