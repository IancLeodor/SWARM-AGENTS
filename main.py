import json

from DICT_MANAGER.dict_manager import write_file_dict, read_file_dict, get_agent_by_name, create_file_dict
from SWARM.create_swarm import get_swarm
from SUPABASE.upsert_conversation import upsert_phone_conversation
from env import load_dotenv
from numpy import concatenate

load_dotenv()


def talk(content, agent, location, phone):
    create_file_dict()
    try:
        address_dict = read_file_dict()

        if not content:
            return ""

        # If the address or user is new, initialize with the agent and empty history
        if location not in address_dict or phone not in address_dict[location]:
            write_file_dict(location, phone, agent, history=[])
            address_dict = read_file_dict()

        # Get the agent and history for the specific user under this address
        user_data = address_dict[location].get(phone, {})
        agent_name = user_data.get("agent")

        if not agent_name:
            raise ValueError(f"Agent name not found for user '{phone}' at address '{location}'")

        agent = get_agent_by_name(agent_name)
        history = user_data.get("history", [])

        if agent is None:
            raise ValueError(f"Agent function '{agent_name}' not found")

        # Append the new message to the conversation history
        history.append({"role": "user", "content": content})

        print(f"AGENT: {agent_name} : {agent}")

        # try:
        # Run the conversation using the updated history
        response = get_swarm().run(
            agent=agent(),
            messages=history
        )

        ai_messages = response.messages

        history = history + ai_messages

        # Save the updated history back to the file for the user at this address
        write_file_dict(location, phone, agent_name, history=history)
        upsert_phone_conversation(phone, location, history)
        content_only = [message["content"] for message in ai_messages]

        return content_only
    except Exception as e:
        return f'ERROR: {e}'
