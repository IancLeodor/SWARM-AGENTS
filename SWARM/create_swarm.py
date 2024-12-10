from swarm import Swarm
from OPENAI.create_client import create_client

client = create_client()
swarm = Swarm(client=client)


def get_swarm() -> Swarm:
    global swarm
    return swarm
