from flask import Flask, request, jsonify
from db_utils import _connect_to_db, DbConnectionError, get_all_records, add_book, borrow_book

app = Flask(__name__)

# Connect to the database made in SQL
DATABASE_NAME = 'Library_'


# Route to get all records from the `Books` table.
@app.route('/books', methods=['GET'])
def get_books():
    """Retrieve all books in the library."""
    try:
        db_connection = _connect_to_db(DATABASE_NAME)
        if db_connection is None:
            raise DbConnectionError("Could not establish a database connection.")

        cursor = db_connection.cursor(dictionary=True)
        query = "SELECT * FROM Books"
        cursor.execute(query)
        books = cursor.fetchall()

        # Transform the available column for the user for readability
        for book in books:
            book['Available'] = 'available' if book['Available'] == 1 else 'borrowed'
        cursor.close()

        # Return the fetched book data as a JSON response.
        return jsonify(books), 200 #200 = ok

    except DbConnectionError as e:
        return jsonify({"error": str(e)}), 500 #500 = internal server error

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

    finally:
        if db_connection:
            db_connection.close()


# Route to add a new book.
@app.route('/add-book', methods=['POST'])
def add_book_route():
    """Add a new book to the library."""
    try:
        data = request.get_json()
        title = data.get('Title')
        author = data.get('Author')

        db_connection = _connect_to_db(DATABASE_NAME)
        if db_connection is None:
            raise DbConnectionError("Could not establish a database connection.")

        cursor = db_connection.cursor()
        query = "INSERT INTO Books (title, author, available) VALUES (%s, %s, %s)"
        values = (title, author, True) # True = 1 i.e. book is available
        cursor.execute(query, values)
        db_connection.commit()

        cursor.close()
        return jsonify({"message": "Book added successfully!"}), 201 #201 = created

    except DbConnectionError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

    finally:
        if db_connection:
            db_connection.close()


# Route to borrow a book by updating its availability.
@app.route('/borrow-book/<int:book_id>', methods=['POST'])
def borrow_book_route(book_id):
    """Borrow a book by setting its availability to False."""
    try:
        db_connection = _connect_to_db(DATABASE_NAME)
        if db_connection is None:
            raise DbConnectionError("Could not establish a database connection.")

        cursor = db_connection.cursor()
        query = "UPDATE Books SET Available = %s WHERE id = %s AND available = %s"
        values = (0, book_id, 1)  # Set to 0 for borrowed, check if it was 1 (available)
        updated_rows = cursor.rowcount  # Get the number of rows affected
        db_connection.commit()

        cursor.close()

        if updated_rows > 0:  # Check if any rows were updated
            return jsonify({"message": "Book borrowed successfully!"}), 200
        else:
            return jsonify({"message": "Book not available or doesn't exist, try again."}), 404 #404 = not found

    except DbConnectionError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

    finally:
        if db_connection:
            db_connection.close()

def run():
    print("############################")
    print("Hello, welcome to the library system!")
    print("############################\n")

    while True:
        print("Please choose a number from the appointed options:")
        print("1. Add a new book")
        print("2. Borrow a book")
        print("3. View all books")
        print("4. Exit\n")

        choice = input("Enter the number corresponding to your choice (1-4): ")

        if choice == '1':
            # Add a new book.
            title = input("Enter the book title: ")
            author = input("Enter the author name: ")
            add_book(title,author)
        elif choice == '2':
            # Borrow a book.
            try:
                book_id = int(input("Enter the ID of the book you wish to borrow (for ID range select option 3): "))
                borrow_book(book_id)
            except ValueError:
                 print("Invalid ID. Please enter a whole number tip:select option 3 to check how many books are available.")
        elif choice == '3':
            # View all books.
            print("\n####### AVAILABLE BOOKS #######\n")
            get_all_records()
        elif choice == '4':
            # Exit the loop.
            print("Thank you for using the library system. See you soon!")
            break
        else:
            print("Invalid option. Please select an option between 1-4.")

        print("\n------------------------------\n")


# Start the Flask application.
if __name__ == '__main__':
    run()
    app.run(debug=True)
