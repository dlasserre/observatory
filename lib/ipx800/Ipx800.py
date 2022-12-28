import socket


class Ipx800:
    """ IPX API M2M """

    ON = 'ON'
    OFF = 'OFF'

    def __init__(self, ip: str, port: int = 9870) -> None:
        self.input = 1
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, port)
        self.sock.connect(server_address)

    def __send(self, command: str) -> str:
        self.sock.send(command.encode())
        data = self.sock.recv(4096)
        return data.decode().strip()

    def __set_output(self, output: str, state: bool, pulse: bool = None) -> None:
        message = 'Set' + output + ('1' if state else '0')
        if pulse is True:
            message += 'p'  # Be sure to have defined the TB and TA in the ipx beforehand
        print(message)
        response = self.__send(message)
        if 'OK' == response:
            print('Success Channel 3 turn ' + ('on' if state else 'off'))

    def turn_off(self, channel: str) -> None:
        self.__set_output(channel, False)

    def turn_on(self, channel: str, pulse: bool = False) -> None:
        self.__set_output(channel, True, pulse)

    def get_output_status(self, channel: str) -> str:
        command = "GetOut" + channel
        return self.__send(command)

    def get_input_status(self, channel: str) -> str:
        command = 'GetIn'+channel
        return self.__send(command)

    def get_analog_status(self, channel: str) -> str:
        command = 'GetAn'+channel
        return self.__send(command)

    def get_count_status(self, channel: str) -> str:
        command = 'GetCount'+channel
        return self.__send(command)

    def reset_count(self, channel: str) -> str:
        command = 'ResetCount' + channel
        return self.__send(command)

    def reset(self) -> None:
        command = 'Reset'
        self.__send(command)

    def increment_count(self, counter: str) -> None:
        self.__send('ResetCount11')

