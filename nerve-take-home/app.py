from flask import Flask, request, jsonify
import os
import uuid
import openai
from typing import List, Dict

app = Flask(__name__)

# OpenAI API Key
openai.api_key = "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"

# In-memory storage for chats and knowledge base
knowledge_base: List[str] = []
chats: Dict[str, List[Dict]] = {}

# To ingest file
@app.route('/ingest', methods=['POST'])
def ingest():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    # Save file content to the knowledge base
    file_content = file.read().decode('utf-8')
    knowledge_base.append(file_content)
    # Debugging line to print the current knowledge base
    print("Updated Knowledge Base:", knowledge_base)

    return jsonify({"success": True}), 200


# To create new chat
@app.route('/chat/new', methods=['POST'])
def new_chat():
    chat_id = str(uuid.uuid4())
    chats[chat_id] = []
    return jsonify({"chat_id": chat_id}), 201

# To get chat messages
@app.route('/chat/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    if chat_id not in chats:
        return jsonify({"error": "Chat ID not found"}), 404
    return jsonify({"chat_id": chat_id, "messages": chats[chat_id]}), 200

# To process user message and generate AI response
@app.route('/message', methods=['POST'])
def message():
    data = request.json
    chat_id = data.get('chat_id')
    user_input = data.get('input')

    if not chat_id or chat_id not in chats:
        return jsonify({"error": "Invalid or missing chat_id"}), 400
    if not user_input:
        return jsonify({"error": "Input message is required"}), 400

    # Combine knowledge base into context
    context = "\n".join(knowledge_base)
    messages = [
        {"role": "system", "content": "You are an AI assistant. Use the knowledge base for context."},
        {"role": "user", "content": f"Knowledge Base:\n{context}\n\n{user_input}"}
    ]

    try:
        # Generate response using OpenAI ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Updated model
            messages=messages,
            max_tokens=150
        )
        ai_response = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # To add messages to chat
    chat = chats[chat_id]
    message_id = len(chat) + 1
    chat.append({"message_id": message_id, "user_input": user_input, "ai_response": ai_response})

    return jsonify({"chat_id": chat_id, "message_id": message_id, "response": ai_response}), 200

if __name__ == '__main__':
    os.makedirs('knowledge_base', exist_ok=True)
    app.run(debug=True)