import jsonController as JC
import os, json

'''
'market id': [
    {
    'Date': '12.12.2024',
    'Time': '15:30',
    'Value': 1233,
    'Sender': Iduser
    }
]
'''

class salesController(JC.jsonController):
    def addSales(self, marketID, sales):
        if (os.path.isfile(self.fileName)):
            dateFromFiles = self.getDate()
            if(len(dateFromFiles) > 0):
                if (str(marketID) in dateFromFiles.keys()):
                    dateFromFiles[str(marketID)].append(sales)
                else:
                    dateFromFiles[str(marketID)] = [sales]
                self.writeDate(dateFromFiles)
            else:
                self.writeDate({marketID: [sales]})
        else:
            self.writeDate({marketID: [sales]})
    
    def getSumSales(self, marketID):
        if (os.path.isfile(self.fileName)):
            dateFromFiles = self.getDate()
            sumSales = 0
            for market in dateFromFiles:
                if (market == marketID):
                    for sales in dateFromFiles[market]:
                        sumSales += sales['Value']
            return sumSales
        else:
            return 0