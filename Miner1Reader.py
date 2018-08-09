

class Reader():
    '''Read, parse, and save a log from Claymore's Miner.'''

    def __init__(self, file_name=None):
        '''Initialize Reader, prep file for reading.'''
        if file_name is None:
            self.file_name = 'sample logs/1533121433_log.txt'
        else:
            self.file_name = file_name
        self.f = open(self.file_name, 'r')
        self.line = ''  # Get temp 'line' string ready for use.

# If Miner1Reader.py is run individually...
if __name__ == '__main__':
    reader = Reader()



    reader.f.close()
