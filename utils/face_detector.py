from google.cloud.vision import ImageAnnotatorClient

def detect_faces(client: ImageAnnotatorClient, image_content):
    response = client.face_detection(image=image_content)
    return response.face_annotations