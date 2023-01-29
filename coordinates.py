import time
from lib import Observatory
from lib.mount.CEM70G import CEM70G

mount = CEM70G('192.168.1.73', 8899)
app = Observatory.Observatory(mount)

while True:
    coordinates = app.get_current_scope_position()
    file = open('./coordinates.txt', 'w')
    file.write(coordinates['ra']+"\n")
    file.write(coordinates['dec'])
    file.close()
    time.sleep(5)
