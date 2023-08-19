import os, sys

import weaviate
from weaviate.embedded import EmbeddedOptions

class WeaviateWrapper:
    def __init__(self) -> None:
        # Get the WEAVIATE_API_KEY from the environment
        weaviate_apikey = os.environ.get('WEAVIATE_API_KEY')
        # Get the WEAVIATE_ENDPOINT from the environment
        weaviate_endpoint = os.environ.get('WEAVIATE_ENDPOINT')

        # Instantiate the client with the auth config
        auth_config = weaviate.AuthApiKey(api_key=weaviate_apikey)
        client = weaviate.Client(
            url=weaviate_endpoint,
            auth_client_secret=auth_config
        )

        # Simple test to see if the client is connected
        try:
            client.get_meta()
        except weaviate.UnexpectedStatusCodeException as e:
            sys.stderr.write("Error connecting to Weaviate: {}".format(e))
            sys.exit(1)
