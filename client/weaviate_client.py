# weaviate_client.py
import weaviate
from config import WEAVIATE_URL, WEAVIATE_API_KEY, OPENAI_API_KEY


class WeaviateExecuter:
    CLASS_NAME = "DocChunk"

    def __init__(self):
        self.client = None

    def connect_client(self):
        client = weaviate.Client(
            url=WEAVIATE_URL,
            additional_headers={
                "X-OpenAI-Api-Key": OPENAI_API_KEY
            },
            auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)
        )
        return client

    def recreate_schema(self):
        self.delete_schema()
        self.create_schema()

    def create_schema(self):
        schema = {
            "classes": [
                {
                    "class": self.CLASS_NAME,
                    "description": "Chunks of documents",
                    "vectorizer": "text2vec-openai",
                    "properties": [
                        {
                            "name": "content",
                            "dataType": ["text"]
                        },
                        {
                            "name": "docName",
                            "dataType": ["text"]
                        },
                        {
                            "name": "chunkIndex",
                            "dataType": ["int"]
                        }
                    ]
                }
            ]
        }
        client = self.connect_client()

        existing_classes = [c["class"] for c in client.schema.get()["classes"]]
        if self.CLASS_NAME not in existing_classes:
            client.schema.create(schema)
            print(f"'{self.CLASS_NAME}' sınıfı Weaviate'a başarıyla eklendi!")
        else:
            print(f"'{self.CLASS_NAME}' sınıfı zaten Weaviate'da mevcut.")

    def delete_schema(self):
        client = self.connect_client()
        client.schema.delete_all()
        print("Weaviate'daki tüm sınıflar silindi!")

    def upload_chunks(self, chunks, doc_name):
        client = self.connect_client()
        with client.batch as batch:
            batch.batch_size = 200
            for (i, chunk) in chunks:
                data = {
                    "content": chunk,
                    "docName": doc_name,
                    "chunkIndex": i
                }
                batch.add_data_object(
                    data_object=data,
                    class_name=self.CLASS_NAME
                )
        print(f"{doc_name} adlı belge başarıyla yüklendi.")

    def semantic_search(self, query_text, top_k=3):
        client = self.connect_client()
        response = (
            client.query
            .get(self.CLASS_NAME, ["content", "docName", "chunkIndex"])
            .with_near_text({"concepts": [query_text]})
            .with_limit(top_k)
            .do()
        )

        result = response.get("data", {}).get("Get", {}).get(self.CLASS_NAME, [])
        return result
