from flask import Blueprint, request, jsonify, make_response
from config import Config
import tempfile
import os
import requests
from ..models.qdrant import qdrant_search
from retinaface import RetinaFace
from PIL import Image
from deepface import DeepFace





"""
This function:
- Checks if the urls are valid for a picture(png,jpg,jpeg)
- Downloads the image for a tmp file (stores the path in img_path)
- Calls the function responsible for the recognition
- Deletes the tmp file
"""
def build_response(url):
    
    if url.lower().endswith(('.png', '.jpg', '.jpeg')):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(url)[1]) as tmp_file:
                    tmp_file.write(response.content)
                    img_path = tmp_file.name 
                
                
                faces_recognition_result = recognize_faces(img_path)
                
                img_response = {
                    "faces": faces_recognition_result,
                    "url": url
                }
                
                delete_temp_file(img_path)
            else:
                img_response = {"imageURL": url, "status": "Inaccessible"}
        except Exception as e:
            img_response = {"imageURL": url, "status": "Inaccessible"}
            with open("/tmp/error.txt", "w") as f:
                f.write(str(e))

    else:
        img_response = {"imageURL": url, "status": "Unsupported file type"}
        


    return img_response


def recognize_faces(img_path):
    faces_embeddings = preprocess_image(img_path)

    faces_recongitions = []

    for face in faces_embeddings:
        face_recognition_result = qdrant_search(face["embedding"])
        if face_recognition_result != None:

            #Information to return in the response body 
            face_info_response = {
                "coordinates": {
                    "x": int(face["facial_area"][0]),
                    "y": int(face["facial_area"][1]),
                    "width": int(face["facial_area"][2]),
                    "height": int(face["facial_area"][3])
                },
                "imageMatch": face_recognition_result["imageId"],
                "entityId":face_recognition_result["entityId"],
                "entityName":face_recognition_result["entityName"]
            }
            faces_recongitions.append(face_info_response)
        else:
            faces_recongitions.append({
                "coordinates": {
                    "x": face["facial_area"][0],
                    "y": face["facial_area"][1],
                    "width": face["facial_area"][2],
                    "height": face["facial_area"][3]
                },
                "message": "Couldnt find an entity for this face"
            })
    return faces_recongitions


def preprocess_image(img_path):
    response = []
    try:
        faces = RetinaFace.detect_faces(img_path)
        for face_key, face_data in faces.items():
            cropped_img_path = extract_image(img_path, face_data["facial_area"])
            embedding = represent_faces(cropped_img_path)
            face_data["embedding"] = embedding
            response.append(face_data)
        return response
    except Exception as e:
        return None
    
def extract_image(img_path, bbox):
    # Open the image
    image = Image.open(img_path)

    # Extract the specified region
    cropped_image = image.crop(bbox)

    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    cropped_image.save(temp_file.name)

    # Close the file
    temp_file.close()

    return temp_file.name


"""
This function uses Facenet512 to represent images as a multidimensional vector(embedding).
"""
def represent_faces(img_path):
    try:
        embedding_obj = DeepFace.represent(
            img_path = img_path,
            model_name = "Facenet512",
            detector_backend='skip'
        )
        return embedding_obj[0]["embedding"]
    except Exception as e:

        return []




def delete_temp_file(file_path):
    try:
        os.remove(file_path)
        print(f"Temporary file '{file_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"Temporary file '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


