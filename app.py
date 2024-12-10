# app.py

from flask import Flask, request, Response
from flask_socketio import SocketIO, emit
import os
from main import talk  # Import the talk function that interacts with Swarm agents
from env import load_dotenv
from DICT_MANAGER.dict_manager import create_file_dict
from flask_cors import CORS
import json
import base64
import speech_recognition as sr
from gtts import gTTS
import io
from pydub import AudioSegment
import eventlet

# Monkey patching for compatibility with eventlet
eventlet.monkey_patch()

# Load environment variables
load_dotenv()

# Initialize conversation dictionaries
create_file_dict()

# Retrieve environment variables
flask_host = os.getenv('FLASK_IP', '0.0.0.0')
flask_port = int(os.getenv('FLASK_PORT', 2000))

# Initialize Flask app
app = Flask(__name__)
app.logger.setLevel('DEBUG')
CORS(app, resources={r"/api/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

recognizer = sr.Recognizer()

def decode_audio(base64_audio):
    audio_data = base64.b64decode(base64_audio)
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")
    return audio_segment

def encode_audio(text):
    tts = gTTS(text=text, lang='ro') 
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    audio = AudioSegment.from_file(fp, format="mp3")
    
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)
    
    # Encode WAV audio to base64
    return base64.b64encode(wav_io.read()).decode('utf-8')

@app.route('/incoming-call', methods=['GET', 'POST'])
def incoming_call():
    """
    Endpoint to handle incoming and outgoing calls via Twilio.
    Returns TwiML XML instructing Twilio to connect to the media stream WebSocket.
    """
    host = request.headers.get('host')
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Pause length="1"/>
    <Say voice="alice" language="ro-RO">Salut! Vă rog să așteptați în timp ce vă conectăm la asistentul nostru AI.</Say>
    <Connect>
        <Stream url="wss://{host}/media-stream" />
    </Connect>
</Response>"""
    return Response(twiml_response, mimetype='text/xml')

@socketio.on('connect', namespace='/media-stream')
def handle_connect():
    app.logger.info('Client connected to /media-stream')
    emit('connected', {'data': 'Connected to server'})

@socketio.on('media', namespace='/media-stream')
def handle_media(data):
    """
    Handle incoming media from Twilio, process it, and send response back.
    """
    # Spawn a new green thread to handle media to avoid blocking
    eventlet.spawn_n(process_media, data)

def process_media(data):
    try:
        # Extract audio payload from data
        payload = data.get('media', {}).get('payload')
        if not payload:
            app.logger.error('No payload found in media data.')
            return

        # Decode and process audio
        audio_segment = decode_audio(payload)

        # Convert AudioSegment to a format suitable for Speech Recognition
        with io.BytesIO() as wav_io:
            audio_segment.export(wav_io, format="wav")
            wav_io.seek(0)
            with sr.AudioFile(wav_io) as source:
                audio = recognizer.record(source)
                try:
                    # Perform Speech-to-Text (STT) using Google's API
                    text = recognizer.recognize_google(audio, language='ro-RO')
                    app.logger.info(f"Transcribed Text: {text}")
                except sr.UnknownValueError:
                    app.logger.error("Google Speech Recognition could not understand audio")
                    text = ""
                except sr.RequestError as e:
                    app.logger.error(f"Could not request results from Google Speech Recognition service; {e}")
                    text = ""

        if text:
            # Communicate with Swarm agents using the talk function
            response = talk(content=text, agent='catalin_pop', location='default', phone='default')
            
            if isinstance(response, list):
                response_text = ' '.join(response)
            else:
                response_text = response

            app.logger.info(f"Agent Response: {response_text}")

            # Convert response text to audio
            response_audio = encode_audio(response_text)

            # Send audio back to Twilio
            emit('media', {'event': 'media', 'media': {'payload': response_audio}}, namespace='/media-stream')
    except Exception as e:
        app.logger.error(f"Error handling media: {e}")

@socketio.on('disconnect', namespace='/media-stream')
def handle_disconnect():
    app.logger.info('Client disconnected from /media-stream')

if __name__ == '__main__':
    socketio.run(app, host=flask_host, port=flask_port, debug=True)
