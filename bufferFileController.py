import os
import json
from datetime import datetime

import jsonController as JC

'''
'1234536': {
        'authorizationState': False,
        'salesCollectState': False
    }
'''

class stateController(JC.jsonController):
    def setUserStats(self, idUser, stats, value):
        dateFromFiles = self.getDate()
        change = False

        for id in dateFromFiles:
            if id == idUser:
                dateFromFiles[id][stats] = value
                change = True

        if (change == False):
            dateFromFiles[idUser] = {
                'authorizationState': False,
                'salesCollectState': False
            }
            dateFromFiles[idUser][stats] = value
        
        self.writeDate(dateFromFiles)

    def getAuthorizationUserState(self, idUser):
        dateFromFiles = self.getDate()

        for id in dateFromFiles:
            if (id == idUser):
                return dateFromFiles[id]['authorizationState']
    
    def getSalesCollectState(self, idUser):
        dateFromFiles = self.getDate()

        for id in dateFromFiles:
            if (id == idUser):
                return dateFromFiles[id]['salesCollectState']