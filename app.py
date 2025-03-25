from flask import Flask, request, jsonify,render_template
import os
import mysql.connector
import json
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user='avnadmin',
        password=os.getenv('DB_PASSWORD'),
        database='chatbot_library',
        port=26060
    )
    cursor = conn.cursor(dictionary=True)
    print("✅ Database connected successfully!")
except mysql.connector.Error as err:
    print(f"❌ Database connection error: {err}")

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Check if request has JSON data
        if not request.data:
            print("❌ No request data received!")
            return jsonify({"fulfillmentText": "No request data received."})

        # Decode raw request data
        raw_data = request.data.decode('utf-8')
        # print("🔍 Raw Request Data:", raw_data)

        # Parse JSON safely
        req = json.loads(raw_data)
        # print("✅ Parsed JSON:", req)

        # Extract intent name
        intent = req.get('queryResult', {}).get('intent', {}).get('displayName', "")

        if intent == "Show Available Books":
            cursor.execute("SELECT title FROM BOOK_DETAILS WHERE availability = 'y';")
            books = cursor.fetchall()
            print(books)
            if not books:
                return jsonify({"fulfillmentText": "No books are currently available."})

            book_list = ", ".join([book["title"] for book in books])
            return jsonify({"fulfillmentText": f"Available books: {book_list}"})

        return jsonify({"fulfillmentText": "I didn't understand that."})

    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        return jsonify({"fulfillmentText": "Error parsing JSON request."})

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return jsonify({"fulfillmentText": "An unexpected error occurred."})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
