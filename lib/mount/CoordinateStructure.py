

class CoordinateStructure:

    def __init__(self, altitude, azimuth):
        self.azimuth = azimuth
        self.altitude = altitude

    def get_altitude(self):
        return self.altitude

    def get_azimuth(self):
        return self.azimuth
