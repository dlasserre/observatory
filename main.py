import configparser
import time

import ventilation
from lib.ipx800.Ipx800 import Ipx800
from lib.pegasus.PPBAdvance import PPBAdvance

config = configparser.ConfigParser()
config.read('config.ini')

ipx = Ipx800(config['ipx']['address'])
pegasus = PPBAdvance(config['pegasus']['address'])

# Gestion de la ventilation depuis les constantes du pegasus.
while True:
    ventilation.Ventilation(pegasus, ipx, True)
    time.sleep(3600)
