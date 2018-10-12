

class Miner():
    '''Miner obj to hold info & stats'''

    def __init__(self, name, host, port):
        '''Initialize parameters'''
        self._name = name
        self._host = host
        self._port = port

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port
