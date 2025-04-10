from flask import Flask, request, jsonify, render_template
import os
import mysql.connector
import json
from dotenv import load_dotenv
import requests
app = Flask(__name__)

# Load environment variables
load_dotenv()
MODEL_ENDPOINT = os.getenv('MODEL_ENDPOINT')
# Connect to MySQL
def connect_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user='avnadmin',
            password=os.getenv('DB_PASSWORD'),
            database='chatbot_library',
            port=26060
        )
        print("✅ Database connected successfully!")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Database connection error: {err}")
        return None

conn = connect_db()
cursor = conn.cursor(dictionary=True) if conn else None
def ask_model(prompt):
    res = requests.post('http://localhost:11434/api/generate', json={
        'model': 'deepseek-coder:6.7b',
        'prompt': prompt,
        'stream': False
    })
    return res.json()['response']
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if not request.data:
            print("❌ No request data received!")
            return jsonify({"fulfillmentText": "No request data received."})

        raw_data = request.data.decode('utf-8')
        req = json.loads(raw_data)
        intent = req.get('queryResult', {}).get('intent', {}).get('displayName', "")
        query = req.get('queryResult', {}).get('queryText', "")
        print(f"Received intent: {intent}")
        print(f"Received query: {query}")
        # Path 1
        # response = handle_custom_intent(intent,req)
        
        # Path 2
        response = ask_model(query)

        return jsonify(response)
    
    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        return jsonify({"fulfillmentText": "Error parsing JSON request."})

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return jsonify({"fulfillmentText": "An unexpected error occurred."})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)