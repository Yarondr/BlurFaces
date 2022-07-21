from fileinput import filename
from pyexpat import model
import cv2
import numpy as np
import os
import sys

model = None

def running_path():
    application_path = None
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    elif __file__:
        application_path = os.path.dirname(__file__)
    return application_path

def load_model():
    # get paths
    prototxt_path = os.path.join(running_path(), "face_detector", "deploy.prototxt.txt")
    model_path = os.path.join(running_path(), "face_detector", "res10_300x300_ssd_iter_140000_fp16.caffemodel")

    # load Caffe model
    global model
    model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
    return model


def blur_faces(image_path, blur_level=1):
    # load image
    image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)

    # get width and height of the image
    h, w = image.shape[:2]

    # gaussian blur kernel size depends on width and height of original image
    kernel_width = (w // (11-blur_level)) | 1
    kernel_height = (h // ((11-blur_level))) | 1

    # preprocess the image: resize and performs mean subtraction
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
    # set the image into the input of the neural network
    model.setInput(blob)

    # perform inference and get the result
    output = np.squeeze(model.forward())

    for i in range(0, output.shape[0]):
        confidence = output[i, 2]
        # get the confidence
        # if confidence is above 40%, then blur the bounding box (face)
        if confidence > 0.4:
            # get the surrounding box cordinates and upscale them to original image
            box = output[i, 3:7] * np.array([w, h, w, h])
            # convert to integers
            start_x, start_y, end_x, end_y = box.astype(np.int64)
            # get the face image
            face = image[start_y: end_y, start_x: end_x]
            # apply gaussian blur to this face
            face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
            # put the blurred face into the original image
            image[start_y: end_y, start_x: end_x] = face

    # save the image
    save_image(image, image_path)


def save_image(image, image_path):
    # last index of the image path (only the file name)
    file_name = os.path.basename(image_path)
    file_folder = os.path.dirname(image_path)

    # check if blurred folder exists, if not, create it
    if not os.path.exists(file_folder + "/blurred_faces"):
        os.makedirs(file_folder + "/blurred_faces")
    
    # save the blurred image
    new_path = os.path.join(file_folder + "/blurred_faces", file_name)
    ext = new_path.split(".")[-1]
    cv2.imencode("."+ext, image)[1].tofile(new_path)
