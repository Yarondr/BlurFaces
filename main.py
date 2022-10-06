print("Loading...")
import os
from time import sleep
import config
import cv2
from google.cloud import vision

from utils.blur_faces import blur_faces
from utils.face_detector import detect_faces
from utils.image_loader import load_images, select_blur_level

def load_config():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.GOOGLE_APPLICATION_CREDENTIALS

def save_image(image, image_path):
    file_name = os.path.basename(image_path)
    file_folder = os.path.dirname(image_path)

    if not os.path.exists(file_folder + "/blurred_faces"):
        os.makedirs(file_folder + "/blurred_faces")
    
    new_path = os.path.join(file_folder + "/blurred_faces", file_name)
    ext = new_path.split(".")[-1]
    cv2.imencode("."+ext, image)[1].tofile(new_path)
    
if __name__ == "__main__":
    load_config()
    client = vision.ImageAnnotatorClient()
    
    images = load_images()
    blur_level = select_blur_level()
    print("\nBlur level: " + str(blur_level))
    print("Blurring faces...")
    
    for image_path in images:
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        
        faces = detect_faces(client, content)
        blured_image = blur_faces(content, faces, blur_level)
        save_image(blured_image, image_path)
        
        for face in faces:
            print(face.bounding_poly)
            print(face.bounding_poly.vertices)
    print("Blurred {} photos!".format(len(images)))
    print("Exiting...")
    sleep(1.5)