class dataFile:

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return f'{self.filename}'

    def readfile(self):
        self.file = open(self.filename, 'r')
        self.data = dict()
        for line in self.file.readlines():
            line_array = line.split(':')
            self.data[str(line_array[0].strip())] = str(line_array[1].strip())
        self.file.close()