## Overview
This application implements a real backend service with a REST API to manage a Retrieval-Augmented Generation (RAG) system. The system allows users to interact with an AI that can tap into a knowledge base ingested from files.

## Requirements
- Python 3.x
- Flask
- OpenAI API key

## Setup Instructions
1. Clone the repository to your local machine.
2. Install dependencies: 
3. Run the Flask application:


## API Endpoints

### POST /ingest
- **Description**: Ingests a file into the knowledge base.
- **Request**: Multipart-form data with a file (e.g., `test.txt`).
- **Response**: Returns a `True` status on success.

### POST /chat/new
- **Description**: Creates a new chat session.
- **Response**: Returns a `chat_id`.

### GET /chat/<chat_id>
- **Description**: Retrieves the messages in a specified chat.
- **Response**: Returns a list of messages.

### POST /message
- **Description**: Sends a message in the chat and gets a response from the AI.
- **Request**: JSON with `chat_id` and `input`.
- **Response**: Returns the AI's response.

## Running the Application
After setting up, you can start the Flask server and access the API on `http://127.0.0.1:5000`.