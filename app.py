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
    
    cursor.execute("SELECT title FROM books_details")
    books = cursor.fetchall()
    
    if not books:
        return {"fulfillmentText": "No books are currently available."}
    
    book_list = ", ".join([book["title"] for book in books])
    return {"fulfillmentText": f"Available books: {book_list}"}

# Function to recommend books based on genre
def books_bygenre(genre):
    if not cursor:
        return {"fulfillmentText": "Database connection error."}
    
    cursor.execute("SELECT title FROM BOOK_DETAILS WHERE genre = %s", (genre,))
    books = cursor.fetchall()
    
    if not books:
        return {"fulfillmentText": "No books are currently available in this genre."}
    book_list = ", ".join([book["title"] for book in books])
    return {"fulfillmentText": f"Books in this genre: {book_list}"}

# Function to locate a book by ISBN
def locate_book(isbn):
    if not cursor:
        return {"fulfillmentText": "Database connection error."}
    
    cursor.execute("SELECT title FROM BOOK_DETAILS WHERE isbn = %s", (isbn,))
    books = cursor.fetchall()

    if not books:
        return {"fulfillmentText": "No books are currently available with this ISBN."}
    book_list = ", ".join([book["title"] for book in books])
    return {"fulfillmentText": f"Books with this ISBN: {book_list}"}

# Function to recommend books based on author
def books_byauthor(author):
    if not cursor:
        return {"fulfillmentText": "Database connection error."}
    
    cursor.execute("SELECT title FROM BOOK_DETAILS WHERE author = %s", (author,))
    books = cursor.fetchall()

    if not books:
        return {"fulfillmentText": "No books are currently available by this author."}
    book_list = ", ".join([book["title"] for book in books])
    return {"fulfillmentText": f"Books by this author: {book_list}"}

# Function to handle general queries with multiple parameters
def general_query(req):
    if not cursor:
        return {"fulfillmentText": "Database connection error."}
    query = "SELECT * FROM books_details WHERE 1=1"
    values = []
    
    # Extract parameters from request
    genre = req.get('queryResult', {}).get('parameters', {}).get('genre', [])
    author = req.get('queryResult', {}).get('parameters', {}).get('author', [])
    isbn = req.get('queryResult', {}).get('parameters', {}).get('isbn', [])
    availability = req.get('queryResult', {}).get('parameters', {}).get('availability', [])
    book_status = req.get('queryResult', {}).get('parameters', {}).get('book_status', [])

    # Ensure all parameters are lists (if they are single values, wrap them in a list)
    if isinstance(genre, str): genre = [genre]
    if isinstance(author, str): author = [author]
    if isinstance(isbn, str): isbn = [isbn]
    if isinstance(availability, str): availability = [availability]
    if isinstance(book_status, str): book_status = [book_status]

    # Dynamically build the WHERE clause for multiple values
    if genre:
        query += f" AND genre IN ({', '.join(['%s'] * len(genre))})"
        print(query)        
        values.extend(genre)
    if author:
        query += f" AND author IN ({', '.join(['%s'] * len(author))})"
        print(query)
        values.extend(author)
    if isbn:
        query += f" AND isbn IN ({', '.join(['%s'] * len(isbn))})"
        print(query)
        values.extend(isbn)
    if availability:
        query += f" AND availability IN ({', '.join(['%s'] * len(availability))})"
        print(query)
        values.extend(availability)
    if book_status:
        query += f" AND book_status IN ({', '.join(['%s'] * len(book_status))})"
        print(query)
        values.extend(book_status)
    print(query)
    print(values)
    cursor.execute(query, tuple(values))
    books = cursor.fetchall()
    print(books)
    
    if not books:
        return {"fulfillmentText": "No books are currently available by this author."}
    
    book_list = ", ".join([book["title"] for book in books])
    return {"fulfillmentText": f"Books by these parameters : {book_list}"}


# Template function for future intents
def handle_custom_intent(intent,req):
    if intent == "Show Available Books":
        print("GOING TO Show Available Books")
        return show_available_books()
    elif intent == "Find Book by Genre":
        genre = req.get('queryResult', {}).get('parameters', {}).get('genre', "")
        print(genre)
        return books_bygenre(genre)
    elif intent == "books.by_author":
        author = req.get('queryResult', {}).get('parameters', {}).get('author', "")
        print(author)
        return books_byauthor(author)
    elif intent == "locate_book":
        isbn = req.get('queryResult', {}).get('parameters', {}).get('isbn', "")
        print(isbn)
        return books_byauthor(isbn)
    else:
        print("GOING TO GENERAL QUERY")
        return general_query(req)
  

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if not request.data:
            print("❌ No request data received!")
            return jsonify({"fulfillmentText": "No request data received."})

        raw_data = request.data.decode('utf-8')
        req = json.loads(raw_data)
        print(req)
        intent = req.get('queryResult', {}).get('intent', {}).get('displayName', "")
        print(f"Intent: {intent}")
        response = handle_custom_intent(intent,req)
        # response2 = handle_custom_intent("",req)
        # if(len(response["fulfillmentText"].split(":")[-1])<len(response2["fulfillmentText"].split(":")[-1])):
        #     response = response2
        return jsonify(response)
    
    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        return jsonify({"fulfillmentText": "Error parsing JSON request."})

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return jsonify({"fulfillmentText": "An unexpected error occurred."})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500, debug=True)
