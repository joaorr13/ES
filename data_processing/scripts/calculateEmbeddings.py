import tempfile
from retinaface import RetinaFace
from PIL import Image
from deepface import DeepFace
import json
import os


def preprocess_image(img_path, entityId, entityName):
    try:
        result = {}
        faces = RetinaFace.detect_faces(img_path)
        if(len(faces.items()) > 1):
            print(img_path + " found " + len(faces.items()) + " faces")
        for face_key, face_data in faces.items():
            cropped_img_path = extract_image(img_path, face_data["facial_area"])
            embedding = represent_faces(cropped_img_path)
            result["embedding"] = embedding
            result["entityId"] = entityId
            result["entityName"] = entityName
            os.remove(cropped_img_path)
            break #Assume there's only one face per image, only process the first identified
        return result
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


def process_entities(json_file_path, photos_base_path):
    notFoundArray = []
    numberProcessed = 0
    faces = []
    with open(json_file_path, "r") as json_file:
        entities = json.load(json_file) 

    size = len(entities)
    
    for entity in entities:
        entity_id = entity["id"]
        entity_name = entity["name"]
        entity_folder = os.path.join(photos_base_path, entity_id)
        
        if not os.path.exists(entity_folder):
            notFoundArray.append(entity_id)
            continue
        
        for file_name in os.listdir(entity_folder):
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(entity_folder, file_name)
                image_id = file_name.split(".")[0]
                face_id = entity_id + '/' + image_id
                result = preprocess_image(img_path, entity_id, entity_name)
                if result:
                    result['id'] = face_id
                    faces.append(result)
        numberProcessed += 1
        print(str(numberProcessed) + " of " + str(size)  + " processed")

           

    with open("faces.json", "w") as faces_file:
        json.dump(faces, faces_file, indent=4)
    
    print("Total number Ids:", len(entities))
    print("Not found Ids:")
    print(notFoundArray)
    print("Not found size:", len(notFoundArray))

def main():
    json_file_path = "../initial_data/players.json"  
    photos_base_path = "../initial_data/photos" 

    process_entities(json_file_path, photos_base_path)


if __name__ == "__main__":
    main()
