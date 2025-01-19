from qdrant_client import QdrantClient, models
import json

client = QdrantClient(url="http://localhost:6333", timeout=60)

FACE_COLLECTION_PATH = 'faces.json'
    
with open(FACE_COLLECTION_PATH) as f:
    face_collection_json = json.load(f)  

"""
This function:
- checks if the collection exists and if exists deletes
- creates the collection with the defined vector size and using the cosine distance
"""
def create_collection(collection, vector_size):
    print(f"Creating Collection {collection}")
    if(client.collection_exists(collection)):
        client.delete_collection(collection)
    result = client.create_collection(
        collection_name=collection,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE)
    )
    print("Create Collection Response")
    print(result)

"""
This function:
- Inserts all faces in the faces collection 
"""
def insert_faces():
    print(f"Inserting faces")
    result = client.upsert(
        collection_name="faces",
        points=[
            models.PointStruct(
                id=idx,
                vector=face["embedding"],
                payload={"entityId":face["entityId"],"entityName":face["entityName"], "imageId": face["id"]}
            )
            for idx, face in enumerate(face_collection_json)
        ]
    )
    print(result)


create_collection("faces", 512)
insert_faces()



