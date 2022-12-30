from lib import Observatory
from lib.ipx800.Ipx800 import Ipx800
from lib.mount.CEM70G import CEM70G

# mount = CEM70G('192.168.1.73', 8899)
ipx = Ipx800('192.168.1.88')
app = Observatory.Observatory()
# coordinates = app.get_current_scope_position()

percent = app.get_current_cloud_cover('clouds.png', 1000)
if percent > 30:
    ipx.turn_on('06')
