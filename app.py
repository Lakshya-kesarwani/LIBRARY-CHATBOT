from flask import Flask, request, jsonify, render_template
import os
import mysql.connector
import json
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

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

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Function to handle 'Show Available Books' intent
def show_available_books():
    if not cursor:
        return {"fulfillmentText": "Database connection error."}
    
    cursor.execute("SELECT title FROM BOOK_DETAILS WHERE availability = 'y';")
    books = cursor.fetchall()
    
    if not books:
        return {"fulfillmentText": "No books are currently available."}
    
    book_list = ", ".join([book["title"] for book in books])
    return {"fulfillmentText": f"Available books: {book_list}"}



# Function to recommend books based on genre


def recommend_books(genre):
    if not cursor:
        return {"fulfillmentText": "Database connection error."}
    
    cursor.execute("SELECT title FROM BOOK_DETAILS WHERE genre = %s", (genre,))
    books = cursor.fetchall()
    
    if not books:
        return {"fulfillmentText": "No books are currently available in this genre."}
    book_list = ", ".join([book["title"] for book in books])
    return {"fulfillmentText": f"Books in this genre: {book_list}"}
    
# Template function for future intents
def handle_custom_intent(intent,req):
    if intent == "Show Available Books":
        return show_available_books()
    elif intent == "Find Book by Genre":
        genre = req.get('queryResult', {}).get('parameters', {}).get('genre', "")
        print(genre)
        return recommend_books(genre)
    # Add more intent handling functions here
    return {"fulfillmentText": "I didn't understand that."}

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if not request.data:
            print("❌ No request data received!")
            return jsonify({"fulfillmentText": "No request data received."})

        raw_data = request.data.decode('utf-8')
        req = json.loads(raw_data)

        intent = req.get('queryResult', {}).get('intent', {}).get('displayName', "")
        response = handle_custom_intent(intent,req)
        return jsonify(response)
    
    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        return jsonify({"fulfillmentText": "Error parsing JSON request."})

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return jsonify({"fulfillmentText": "An unexpected error occurred."})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
