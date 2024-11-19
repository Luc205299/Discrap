# Discord Server and Message Fetcher

This project allows you to retrieve information from a Discord server, including channels, messages, and user data, and store it in a MySQL database. It also saves the fetched messages in text files within a structured folder for further analysis.

## Features

- **Fetch Server Channels**: Retrieve all the channels within a specific Discord server.
- **Fetch Messages**: Retrieve messages from the channels of a Discord server.
- **User Data**: Fetch detailed user information (username, global name, avatar, etc.) for the authors of the messages.
- **Database Integration**: Store server, channel, message, and user data in a MySQL database.
- **Save Data in Files**: Save the messages and channel data as text files in structured folders.

## Prerequisites

Before running this project, you need to have:

- Python 3.x
- MySQL server running with a database created for storing the data
- A Discord Bot Token with the necessary permissions (`YOUR DISCORD KEY`)
- Installed libraries: `requests`, `mysql-connector-python`, and `json`

## Setup Instructions

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/discord-server-fetcher.git
   
2. Install Python Libraries:
   You need to install the required Python libraries. Navigate to the project directory and run:
   ```bash
   pip install requests mysql-connector-python
   
3. Configure the Script:
   Open the Python script discord_fetcher.py and do the following:
   ```python
   conn = mysql.connector.connect(
    host="your_mysql_host",
    user="your_mysql_user",
    password="your_mysql_password",
    database="discord_data"
   )
   ```
   Replace the YOUR DISCORD KEY with your actual Discord Bot Token in both places within the script:
   ```
   headers = {
    'authorization': 'YOUR DISCORD KEY'
   }
   ```
   Dont forget to adapt the script to your database!!

   ```python
   sql = "INSERT INTO messages (id, content, author_id, name, pseudo_name, channel_id, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
   ```
This project is licensed under the MIT License - see the LICENSE.txt file for details.


**Warning: Compliance with Discord's Terms of Service**

Using this project involves collecting data from Discord servers, including messages, user information, and channel details. Before using this bot to fetch data from a Discord server, you must **ensure that you comply with Discord's Terms of Service (ToS)** and **Privacy Policy**.

**Discord ToS**: https://discord.com/terms  
**Discord Privacy Policy**: https://discord.com/privacy

Here are some important points to consider:

- **Obtain Consent**: You must obtain explicit permission from server admins and members before collecting data from a server. Using this script without consent may violate Discord's rules and result in the suspension of your account or bot.

- **Data Collection**: This script collects sensitive information such as private messages, user IDs, and metadata. Ensure that you are not collecting sensitive personal data or doing so in an intrusive manner.

- **Usage Restrictions**: Do not use this bot to collect data in an abusive or intrusive manner, or for purposes other than specified. Any data collection must comply with data protection laws, such as GDPR (General Data Protection Regulation) if you are in Europe.
   
