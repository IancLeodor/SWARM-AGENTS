from SUPABASE.create_client import get_client
from supabase import PostgrestAPIResponse


def update(table: str, values: dict, condition: dict) -> PostgrestAPIResponse:
    client = get_client()

    return client.table(table).update(values).eq(*list(condition.items())[0]).execute()
