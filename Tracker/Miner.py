import Stats

class Miner():
    '''Miner obj to hold info & stats'''

    def __init__(self, name, host, port, stats=None):
        '''Initialize parameters'''
        self._name = name
        self._host = host
        self._port = int(port)
        if stats is None:
            self._stats = Stats.Stats('Claymore json')
        else:
            self._stats = stats


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

    @property
    def stats(self):
        return self._stats
