from lib.pegasus import Pegasus


class PPBAdvance(Pegasus.Pegasus):
    """ PPBAdvance API """

    def __init__(self, address: str):
        super().__init__(address, 'PPBAdvance')

    def __auto_dew(self, state: bool) -> None:
        self._call('post', '/Driver/PPBAdvance/Dew/Auto/'
                   + ('On' if state else 'Off') + '?DriverUniqueKey=' + self.unique_key)

    def get_devices_connected(self) -> None:
        response = self._call('get', '/Server/DeviceManager/Connected')
        for device in response:
            print('Device: ' + device.name + ' Key: ' + device.uniqueKey + ' Desciption: ' + device.fullName)

    def auto_dew_on(self) -> None:
        self.__auto_dew(True)

    def auto_dew_off(self) -> None:
        self.__auto_dew(False)

    def set_adjustable(self, state: bool) -> None:
        self._call('post', 'Driver/PPBAdvance/Power/Variable/'
                   + ('On' if state else 'Off') + '?DriverUniqueKey=' + self.unique_key)

    def set_power(self, state: bool) -> None:
        self._call('post', '/Driver/PPBAdvance/Power/Hub/'
                   + ('On' if state else 'Off') + '?DriverUniqueKey=' + self.unique_key)

    def get_auto_dew_status(self) -> bool:
        response = self._call('get', '/Driver/PPBAdvance/Dew/Auto?DriverUniqueKey=' + self.unique_key)
        return True if response['data']['message']['switch']['state'] == 'ON' else False

    def get_environment(self):
        response = self._call('get', '/Driver/PPBAdvance/Report/Environment?DriverUniqueKey=' + self.unique_key)
        return response['data']['message']

    def set_dew(self, port, state):
        if self.get_auto_dew_status():
            self.auto_dew_off()
            if state:
                self._call('post', '/Driver/PPBAdvance/Dew/' + port + '/On/Max?DriverUniqueKey=' + self.unique_key)
            else:
                self._call('post', '/Driver/PPBAdvance/Dew/' + port + '/Off?DriverUniqueKey=' + self.unique_key)



