from lib.ipx800.Ipx800 import Ipx800
from lib.mount.CEM70G import CEM70G


class Observatory:
    """ Observatory pilote """


    def __init__(self):
        self.ipx = Ipx800('192.168.1.88')
        self.mount = CEM70G('192.168.1.5')

    def is_park(self) -> bool:
        return self.ipx.get_input_status('02') == self.ipx.ON and \
            self.mount.is_parked()

obs = Observatory()
print(obs.is_park())
