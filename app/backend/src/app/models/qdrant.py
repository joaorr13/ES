from qdrant_client import models
from ..extensions import qdrant

def qdrant_search(embedding):
    result = qdrant.search(
        collection_name="faces",
        search_params=models.SearchParams(hnsw_ef=128, exact=False), 
        query_vector=embedding,
        with_payload=True,
        limit=1,
    )
    print(result[0].payload)
    return result[0].payload