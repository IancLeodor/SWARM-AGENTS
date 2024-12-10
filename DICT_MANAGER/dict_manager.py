import json
from env import load_dotenv
import os
from SWARM.create_agent import catalin_pop, supabase_db_agent

load_dotenv()

dict_path = os.getenv('DICT_PATH')

# A mapping of function names to actual function objects
function_map = {
    'catalin_pop': catalin_pop,
    'database_agent': supabase_db_agent
}

address_dict = {}


def create_file_dict() -> bool:
    try:
        if not os.path.exists(dict_path):
            with open(dict_path, 'w') as file_dic:
                file_dic.write('{}')
            return True

        with open(dict_path, 'r+') as file_dic:
            try:
                json.load(file_dic)
            except json.JSONDecodeError:
                file_dic.seek(0)
                file_dic.write('{}')
                file_dic.truncate()
            return True
    except Exception as e:
        print(e)
        return False


def read_file_dict() -> dict:
    try:
        global address_dict
        with open(dict_path, 'r') as file_dic:
            address_dict = json.load(file_dic)
            return address_dict
    except Exception as e:
        print(e)
        return {}


def write_file_dict(remote_address, user, agent_name, history=None) -> bool:
    try:
        global address_dict
        with open(dict_path, 'r') as file_dic:
            address_dict = json.load(file_dic)

        if history is None:
            history = []

        if remote_address not in address_dict:
            address_dict[remote_address] = {}

        address_dict[remote_address][user] = {"agent": agent_name, "history": history}

        with open(dict_path, 'w') as file_dic:
            json.dump(address_dict, file_dic, indent=4)

        return True
    except Exception as e:
        print(e)
        return False


def get_agent_by_name(agent_name):
    """Return the function object based on the function name"""
    if agent_name in function_map:
        return function_map[agent_name]
    else:
        raise ValueError(f"Agent function '{agent_name}' not found in function_map")
