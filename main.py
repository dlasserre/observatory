from lib import Observatory
from lib.mount.CEM70G import CEM70G

mount = CEM70G('192.168.1.73', 8899)
app = Observatory.Observatory(mount)
print(app.get_current_scope_position())