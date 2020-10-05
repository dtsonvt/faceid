import os
# Flask settings
FLASK_SERVER_NAME = 'localhost:8888'
FLASK_HOST = '0.0.0.0'
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False


# SQL settings
serverName = '192.168.1.168'
AccountSQL='sa'
Password='123456a@'
DatabaseName='Face'


# Values Default for FaceId
THRESHOLD_FRAME = 4         # number of same person
THRESHOLD_DISTANCE = 0.615    # Euclid distance of two embedding vectors 512

# Search in 
SEARCHIN_DB = 'database'
SEARCHIN_AB = 'avairable'
SEARCHIN_QE = 'queue'

# path faces:
PATH_CURRENT = os.getcwd()

PATH_LOG ="{}/log".format(PATH_CURRENT)
PATH_FACES ="{}/static/database/FaceId".format(PATH_CURRENT)
PATH_IMAGE_QUEUE ="{}/static/images/Queue".format(PATH_CURRENT)
PATH_IMAGE_STORAGE ="{}/static/images/storage".format(PATH_CURRENT)
PATH_IMAGE_HIST ="{}/static/images/hist".format(PATH_CURRENT)

#Config
FEATURE_KEY ='Ipc247.co'