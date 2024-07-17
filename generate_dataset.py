import sqlite3
import os
import json
from datetime import datetime, timedelta

# Path to the iMessage database
db_path = os.path.expanduser('~/Library/Messages/chat.db')

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to get messages along with chat info
query = '''
SELECT
    message.rowid,
    message.text,
    message.date,
    message.is_from_me,
    message.attributedBody,
    message.version,
    chat.rowid,
    chat.chat_identifier,
    chat.display_name,
    handle.id AS sender
FROM
    message
LEFT JOIN
    chat_message_join ON message.rowid = chat_message_join.message_id
LEFT JOIN
    chat ON chat_message_join.chat_id = chat.rowid
LEFT JOIN
    handle ON message.handle_id = handle.rowid
ORDER BY
    message.date ASC
'''

# Execute the query
cursor.execute(query)
rows = cursor.fetchall()

# Query to get the number of participants in each chat
chat_participants_query = '''
SELECT
    chat.rowid AS chat_id,
    COUNT(chat_handle_join.handle_id) AS participant_count
FROM
    chat
LEFT JOIN
    chat_handle_join ON chat.rowid = chat_handle_join.chat_id
GROUP BY
    chat.rowid
'''

# Execute the query
cursor.execute(chat_participants_query)
chat_participants = cursor.fetchall()

# Create a dictionary to map chat_id to participant_count
chat_participant_dict = {chat_id: participant_count for chat_id, participant_count in chat_participants}

# Close the connection
conn.close()


# Function to convert Apple's timestamp to readable format
def apple_timestamp_to_datetime(timestamp):
    return datetime(2001, 1, 1) + timedelta(seconds=timestamp / 1e9)


# Handle message content
# credit: https://github.com/niftycode/imessage_reader/blob/master/imessage_reader/fetch_data.py
def parse_text(text, attributedBody):
    if version == 1:
        text = "<Message with no text, but an attachment.>"
        # the chat.db has some weird behavior where sometimes the text value is None
        # and the text string is buried in a binary blob under the attributedBody field.
    if text is None and attributedBody is not None:
        try:
            text = attributedBody.split(b"NSString")[1]
            text = text[
                   5:
                   ]  # stripping some preamble which generally looks like this: b'\x01\x94\x84\x01+'

            # this 129 is b'\x81, python indexes byte strings as ints,
            # this is equivalent to text[0:1] == b'\x81'
            if text[0] == 129:
                length = int.from_bytes(text[1:3], "little")
                text = text[3: length + 3]
            else:
                length = text[0]
                text = text[1: length + 1]
            text = text.decode()
        except Exception as e:
            print(e)

    return text


if __name__ == '__main__':
    # Process and collect the messages
    messages = []
    for row in rows:
        message_id, text, date, is_from_me, attributedBody, version, chat_rowid, chat_identifier, display_name, sender = row

        text = parse_text(text, attributedBody)

        date = apple_timestamp_to_datetime(date)
        is_group_chat = chat_participant_dict.get(chat_rowid,
                                                  1) > 1  # Consider it a group chat if it has more than one participant
        messages.append({
            'message_id': message_id,
            'text': text,
            'timestamp': date.isoformat(),
            'is_from_me': bool(is_from_me),
            'display_name': display_name,
            'is_group_chat': is_group_chat,
            'chat_identifier': chat_identifier
        })

    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the output file path relative to the current directory
    output_file = os.path.join(current_dir, 'imessages.jsonl')

    # Save messages to a JSON Lines file
    with open(output_file, 'w', encoding='utf-8') as f:
        for message in messages:
            f.write(json.dumps(message, ensure_ascii=False) + '\n')

    print(f"Messages saved to {output_file}")