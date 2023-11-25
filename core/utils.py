import json

def save_embed_message_id(message_id):
    with open('core/embed_message_id.json', 'w') as file:
        json.dump({'message_id': message_id}, file)
