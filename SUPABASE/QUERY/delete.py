from SUPABASE.create_client import get_client
from supabase import PostgrestAPIResponse


def delete(table: str, condition: dict) -> PostgrestAPIResponse:
    client = get_client()

    return client.table(table).delete().eq(*list(condition.items())[0]).execute()
