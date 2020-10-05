from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from scipy import misc
import sys
import os
import argparse
import tensorflow as tf
import numpy as np
from src import facenet              # offline
from src.align import detect_face    # offline
import random
from time import sleep
from matplotlib.pyplot import imread
from imageio import imread
import cv2
import pickle
import faiss
from threading import Thread, Lock
from imutils.video import VideoStream
import copy
import base64
from static import settings
from static.functions import extension

FACENET_MODEL_PATH = './model/20180402-114759.pb'
MINSIZE = 20
THRESHOLD = [0.6, 0.8, 0.8]     # MTCNN detect face
FACTOR = 0.709
INPUT_IMAGE_SIZE = 160      # image output sizeof face
MARGIN = 32     # margin for crop face in frame
# frame_mulThre = cv2.imread('./temp.jpg')    # purpose load the first time
THRESHOLD_FRAME = 8         # number of same person
THRESHOLD_DISTANCE = 0.4    # Euclid distance of two embedding vectors 512

list_emb_arrays_db  = np.zeros((0,512))
list_labels_db = []

list_emb_arrays_avairable  =np.zeros((0,512))
list_labels_avairable = []

list_emb_arrays_queue  =np.zeros((0,512))
list_labels_queue = []


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

    # pathFile = "{}/database_queue.pkl".format(pathDir)  
    pathFile = "./model/database_new.pkl"
    if os.path.isfile(pathFile):     
        with open(pathFile, 'rb') as file:
            list_emb_arrays_queue, list_labels_queue = pickle.load(file)
            list_emb_arrays_queue = list_emb_arrays_queue.astype('float32')

    extension.CheckAndCreateDir(settings.PATH_LOG)
    extension.CheckAndCreateDir(settings.PATH_FACES)
    extension.CheckAndCreateDir(settings.PATH_IMAGE_QUEUE)
    extension.CheckAndCreateDir(settings.PATH_IMAGE_STORAGE)
    extension.CheckAndCreateDir(settings.PATH_IMAGE_HIST)

except Exception as ex:
    print("Load Libary ",str(ex))





