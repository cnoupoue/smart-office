import requests
import json
import env
import time 

# Room ID for "ubuntu serveur"

messages_url = f'https://webexapis.com/v1/messages?roomId={env.WEBEX_ROOM_ID_FOR_COMMANDS}'
headers = {
    'Authorization': f'Bearer {env.WEBEX_TOKEN}',
    'Content-Type': 'application/json'
}

# Function to send a message to the room
def send_message(text):
    message_url = 'https://webexapis.com/v1/messages'
    message_data = {
        'roomId': env.WEBEX_ROOM_ID_FOR_COMMANDS,
        'text': '[BOT]: ' + text
    }
    response = requests.post(message_url, headers=headers, data=json.dumps(message_data))
    print(f'Message sent: {response.status_code} {text}')

def _get_last_message():
    global messages_url
    response = requests.get(messages_url, headers=headers)
    messages = response.json()['items']
    return messages[0]

# Main loop to listen for messages
last_message_id= None

def init():
    _get_last_message()['id']

def wait_for_command():
    while True:
        current_message = _get_last_message()
        is_new_messages = current_message['id'] != last_message_id

        if is_new_messages:
            return current_message['text']

        time.sleep(env.WEBEX_LAST_MESSAGE_READ_DELAY)

