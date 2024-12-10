from env import load_dotenv
from openai import Client
import os

load_dotenv()

client = Client(
    api_key=os.getenv('OPENAI_API_KEY')
)


def create_client():
    global client
    return client
