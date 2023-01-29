import socket
import time
from lib.mount.CoordinateStructure import CoordinateStructure


class CEM70G:
    """ CEM70G """

    MOUNT_STOPPED = 0
    MOUNT_TRACKING_WITHOUT_PEC = 1
    MOUNT_SLEWING = 2
    MOUNT_GUIDING = 3
    MOUNT_FLIP_MERIDIAN = 4
    MOUNT_TRACKING_WITH_PEC = 5
    MOUNT_PARKED = 6
    MOUNT_AT_HOME_POSITION = 7

    GPS_KO = 0
    GPS_NO_RECEIVED_DATA = 1
    GPS_OK = 2

    def __init__(self, ip: str, port: int = 8899) -> None:
        self.input = 1
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, port)
        self.sock.connect(server_address)
        self.information = None

    def __send(self, command: str) -> str:
        self.sock.send(command.encode())
        data = self.sock.recv(4096)
        return data.decode()

    def __get_mount_status(self):
        return int(self.get_information()[18:19])

    def get_information(self):
        while True:
            status = self.__send(':GLS#')
            if len(status) == 24:
                return status
            time.sleep(1)

    def __gps_status(self):
        return int(self.get_information()[16:17])

    def gps_is_activated(self):
        return True if self.__gps_status() == self.GPS_OK else False

    def gps_is_disconnected(self):
        return True if self.__gps_status() == self.GPS_KO else False

    def is_tracking(self) -> bool | int:
        state = self.__get_mount_status()
        match state:
            case [self.MOUNT_TRACKING_WITHOUT_PEC, self.MOUNT_TRACKING_WITH_PEC]:
                return self.__get_mount_status()
        return False

    def is_tracking_with_pec(self, state) -> bool:
        if not state or state == self.MOUNT_TRACKING_WITHOUT_PEC:
            return False
        return True

    def is_stopped(self):
        return True if self.__get_mount_status() == self.MOUNT_STOPPED else False

    def is_parked(self) -> bool:
        return True if self.__get_mount_status() == self.MOUNT_PARKED else False

    def is_at_home_position(self):
        return True if self.__get_mount_status() == self.MOUNT_AT_HOME_POSITION else False

    def get_park_position(self):
        position = self.__send(':GPC#')
        return CoordinateStructure(position[0:8], position[-9:])

    def move_to(self, ra, dec) -> None:
        self.__send(':sRA' + ra + '#')
        self.__send(':Sds' + dec + '#')

    @staticmethod
    def _convert_arcs(arcs: int):
        degree = (arcs * 0.01) / 3600
        min = (degree % 1) * 60
        sec = round((((degree % 1) * 60) % 1) * 60, 2)

        return degree, min, sec

    def current_scope_position(self):
        try:
            position = self.__send(':GAC#')
            sign = position[0:1]

            _dec = int(position[1:9])
            _ra = int(position[9:18])
            if (_dec > 32400000 or _dec < -32400000) or (_ra > 129600000 or _ra < 0):
                return self.current_scope_position()
            dec_degree, dec_min, dec_sec = self._convert_arcs(_dec)
            ra_degree, ra_min, ra_sec = self._convert_arcs(_ra)
            dec = 'ALT=' + (sign + str(int(dec_degree)) + '. ' + str(int(dec_min)) + "' " + str(round(dec_sec, 2)) + '"')
            ra = 'AZ=' + (str(int(ra_degree)) + '. ' + str(int(ra_min)) + "' " + str(round(ra_sec, 2)) + '"')

            return dec, ra
        except:
            return self.current_scope_position()

    def park_mount(self) -> None:
        park = self.get_park_position()
        self.move_to(park.get_azimuth(), park.get_altitude())
