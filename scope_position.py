import time

from lib.Observatory import Observatory
from lib.mount.CEM70G import CEM70G
from PIL import Image
from PIL.ExifTags import TAGS

observatory = None
ip = '192.168.1.73'

while True:
    if observatory is None:
        try:
            mount = CEM70G(ip)
            observatory = Observatory(mount)
        except BaseException as error:
            print('Impossible to connect mount, retrying...')
            time.sleep(30)
            continue
    else:
        if not observatory.mount_is_parked():
            print(observatory.get_current_scope_position())
            time.sleep(30)
        else:
            print('mount is parked...')
        time.sleep(10)
