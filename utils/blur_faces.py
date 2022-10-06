from io import StringIO
from PIL import Image
import numpy as np
import cv2

def blur_faces(image_content, faces, blur_level=1):
    image = Image.open(StringIO(image_content))
    image = np.array(image)
    # flip RGB channel for PIL-OpenCV compatibility
    image = image[:, :, ::-1]
    for face in faces:
        box = [(bound.x.coordinate, bound.y.coordinate) for bound in face.bounds.vertices]
        top_left = box[0]
        bottom_right = box[2]
        x = top_left[0]
        y = top_left[1]
        w = bottom_right[0] - x
        h = bottom_right[1] - y
        
        roi = image[y:y+h, x:x+w]
        roi_blurred = cv2.blur(roi, (blur_level+5, blur_level+5))
        image[y:y+h, x:x+w] = roi_blurred
        
    return image