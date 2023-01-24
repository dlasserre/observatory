import time

from lib import Observatory
from lib.ipx800.Ipx800 import Ipx800
from lib.weather.Wunderground import Weather
from lib.mount.CEM70G import CEM70G
from lib.pegasus.Pegasus import Pegasus

ipx = Ipx800('192.168.1.88')
mount = CEM70G('192.168.1.73', 8899)
weather = Weather('36ea49c08fe446d9aa49c08fe446d946', 'ISAUJO6')
app = Observatory.Observatory(mount)


degree = 4.385981

min = (degree % 1) * 60
sec = round((((degree % 1) * 60) % 1) * 60, 2)
print(str(4) + '° ' + str(round(min)) + '\' ' + str(sec) + '"')
print(str(round(degree - degree%1)))
exit()

coordinates = app.get_current_scope_position()
print(coordinates)


