import os

from supabase import create_client, Client
from env import load_dotenv

load_dotenv()

supabase_url: str = os.environ.get('SUPABASE_URL')
supabase_api_key: str = os.environ.get('SUPABASE_API_KEY')

client: Client = create_client(supabase_url, supabase_api_key)


def get_client() -> Client:
    global client
    return client
