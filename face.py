import mediapipe as mp
import cv2 
from PIL import Image
import numpy as np
import tensorflow as tf
from scipy.spatial.distance import cosine
from PIL import Image


# face detection configurations
mpFaceDetection = mp.solutions.face_detection
faceDetection = mpFaceDetection.FaceDetection(min_detection_confidence = 0.5, model_selection = 1)

# facenet_model for embeddings
facenet_model = tf.keras.models.load_model("./models/facenet_keras_128.h5")

images_path = "./static/"

def predict(known_img, candicate_img):
    known_img = cv2.imread(images_path+known_img)
    candicate_img = cv2.imread(images_path+candicate_img)

    known_face = extractFaces(known_img)
    if type( known_face[0]) == str:
        return "File 1 does not exist face"
    candidate_face = extractFaces(candicate_img)

    if type(candidate_face[0]) == str:
        return "File 2 does not exist face"
    known_embedding = getEmbedding(known_face[0])
    candidate_embedding = getEmbedding(candidate_face[0])

    result = is_match(known_embedding, candidate_embedding)
    return "Result: "+result
# face embeddings for comparsion two facest (input: Pre-processed image, output: a list with 128 datas (features>
def getEmbedding(face_pixels):
        #scale pixel values
        face_pixels = face_pixels.astype('float32')
        #standardize pixel values across channels
        mean, std = face_pixels.mean(), face_pixels.std() # mean and standat deviation
        face_pixels = (face_pixels - mean) / std
        # transform face into one sample
        samples = np.expand_dims(face_pixels, axis=0)
        # make prediction to get embedding
        embedding = facenet_model.predict(samples)
        return embedding
# it compares 2 list with size 128 and returns 1 they are same people else 0
def is_match(known_embedding, candidate_embedding, thresh=0.3):
        # calculate distance between embeddings
        score = cosine(known_embedding, candidate_embedding)

        if score <= thresh:
            #print('>face is a Match (%.3f <= %.3f)' % (score, thresh))
            return "Same person"
        else:
            #print('>face is NOT a Match (%.3f > %.3f)' % (score, thresh))
            return "Different person"

    
# extract face on entire image
def extractFaces(img,requiredSize = (160, 160)):
        # convert the image from BGR to RGB space 
        #imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # get face detection result
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results_face = faceDetection.process(img)

        # find number of faces on image
        faces = results_face.detections # Number of faces
        
        # return it if faces variable is None
        if faces == None:
            return ["There is no face here!", 0]

        # return it if there is not a face
        elif len(faces) == 0:
            return ["There is no face here!", 0]
        
        elif len(faces)>1:
            return ["Multiple face!", int(len(faces))]
        # return it if there is a face
        elif len(faces) == 1:
            # loop on the detected faces
            for id, detection in enumerate(faces):
                # height and width of image
                h, w, _  = img.shape
                # get bounding box of face
                bbox = detection.location_data.relative_bounding_box
                # convert values in bbox float to integer
                bbox = int(bbox.xmin * w), int(bbox.ymin * h), \
                    int(bbox.width * w), int(bbox.height * h)
                # crop face using bbox
                
                face = img[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]]
                # convert face to Image object
                face = Image.fromarray(face)
                # resize face by 160x160 for FaceNet
                face = face.resize(requiredSize)
                face = np.asarray(face)

                return face,bbox