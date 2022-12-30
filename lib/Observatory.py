import time

from lib.ipx800.Ipx800 import Ipx800
from lib.mount.CEM70G import CEM70G
from lib.allsky.CloudDetector import  CloudDetector

class Observatory:
    """ My observatory """

    OPEN = 'OPEN'
    CLOSE = 'CLOSE'

    def __init__(self, mount: CEM70G = None, ipx: Ipx800 = None):
        self.ipx = ipx
        self.mount = mount

    def _open_output(self, number: str) -> None:
        self.ipx.turn_on(number)

    def _close_output(self, number: str) -> None:
        self.ipx.turn_off(number)

    def _input_status(self, number: str) -> str:
        return self.ipx.get_input_status(number)

    def __turn(self, output: str) -> bool:
        if self.ipx.get_output_status(output) == '1':
            self.ipx.turn_off(output)
            return False
        self.ipx.turn_on(output)
        return True

    def roof_status(self) -> str:
        is_open = self._input_status('03')
        is_close = self._input_status('04')

        if is_open == self.ipx.OFF and is_close == self.ipx.ON:
            return self.CLOSE
        return self.OPEN

    def mount_is_parked(self) -> bool:
        return self.mount.is_parked()

    def is_safe_to_roll_roof(self) -> bool:
        if self.mount_is_parked() and self.ipx.get_input_status('02') is self.ipx.ON:
            return True
        return False

    def open_light(self) -> None:
        self.ipx.turn_on('03')

    def close_light(self) -> None:
        self.ipx.turn_off('03')

    def open_roof(self):
        if self.is_safe_to_roll_roof() and self.roof_status() == self.CLOSE:
            self.ipx.turn_on('05')
            time.sleep(0.5)
            self.ipx.turn_off('05')

    def close_root(self):
        if self.is_safe_to_roll_roof() and self.roof_status() == self.OPEN:
            self.ipx.turn_on('05')
            time.sleep(0.5)
            self.ipx.turn_on('05')

    def get_current_scope_position(self):
        coordinate = self.mount.current_scope_position()
        return {'ra': coordinate[0], 'dec': coordinate[1]}

    @staticmethod
    def get_current_cloud_cover(path_to_img, radius) -> int:
        cloud = CloudDetector()
        return cloud.percent_cloudy(path_to_img, radius)