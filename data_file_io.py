class dataFileIO:

    def __init__(self, filename, filetype):
        self.filename = filename
        self.filetype = filetype
        self.sys_params = {}

    def __str__(self):
        return f'{self.filename} | {self.filetype}'

    def readfile(self):
        match self.filetype:
            case 'prompt':
                self.readpromptfile()
            case 'background':
                self.readbgfile()
            case _:
                print("No file type")

    def readpromptfile(self):
        self.file = open(self.filename, 'r')
        self.data = dict()
        for line in self.file.readlines():
            line_array = line.split(':')
            self.data[str(line_array[0].strip())] = str(line_array[1].strip())
        self.file.close()

        print('Loaded: ', self.filename)

    def read_bg_file(self):
        #function that opens formatted file that gives background on the person
        self.file = open(self.filename,'r')
        self.data = dict()
        for line in self.file.readlines():
            line_array = l