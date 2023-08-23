from flask import Flask, request, jsonify, send_from_directory
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from generate_audio import get_audio
from bot import Bot

app = Flask(__name__)

ngrok_url = "50d4-71-127-239-78.ngrok-free.app"

# Your Twilio credentials
# account_sid = 'YOUR_ACCOUNT_SID'
# auth_token = 'YOUR_AUTH_TOKEN'
# twilio_phone_number = 'YOUR_TWILIO_PHONE_NUMBER'
# client = Client(account_sid, auth_token)

class Assistant:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.bot = Bot()
        self.conversation = []

    def process_message(self, message):
        self.conversation.append({"role": "user", "content": message})
        text_response = self.bot.get_completion(self.conversation)
        self.conversation.append({"role": "assistant", "content": text_response})
        audio_url = get_audio_url(text_response)
        print("Response:", text_response)
        print("Audio URL:", audio_url)
        return text_response, audio_url
    
assistants = {}

def get_audio_url(text):
    # Assuming your get_audio function saves the audio file in a directory named 'audio'
    words = text.split()[:3]
    filename = "_".join(words) + ".mp3"
    get_audio(text, filename)
    # Construct the URL where this audio will be accessible, assuming you're using ngrok or similar
    audio_url = f'http://{ngrok_url}/audio/{filename}'
    return audio_url

@app.route('/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    return send_from_directory('audio', filename)

@app.route('/sms', methods=['POST'])
def sms_reply():
    sender_number = request.values.get('From', '')
    incoming_message = request.values.get('Body', '').strip().lower()

    assistant = assistants.get(sender_number)
    if assistant is None:
        assistant = Assistant(sender_number)
        assistants[sender_number] = assistant

    reply_text, audio_url = assistant.process_message(incoming_message)

    print(reply_text)

    # Use TwiML to send the reply and include the audio URL as a media attachment
    response = MessagingResponse()
    response.message(reply_text)
    response.message().media(audio_url)
    # msg.media(audio_url)

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
