import json

def save_control_buttons_message_id(message_id):
    """Saves the message ID of the server control buttons for future reference."""
    try:
        with open('core/server_control_message_id.json', 'w') as file:
            json.dump({'message_id': message_id}, file)
    except Exception as e:
        print(f"Error saving server control buttons message ID: {e}")
        # Consider adding logging here if necessary
