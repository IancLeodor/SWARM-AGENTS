from flask import Flask, request
import os
from main import talk
from env import load_dotenv
from DICT_MANAGER.dict_manager import create_file_dict
from flask_cors import CORS

load_dotenv()

create_file_dict()

openai_key = os.getenv('OPENAI_API_KEY')
flask_host = os.getenv('FLASK_IP')
flask_port = os.getenv('FLASK_PORT')

app = Flask(__name__)
app.logger.setLevel('DEBUG')
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.post('/')
def home():
    req_data = request.get_json()
    content = req_data.get('content')
    agent = req_data.get('agent', 'catalin_pop')
    location = req_data.get('location', 'default')
    phone = req_data.get('phone', 'default')

    return talk(content, agent, location, phone)


if __name__ == '__main__':
    app.run(flask_host, flask_port, debug=True)
