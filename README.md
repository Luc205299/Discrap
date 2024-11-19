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
