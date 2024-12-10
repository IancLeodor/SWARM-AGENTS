from SUPABASE.create_client import get_client
from supabase import PostgrestAPIResponse


def insert(table: str, values: dict) -> PostgrestAPIResponse:
    client = get_client()

    return client.table(table).insert(values).execute()
