import os, sys, json

import weaviate
import openai
from weaviate.embedded import EmbeddedOptions

openai.api_key = os.environ.get('OPENAI_API_KEY')
embedding_model="text-embedding-ada-002"

class WeaviateWrapper:
    def __init__(self) -> None:
        # Get the WEAVIATE_API_KEY from the environment
        weaviate_apikey = os.environ.get('WEAVIATE_API_KEY')
        # Get the WEAVIATE_ENDPOINT from the environment
        weaviate_endpoint = os.environ.get('WEAVIATE_ENDPOINT')
        # Get the OPENAI_API_KEY from the environment
        openai_apikey = os.environ.get('OPENAI_API_KEY')

        # Instantiate the client with the auth config
        auth_config = weaviate.AuthApiKey(api_key=weaviate_apikey)
        self.client = weaviate.Client(
            url=weaviate_endpoint,
            auth_client_secret=auth_config,
            additional_headers = {
                "X-OpenAI-Api-Key": openai_apikey,
            },
        )

        # Simple test to see if the client is connected
        try:
            print(self.client.get_meta())
        except weaviate.UnexpectedStatusCodeException as e:
            sys.stderr.write("Error connecting to Weaviate: {}".format(e))
            sys.exit(1)
    
    def insert_one(self, class_name, data_object):
        oai_resp = openai.Embedding.create(input = [json.dumps(data_object)], model=embedding_model)
        uuid = self.client.data_object.create(
            data_object=data_object,
            class_name=class_name,
            vector=oai_resp['data'][0]['embedding'],
        )
        return uuid
    
    def _generate_embedding(self, text):
        oai_resp = openai.Embedding.create(input = [text], model=embedding_model)
        return oai_resp['data'][0]['embedding']
    
    def run_near_query(self, class_name, query, k=10):
        vector = self._generate_embedding(query)
        result = self.client.query.get(class_name, ["content"]).with_near_vector({"vector": vector}).with_limit(k).do()
        return result

    def delete_class(self, class_name):
        self.client.schema.delete_class(class_name=class_name)
    
    def dump(self):
        result = self.client.data_object.get()
        return result["objects"]

# Sample usage:
# weaviate = WeaviateWrapper()
# weaviate.insert_one("test_class", {"content": "The hills are flat... the water is dry... who the heck talks like this?" })
# weaviate.insert_one("test_class", {"content": "Sulfiric acid has many uses in metallurgy." })
# weaviate.insert_one("test_class", {"content": "The carpenters are in need of more 2x4s" })
# print(weaviate.run_near_query("test_class", "chemistry", 1))
# weaviate.delete_class("test_class")
# print(weaviate.dump())
