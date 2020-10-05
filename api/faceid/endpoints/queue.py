import logging
from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.faceid import serializers
from static.functions import extension
import base64


from static.library import *
from static.instance import *
from static.functions import faceid
from static.settings import *
# from static.functions.cam_img import *

log = logging.getLogger(__name__)

ns = api.namespace('faceid/queue', description='')

@ns.route('/check')
class FaceIdCollection(Resource):

    @api.expect(serializers.b64FaceImage)
    def post(self):
        """
        get Ordinal number from API 
        """
        try:
            base64Image = request.get_json()['base64']
            image = base64.b64decode(base64Image.encode())
            
            # jpg_as_np = np.frombuffer(image, dtype=np.uint8)
            # img = cv2.imdecode(jpg_as_np, flags=1)
            # save image to local
            error = extension.SaveImage(image)
            if(error!=""):
                return {"status": "-2", "message":error , "STT": ""}, 500
            
            error,emb_array = faceid.ConvertBase64ToVector(image)
            if(error!=""):
                return {"status": "-2", "message":error , "STT": ""}, 500

            error,personId = faceid.SearchFaceIn(SEARCHIN_AB,emb_array)
            print("personId: ",personId)
            if(error!=""):
                return {"status": "-2", "message":error , "STT": ""}, 500

            if(personId!=-1): #is existed in list avairable
                return {"status": "0", "message":"Khách Hàng đã Lấy Thẻ" , "STT": ""}, 200
            
            error,personId = faceid.SearchFaceIn(SEARCHIN_QE,emb_array)
            print("personId: ",personId)
            if(error!=""):
                return {"status": "-2", "message":error , "STT": ""}, 500
            if(personId!=-1): #is existed in queue => create a new ordinal number
                error,Id,OrdinalNumber = faceid.GetOrdinalNumberById(str(personId))
                return {"status": "1", "message":"Queue - STT của bạn là: {}".format(OrdinalNumber) , "STT": OrdinalNumber}, 200
            
            error,personId = faceid.SearchFaceIn(SEARCHIN_DB,emb_array)
            if(error!=""):
                return {"status": "-2", "message":error , "STT": ""}, 500

            if(personId!=-1): #is existed in database => create a new ordinal number & add new face to queue
                return {"status": "1", "message":"DB - STT của bạn là: 1" , "STT": "1"}, 200

            
            return {"status": "-1", "message":"Vui lòng scan khuôn mặt" , "STT": ""}, 200

        except Exception as ex:
            return {"status": "-2", "message":str(ex) , "STT": ""}, 500


@ns.route('/addnew')
class FaceIdCollection(Resource):

    @api.expect(serializers.b64OfFaces)
    def post(self):
        """
        add new faces to queue
        """
        global list_emb_arrays_queue,list_labels_queue
        try:
            base64sImage = request.get_json()['Listbase64']
            
            error,OrdinalNumber = faceid.RegisterToQueue(base64sImage)

            if(error != ""):
                return {"status": "-2", "message":error , "STT": "0"}, 500
            else:
                return {"status": "1", "message":"STT của bạn là: {}".format(OrdinalNumber) , "STT": OrdinalNumber}, 200
        except Exception as ex:
            return {"status": "-2", "message":str(ex) , "STT": ""}, 500


@ns.route("/cropforface")
class FaceIdCollection(Resource):
    @ns.expect(serializers.b64FaceImage)
    def post(self):
        try:
            base64Image = request.get_json()['base64']

            byteImage = base64.b64decode(base64Image.encode())
            
            error,jpg_as_text = faceid.CropImageContainFace(byteImage)
            if(error==""):
                return {"status": "success", "message":str(jpg_as_text) , "data": ""}, 200
            else:
                return {"status": "Error", "message":error , "data": ""}, 500
        except Exception as ex:
            return {"status": "Error", "message":str(ex) , "data": ""}, 500 