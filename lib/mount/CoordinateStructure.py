

class CoordinateStructure:

    def __init__(self, altitude, azimuth):
        self.azimuth = azimuth
        self.altitude = altitude

    def get_dec(self):
        return self.altitude

    def get_ra(self):
        return self.azimuth
