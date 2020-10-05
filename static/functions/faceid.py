
from static.library import *
from static.instance import *
from static import settings
from static.functions import extension
from static.database import SqlHelper
from static.functions.logger import logger
from datetime import datetime
import time
import json

def GetOrdinalNumber():
    try:
        params = {}
        error,result = SqlHelper.ExucteSQLasDataTable("spRegisterGetOrdinalNumber", **params)  
        if(error != ""):
            return error,""
            
        Id = result['Table1'][0]['Id']
        print(Id)
        OrdinalNumber = result['Table1'][0]['OrdinalNumber']

        return "",Id,OrdinalNumber
    except Exception as ex:
        print("FaceId - GetOrdinalNumber - {}".format(str(ex)))
        logger.error("FaceId - GetOrdinalNumber - {}".format(str(ex)))
        return str(ex),"",""

def GetOrdinalNumberById(Id):
    try:
        params = {'Id':Id }
        error,result = SqlHelper.ExucteSQLasDataTable("spRegisterGetOrdinalNumberById", **params)  
        if(error != ""):
            return error,""
            
        Id = result['Table1'][0]['Id']
        OrdinalNumber = result['Table1'][0]['OrdinalNumber']

        return "",Id,OrdinalNumber
    except Exception as ex:
        print("FaceId - GetOrdinalNumber - {}".format(str(ex)))
        logger.error("FaceId - GetOrdinalNumber - {}".format(str(ex)))
        return str(ex),"",""

def UpdateQueueDetails(Id,ListPathImage):
    try:
        params =  {"Id": Id, "ListPathImage": ListPathImage}
        error,result = SqlHelper.ExucteSQLasDataTable("spRegisterUpdateQueue", **params)  
        if(error != ""):
            return error,""
            
        Result = result['Table1'][0]['Result']
        Message = result['Table1'][0]['Message']

        if Result == "1":
            return "",""
        else:
            return Message,""

    except Exception as ex:
        print("FaceId - UpdateQueueDetails - {}".format(str(ex)))
        logger.error("FaceId - UpdateQueueDetails - {}".format(str(ex)))
        return str(ex),"",""

def ConvertBase64ToVector(face_img):
    try:
        jpg_as_np = np.frombuffer(face_img, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)
        print(img.shape)
        # img = img.reshape((160,160,3))#cv2.resize(img,(160,160))
        img = cv2.resize(img,(160,160))
        face_norm = facenet.prewhiten(img)
        face_reshape = face_norm.reshape(-1, INPUT_IMAGE_SIZE, INPUT_IMAGE_SIZE, 3)
        feed_dict = {images_placeholder: face_reshape, phase_train_placeholder: False}

        emb_array = sess.run(embeddings, feed_dict=feed_dict)
        emb_array = emb_array.astype('float32')
        return "",emb_array
    except Exception as ex:
        print("ConvertBase64ToVector - {}".format(str(ex)))
        return str(ex),""

def SearchFaceIn(storage, embFace):
    try:
        '''
        function: find person type 1 : N
        input: embed: has shape (1, 512), embedding vector
        output: personId: identify person
        '''
        global list_emb_arrays_db,list_labels_db,list_emb_arrays_avairable,list_labels_avairable,list_emb_arrays_queue,list_labels_queue
        list_emb_arrays = np.zeros((0,512))
        list_labels = []
        if(storage == settings.SEARCHIN_DB):
            print("SEARCHIN_DB: ",len(list_emb_arrays_db))
            list_emb_arrays = list_emb_arrays_db
            list_labels = list_labels_db  
        elif (storage == settings.SEARCHIN_AB):
            print("SEARCHIN_AB: ",len(list_emb_arrays_avairable))
            list_emb_arrays = list_emb_arrays_avairable
            list_labels = list_labels_avairable
        elif (storage == settings.SEARCHIN_QE):
            print("SEARCHIN_QE: ",len(list_emb_arrays_queue))
            list_emb_arrays = list_emb_arrays_queue
            list_labels = list_labels_queue

        list_emb_arrays = list_emb_arrays.astype('float32')

        if(len(list_labels)==0):
            return "",-1

        THRESHOLD_FRAME = settings.THRESHOLD_FRAME         # number of same person
        THRESHOLD_DISTANCE = settings.THRESHOLD_DISTANCE    # Euclid distance of two embedding vectors 512
        personId = -1
     
        index = faiss.IndexFlatL2(list_emb_arrays.shape[1])    # get dimension 512
        index.add(list_emb_arrays)

        datapoint = embFace.reshape((-1, 512))
        dist, idx = index.search(datapoint, 15)

        result = []
        for j in idx[:, 1:].tolist()[0]:
            result.append(list_labels[j])
        result = np.array(result)

        # SORT and FIND INDEX DUPLICATE
        idx_sort = np.argsort(result)
        result_sort = result[idx_sort]
        vals, idx_start, count = np.unique(result_sort, return_counts=True, return_index=True)
        print(count,"-",np.max(count))
        if np.max(count) >= THRESHOLD_FRAME:  # check the first time
            # find distance minimum
            result_index = idx_start.item(np.argmax(count))
            index_distance = np.argwhere(result == result_sort.item(result_index))
            distance_min = np.min(dist[:, 1:][0][index_distance])
            print("distance_min: ",distance_min)
            if distance_min <= THRESHOLD_DISTANCE:  # check the second time
                personId = vals.item(np.argmax(count))

        return "",personId
    except Exception as ex:
        print("SearchFaceInList: {}".format(str(ex)))
        return str(ex),""

def CropImageContainFace(byteImageFull):
    try:
        jpg_as_np = np.frombuffer(byteImageFull, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)
        frame = copy.copy(img)
        bounding_boxes, _ = detect_face.detect_face(frame, MINSIZE, pnet, rnet, onet, THRESHOLD, FACTOR)
        faces_found = bounding_boxes.shape[0]
        if faces_found > 0:
            idmax = 0
            if faces_found > 1:
                idmax = GetMaxBBox(bounding_boxes)
            det = bounding_boxes[:, 0:4]
            # bb = np.zeros((faces_found, 4), dtype=np.int32)
            bb = np.zeros((4,), dtype=np.int32)     # bb: x_min, y_min, x_max, y_max
            bb[0] = np.maximum(det[idmax][0] - MARGIN/2, 0)
            bb[1] = np.maximum(det[idmax][1] - MARGIN/2, 0)
            bb[2] = np.minimum(det[idmax][2] + MARGIN/2, frame.shape[1])
            bb[3] = np.minimum(det[idmax][3] + MARGIN/2, frame.shape[0])
            if (bb[3] - bb[1]) / frame.shape[0] > 0.25:
                cropped = frame[bb[1]:bb[3], bb[0]:bb[2], :]
                if cropped.shape[0] == 0 or cropped.shape[1] == 0: 
                    return jsonify({"status": "success", "message":-1 , "data": ""}), 200
                scaled = cv2.resize(cropped, (INPUT_IMAGE_SIZE, INPUT_IMAGE_SIZE), interpolation=cv2.INTER_CUBIC)
                print(type (scaled))
                retval, buffer = cv2.imencode('.png', scaled)

                jpg_as_text = base64.b64encode(buffer).decode('utf-8')
            return "",jpg_as_text
    except Exception as ex:
        print("CropImageContainFace: {}".format(str(ex)))
        return str(ex),""

def RegisterToQueue(b64OfFaces):
    try:
        listBase64 = b64OfFaces.split(';')
        
        error,Id,OrdinalNumber = GetOrdinalNumber()
        
        if (error!=""):
            return "RegisterToQueue: {}".format(str(ex)),""

        pathDir = "{}/{}/STT_{}".format(settings.PATH_IMAGE_QUEUE,datetime.now().strftime("%d%m%Y"),OrdinalNumber)
        extension.CheckAndCreateDir(pathDir)

        listPathFile = ""

        emb_person = np.zeros((20, 512))
        label_person = []
        count = 0
        for strBase64 in listBase64:
            if strBase64 == "":
                continue
            image = base64.b64decode(strBase64.encode())

            fileName = "img_{}.png".format(int(time.time()*1000))

            extension.SaveImage(image,pathDir,fileName)

            error,emb_array = ConvertBase64ToVector(image)

            emb_person[count] = emb_array.astype('float32')
            label_person.append(Id)

            listPathFile+="{}/{};".format(pathDir,fileName)

            count+=1

        error,message = WriteFileKpl(settings.SEARCHIN_QE,emb_person,label_person)
        if(error != ""):
            return error,""
        
        error,message = UpdateQueueDetails(Id,listPathFile)
        if(error != ""):
            return error,""

        return "",OrdinalNumber
    except Exception as ex:
        return "RegisterToQueue: {}".format(str(ex)),""

def WriteFileKpl(storage,emb_array,labels):
    try:
        global list_emb_arrays_db,list_labels_db,list_emb_arrays_queue,list_labels_queue,list_emb_arrays_avairable,list_labels_avairable
        pathDir = settings.PATH_FACES
        extension.CheckAndCreateDir(pathDir)

        if (storage == settings.SEARCHIN_QE):
            list_emb_arrays_queue = np.concatenate((list_emb_arrays_queue, emb_array), axis=0)
            [list_labels_queue.append(x) for x in labels]
            with open('{}/database_queue.pkl'.format(pathDir), 'wb') as outfile:
                pickle.dump((list_emb_arrays_queue, list_labels_queue), outfile)

        elif (storage == settings.SEARCHIN_AB):
            list_emb_arrays_avairable = np.concatenate((list_emb_arrays_avairable, emb_array), axis=0)
            [list_labels_avairable.append(x) for x in labels]
            with open('{}/database_ab.pkl'.format(pathDir), 'wb') as outfile:
                pickle.dump((list_emb_arrays_avairable, list_labels_avairable), outfile)

        elif (storage == settings.SEARCHIN_DB):
            list_emb_arrays_db = np.concatenate((list_emb_arrays_db, emb_array), axis=0)
            [list_labels_db.append(x) for x in labels]
            with open('{}/database.pkl'.format(pathDir), 'wb') as outfile:
                pickle.dump((list_emb_arrays_db, list_labels_db), outfile)

        return "","success"
    except expression as identifier:
        return "WriteFileKpl: {}".format(str(ex)),""




