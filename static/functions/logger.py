import os
from static import settings
from datetime import datetime
from static.functions import extension

def writeFileLog(strLog,typelog):
    file = open('{}.{}.{}.txt'.format(settings.PATH_LOG,typelog,datetime.now().strftime("%Y%m%d")),'a')
    file.writelines("==== {}: {}\n".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), strLog))
    file.close() 

class logger:
    def debug(strLog):
        writeFileLog(strLog,"debug")

    def error(strLog):
        writeFileLog(strLog,"error")