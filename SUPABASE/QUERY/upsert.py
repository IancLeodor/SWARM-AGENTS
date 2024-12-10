from SUPABASE.create_client import get_client
from supabase import PostgrestAPIResponse


def upsert(table: str, values: dict) -> PostgrestAPIResponse:
    client = get_client()

    return client.table(table).upsert(values).execute()
