from dotenv import load_dotenv
import os
load_dotenv()

# Elastic Search
ES_NAME = os.getenv("ES_NAME")
ES_CLOUD_ID = os.getenv("ES_CLOUD_ID")
ES_API_KEY = os.getenv("ES_API_KEY")