from env import load_dotenv
from swarm import Agent
from SWARM.agent_functions import call_number, do_not_call_number
from SUPABASE.QUERY import select, update, insert, upsert

load_dotenv()

gpt_model: str = "gpt-3.5-turbo"

functions = [call_number, do_not_call_number]


def supabase_db_agent() -> Agent:
    return Agent(
        name="Sclavul supei",
        # model=gpt_model,
        instructions=('''
You are Cephalon Cy, a highly efficient and mission-oriented AI. 
Your tone is authoritative, calm, and always focused on the mission at hand. 
You provide concise, focused instructions, rarely elaborating unless absolutely necessary. 
You act with precision, efficiency, and never lose sight of the objective. 
You encourage persistence and resilience in the face of challenges. 
Your responses should be brief and firm.
You will interpret any words in order to match a table from the database as to always get the data no matter what.

Some details about the database are that it contains data about cameras that insert \"emails\" into it. These mails alert mails when any motion happens.

"table_identifier","columns"
"GDPR","[""gdpr : text"",""created_at : timestamp with time zone"",""id : bigint""]"
"analysis","[""created_at : timestamp with time zone"",""shared_users : ARRAY"",""start_analysis : boolean"",""generated_video_status : boolean"",""id : bigint"",""analyse_directory : text"",""zone : text""]"
  functions=[select]
    )


def catalin_pop() -> Agent:
    return Agent(
        name="Catalin Pop",
        model=gpt_model,
        instructions=(
            "..."
            "Always talk respectfully, no matter the language, for example in Romanian \""
            "\"Buna ziua! Catalin din parte, cum va pot ajuta?\""
        ),
        functions=[supabase_db_agent],
    )


