from datetime import datetime
from static.functions import extension
from static import settings
import time
import os
from pathlib import Path

def SaveImage(image,dir = "{}/{}".format(settings.PATH_IMAGE_HIST ,datetime.now().strftime("%d%m%Y")) , filename = "img_{}.png".format(int(time.time()*1000))):
    try:
        extension.CheckAndCreateDir(dir)
        filename = "{}/{}".format(dir,filename)
        with open(filename, 'wb') as f:
            f.write(image)
        return ""
    except Exception as ex:
        return str(ex)

def CheckAndCreateDir(path):
    try:
        path = Path("{}".format(path))
        if not os.path.exists(path):
            path.mkdir(parents=True)
        # if not os.path.exists(path):
        #     os.mkdir(path)
    except Exception as ex:
        print("CheckAndCreateDir: {}",str(ex))