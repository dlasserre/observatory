from gui.Index import Index
from PyQt5.QtWidgets import QApplication
import sys


app = QApplication(sys.argv)
a = Index(1024, 500)
a.show()
sys.exit(app.exec_())
