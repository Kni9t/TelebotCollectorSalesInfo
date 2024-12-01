import os
import json
from datetime import datetime

class jsonController:
    def __init__(self, bufFileName):
        self.fileName = bufFileName
        if (os.path.isfile(self.fileName)):
            path, file = os.path.split(self.fileName)
            os.rename(self.fileName, f'{path}/{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}-{file}')
            file = open(self.fileName, 'w', encoding='utf8')
            file.close()
        else:
            file = open(self.fileName, 'w', encoding='utf8')
            file.close()

    def getDate(self):
        if (os.path.isfile(self.fileName)):
            try:
                file = open(self.fileName, 'r', encoding='utf8')
                strList = json.load(file)
                file.close()
                return strList
            except:
                return {}
        else:
            return {}
        
    def addDate(self, date):
        if (os.path.isfile(self.fileName)):
            dateFromFiles = self.getDate()
            for key in date:
                dateFromFiles[str(key)] = date[str(key)]

            with open(self.fileName, "w", encoding='utf8') as outfile:
                outfile.write(json.dumps(dateFromFiles))
                outfile.close()
        else:
            self.writeDate(date)

    def writeDate(self, date):
        with open(self.fileName, "w", encoding='utf8') as outfile:
                outfile.write(json.dumps(date))
                outfile.close()