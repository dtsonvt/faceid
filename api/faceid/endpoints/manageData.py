from static.library import *
from api.restplus import api
from flask_restplus import Resource
from api.faceid import serializers
from static import settings
from flask import request

ns = api.namespace('faceid/manageData', description='')

# @app.before_request
# def before():
#     ip_address = request.remote_addr
#     header = request.headers.get('Authorization')
#     print(header)
#     print("Requester IP: ", ip_address)

@ns.route('/reloadFromFile')
class ManageData(Resource):
    
    @api.expect(serializers.key)
    def post(self):
        base64Image = request.get_json()['key']    
        if(base64Image != settings.FEATURE_KEY):
            return "Key is not valid!"
        global list_emb_arrays_db,list_labels_db,list_emb_arrays_queue,list_labels_queue,list_emb_arrays_avairable,list_labels_avairable
       
        # pathDir = settings.PATH_FACES
        try:
            pathDir = settings.PATH_FACES

            pathFile = "{}/database.pkl".format(pathDir) 
            if os.path.isfile(pathFile):
                with open(pathFile, 'rb') as file:
                    list_emb_arrays_db, list_labels_db = pickle.load(file)
                    list_emb_arrays_db = list_emb_arrays_db.astype('float32')

            pathFile = "{}/database_ab.pkl".format(pathDir) 
            if os.path.isfile(pathFile):
                with open(pathFile, 'rb') as file:
                    list_emb_arrays_avairable, list_labels_avairable = pickle.load(file)
                    list_emb_arrays_avairable = list_emb_arrays_avairable.astype('float32')

            pathFile = "{}/database_queue.pkl".format(pathDir)  
            if os.path.isfile(pathFile):     
                with open(pathFile, 'rb') as file:
                    list_emb_arrays_queue, list_labels_queue = pickle.load(file)
                    list_emb_arrays_queue = list_emb_arrays_queue.astype('float32')
                    print(len(list_emb_arrays_queue))
            return "Ok"
        except Exception as ex:
            return "ERROR: {}".format(str(ex))

@ns.route('/create')
class ManageData(Resource):
    @api.expect(serializers.key)
    def post(self):
        global list_emb_arrays_db,list_labels_db,list_emb_arrays_queue,list_labels_queue,list_emb_arrays_avairable,list_labels_avairable
        try:
            base64Image = request.get_json()['key']    
            if(base64Image != settings.FEATURE_KEY):
                return "Key is not valid!"
            
            pathDir = settings.PATH_FACES

            extension.CheckAndCreateDir(pathDir)

            with open('{}/database.pkl'.format(pathDir), 'wb') as outfile:
                pickle.dump((list_emb_arrays_db, list_labels_db), outfile)
            with open('{}/database_queue.pkl'.format(pathDir), 'wb') as outfile:
                pickle.dump((list_emb_arrays_queue, list_labels_queue), outfile)
            with open('{}/database_ab.pkl'.format(pathDir), 'wb') as outfile:
                pickle.dump((list_emb_arrays_avairable, list_labels_avairable), outfile)
            return "Ok"
        except Exception as ex:
            return "ERROR: {}".format(str(ex))

