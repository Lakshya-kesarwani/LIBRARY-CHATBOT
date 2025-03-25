cursor.execute("SELECT title, author, location FROM books WHERE availability = 'available'")
    books = cursor.fetchall()
    response_text = "Here are available books: " + ", ".join([f"{b['title']} by {b['author']} (Location: {b['location']})" for b in books])
    