from flask import Flask, request, jsonify, abort
from flask_restplus import Api, Resource, fields
from static.library import *
# from static import functions
# from cam_img import *

count = 0
BLUR_THRES = 180
flag_regis = True
gr = tf.Graph().as_default()
sess = tf.Session()
gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
facenet.load_model(FACENET_MODEL_PATH)
images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
sess = tf.Session()
graph = tf.get_default_graph()
pnet, rnet, onet = detect_face.create_mtcnn(sess, "./src/align")

# images_placeholder = 0
# embeddings = 0
# phase_train_placeholder = 0

# def Instance():
#     try:
#         global embeddings,phase_train_placeholder,images_placeholder,graph,sess
#         with sess.as_default():
#             with graph.as_default(): 
#                 print("Instance!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#                 facenet.load_model(FACENET_MODEL_PATH)
#                 images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
#                 embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
#                 phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0") 
#     except Exception as ex:
#         print("Instance: {}".format(str(ex)))