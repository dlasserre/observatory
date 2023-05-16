import requests
from requests.exceptions import HTTPError


class Pegasus:
    """ Pegasus astro server """

    def __init__(self, address, name):
        self.address = address
        self.key = self.get_unique_key_from_name(name)

    def _call(self, method: str, uri: str, parameters: list = None):
        try:
            response = requests.request(method, self.address+uri, params=parameters)
            return response.json()
        except HTTPError as http_err:
            print(f'An error occurred: {http_err}')

    def get_unique_key_from_name(self, device_name: str) -> str:
        devices = self._call('get', '/Server/DeviceManager/Connected')
        for device in devices['data']:
            if device['name'] == device_name:
                return device['uniqueKey']
        raise ValueError('Device ' + device_name + ' not found or not connected')

    @property
    def unique_key(self):
        return self.key
