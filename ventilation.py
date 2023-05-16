

class Ventilation:
    """ Ventilation management """
    def __init__(self, pegasus, ipx, debug=False):
        environment = pegasus.get_environment()
        if debug:
            print('humidity: ' +
                  str(environment['humidity']) + ' Temperature: ' +
                  str(environment['temperature']) + ' dewPoint: ' +
                  str(environment['dewPoint']))
        if environment['humidity'] > 70 or environment['temperature'] > 30:
            if ipx.OFF == ipx.output_status('06'):
                ipx.turn_on('06')
        else:
            ipx.turn_off('06')
