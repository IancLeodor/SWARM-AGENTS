from SUPABASE.create_client import get_client
from supabase import PostgrestAPIResponse


def upsert_phone_conversation(phone: str, location: str, conversation: list[str]) -> PostgrestAPIResponse:
    client = get_client()

    res = client.from_('phone_conversations').upsert({
        "number": phone,
        "location": location,
        "conversation": conversation
    }).execute()

    return res
