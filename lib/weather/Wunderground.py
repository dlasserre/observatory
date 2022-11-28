import time

from wunderground_pws import WUndergroundAPI, units


class Weather(WUndergroundAPI):
    """ Weather Underground """
    
    def __init__(self, api_key, default_station_id):
        super().__init__(api_key, default_station_id, units.METRIC_UNITS)

    def _get_current(self):
        return super().current()['observations'].pop()

    def _get_metric(self, metric: str):
        return self._get_current()['metric'][metric]

    def wind_direction(self):
        sector = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW",
                  "SW", "WSW", "W", "WNW", "NW", "NNW", "N"]
        wind_direction = self._get_current()['winddir']
        return sector[int(round((wind_direction % 360) / 22.5, 0))]

    def current_temperature(self):
        return self._get_metric('temp')

    def wind_speed(self):
        return self._get_metric('windSpeed')

    def wind_gust(self):
        return self._get_metric('windGust')

    def precip_total(self):
        return self._get_metric('precipTotal')

    def precip_rate(self):
        return self._get_metric('precipRate')

    def dew_point(self):
        return self._get_metric('dewpt')

    def pressure(self):
        return self._get_metric('pressure')

    def __str__(self):
        return 'Fast information: ' + str(self.current_temperature()) + '°C '\
               + str(self.wind_direction())+'('+str(self._get_current()['winddir'])+')'


weather = Weather('36ea49c08fe446d9aa49c08fe446d946', 'ISAUJO6')
while True:
    print(weather.wind_direction(), end="\r")
    time.sleep(2)
