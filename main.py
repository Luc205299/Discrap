import requests
import json
import os
import time
import mysql.connector

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

# Check if the connection is successful
if conn.is_connected():
    print("Connected to MySQL database")
else:
    print("Unable to connect to MySQL database")

# Function to retrieve server information and channels
def retrieve_channel(serveur_id):
    headers = {
        'authorization': 'YOUR DISCORD KEY'
    }

    # Get channels for the server
    response = requests.get(f'https://discord.com/api/v9/guilds/{serveur_id}/channels', headers=headers)
    channels_data = json.loads(response.text)
    
    # Get server name
    server_info = requests.get(f'https://discord.com/api/v9/guilds/{serveur_id}', headers=headers)
    server_name = json.loads(server_info.text)['name']
    
    # Insert server data into the database if it doesn't exist
    cursor = conn.cursor()
    check_sql = "SELECT COUNT(*) FROM serveurs WHERE id = %s"
    cursor.execute(check_sql, (serveur_id,))
    result = cursor.fetchone()

    if result[0] == 0:  # If server doesn't exist, insert new record
        sql = "INSERT INTO serveurs (id, name) VALUES (%s, %s)"
        cursor.execute(sql, (serveur_id, server_name))
        conn.commit()
    else:
        print(f"Duplicate entry found for server {serveur_id}, skipping insertion.")

    print(cursor.rowcount, "record inserted.")
    cursor.close()

    # Create folder for the server and save channel information
    server_folder = f"server/{server_name}"
    if not os.path.exists(server_folder):
        os.mkdir(server_folder)

    with open(f"server/{server_name}/{server_name}.txt", "w", encoding="utf-8") as file:
        for channel in channels_data:
            try:
                channel_info = f"{channel['id']} : {channel['name']} : {channel['last_message_id']} : {channel['topic']} \n"
                
                # Insert channel data into the database if it doesn't exist
                cursor = conn.cursor()
                check_sql = "SELECT COUNT(*) FROM channel WHERE id = %s AND name = %s"
                cursor.execute(check_sql, (channel['id'], channel['name']))
                result = cursor.fetchone()

                if result[0] == 0:  # If channel doesn't exist, insert new record
                    sql = "INSERT INTO channel (id, name, server_id, topic) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (channel['id'], channel['name'], serveur_id, channel['topic']))
                    conn.commit()
                
                print(cursor.rowcount, "record inserted.")
                cursor.close()
                
                file.write(channel_info)
                
                # Request to get the channel details
                channel_details = requests.get(f'https://discord.com/api/v9/channels/{channel["id"]}', headers=headers)
                channel_permissions = json.loads(channel_details.text)
                
                # Skip channels with certain error codes
                if channel_permissions.get('code') == '10003':
                    continue
                else:
                    retrieve_message2(channel['id'], server_folder)
            except KeyError:
                pass  # Ignore missing fields

# Function to retrieve messages from a channel
def retrieve_message2(channel_id, server_folder):
    headers = {
        'authorization': 'YOUR DISCORD KEY'
    }
    last_message_id = None
    all_messages = []

    # Fetch messages in groups of 50
    while True:
        print(f"Taking messages before {last_message_id}")
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=50'
        if last_message_id:
            url += f"&before={last_message_id}"

        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print("Error", response.status_code, response.text)
            if response.status_code == 403 or (response.json().get("code") == 50001):
                print("Access denied, skipping channel")
                time.sleep(5)
            break
        
        try:
            messages = response.json()
        except json.decoder.JSONDecodeError:
            print("Error: Response is not JSON, skipping channel")
            break
                
        if len(messages) == 0:
            break
        
        all_messages.extend(messages)
        last_message_id = messages[-1]['id']

        time.sleep(1)

    # Get the channel name for file saving
    channel_info = requests.get(f'https://discord.com/api/v9/channels/{channel_id}', headers=headers)
    channel_name = json.loads(channel_info.text).get('name', channel_id)

    # Save the messages to a file
    with open(f"{server_folder}/{channel_name}.txt", "w", encoding="utf-8") as file:
        for message in all_messages:
            try:
                if isinstance(message, dict) and 'author' in message and isinstance(message['author'], dict):
                    message_text = f"{message['timestamp']} : {message['author']['id'], message['author']['username']} = {message['author'].get('global_name', '')} : {message['content']}\n"
                    
                    # Insert message data into the database
                    cursor = conn.cursor()
                    check_sql = "SELECT COUNT(*) FROM messages WHERE id = %s"
                    cursor.execute(check_sql, (message['id'],))
                    result = cursor.fetchone()

                    if result[0] == 0:  # If message doesn't exist, insert new record
                        sql = "INSERT INTO messages (id, content, author_id, name, pseudo_name, channel_id, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (message['id'], message['content'], message['author']['id'], message['author']['username'], message['author'].get('global_name', ''), channel_id, message['timestamp']))
                        conn.commit()
                        print(cursor.rowcount, "record inserted.")
                        cursor.close()

                    file.write(message_text)

                    # Check if user exists in the user database
                    user_info = requests.get(f'https://discordlookup.mesalytic.moe/v1/user/{message["author"]["id"]}', headers=headers)
                    user_data = json.loads(user_info.text)
                    
                    if user_data.get('code') == '10003':
                        continue
                    elif user_data.get('code') == '10013':
                        print(f"Unknown user for ID {message['author']['id']}. Error: {user_data['message']}")
                        continue
                    else:
                        cursor = conn.cursor()
                        check_sql = "SELECT COUNT(*) FROM users WHERE id = %s"
                        cursor.execute(check_sql, (message['author']['id'],))
                        result = cursor.fetchone()

                        if result[0] == 0:  # If user doesn't exist, insert new record
                            sql = "INSERT INTO users (id, name, pseudoname, created, pp) VALUES (%s, %s, %s, %s, %s)"
                            cursor.execute(sql, (message['author']['id'], user_data['username'], user_data['global_name'], user_data['created_at'], user_data['avatar']['link']))
                            conn.commit()
                            cursor.close()
            except KeyError as e:
                print(f"Missing key: {e}")

# Request server ID and start retrieval process
serveur_id = input("Enter the server id: ")
retrieve_channel(serveur_id)
