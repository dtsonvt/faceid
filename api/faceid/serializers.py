from flask_restplus import fields
from api.restplus import api

b64FaceImage = api.model('Image Face', {
    'base64': fields.String(required=True, description='base64 is encode of face image'),
})

b64OfFaces = api.model('List 20 faces link by ;', {
    'Listbase64': fields.String(required=True, description='List 20 faces link by ;')
})

key = api.model('Feature need a key', {
    'key': fields.String(required=True, description='')
})