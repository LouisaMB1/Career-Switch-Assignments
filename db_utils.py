import mysql.connector
from mysql.connector import Error
from config import USER, PASSWORD, HOST #DATABASE

# Can add here exception for database connection errors.
class DbConnectionError(Exception):
    pass

# Created the connection based on configuration.
def _connect_to_db(db_name):
    try:
        cnx = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin='mysql_native_password',
            database=db_name
        )
        print("Successfully connected to the database!")
        return cnx
    except Error as e:
        print(f"Error: '{e}'")
        return None

# Function to get all records from a specific table.
def get_all_records():
    try:
        # Connect to the database.
        db_name = 'Library_'  # Using my configured database name from config.py.
        db_connection = _connect_to_db(db_name)
        if db_connection is None:
            raise DbConnectionError("Could not establish a database connection.")

        # Created a cursor to execute queries.
        cursor = db_connection.cursor()
        print(f"Connected to DB: {db_name}")

        # Created a cursor to execute queries.
        cursor = db_connection.cursor(dictionary=True)  # Used dictionary=True to get records as dictionaries.
        print(f"Connected to DB: {db_name}")

        # Querying the database.
        query = """SELECT * FROM Books"""  # Updated to match my specific table_name and query.
        cursor.execute(query)
        result = cursor.fetchall()

        for book in result:
            book['Available'] = 'available' if book['Available'] == 1 else 'borrowed' #as available is 1 and unavailable is 0

        # Printed each record in the result set.
        for record in result:
            print(record)

        # As always - close the cursor after fetching data.
        cursor.close()

    except DbConnectionError as e:
        print(e)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # As always - close the database connection in the finally block.
        if db_connection:
            db_connection.close()
            print("DB connection closed.")


# I found an error my books duplicated so this function is to update the details of books with IDs 6-10.
def update_book_details():
    try:
        db_name = 'Library_'  # Using configured database name.
        db_connection = _connect_to_db(db_name)
        if db_connection is None:
            raise DbConnectionError("Could not establish a database connection.")

        cursor = db_connection.cursor()

        # Created an update statement for each book with ID 6-10.
        update_queries = [
            "UPDATE Books SET Title = 'Forth Wing', Author = 'Rebecca Yarros' WHERE id = 6",
            "UPDATE Books SET Title = 'Iron Flame', Author = 'Rebecca Yarros' WHERE id = 7",
            "UPDATE Books SET Title = 'Onyx Storm', Author = 'Rebecca Yarros' WHERE id = 8",
            "UPDATE Books SET Title = 'The Millennium Wolves', Author = 'Sapir A. England' WHERE id = 9",
            "UPDATE Books SET Title = 'Kidnapped by My Mate', Author = 'Annie Whipple' WHERE id = 10"
        ]

        # Executed each update query one by one.
        for query in update_queries:
            cursor.execute(query)

        # Committed the changes to the database.
        db_connection.commit()
        print("Book details updated successfully for IDs 6-10.")

        cursor.close()

    except DbConnectionError as e:
        print(e)

    except Exception as e:
        print(f"An error occurred while updating book details: {e}")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection closed after updating.")

#Updated with functions to add a book and borrow a book.

def add_book(title,author):
    """
    Add a new book to the Books table.
    """
    try:
        db_name = 'Library_'  # Using configured database name.
        db_connection = _connect_to_db(db_name)
        if db_connection is None:
            raise DbConnectionError("Could not establish a database connection.")

        cursor = db_connection.cursor()

        # Created the SQL query to insert a new book.
        query = "INSERT INTO Books (title, author, available) VALUES (%s, %s, %s)"
        values = (title, author, 1) #BIT in SQL 1 is available i.e. True

        # Executed the query and committed the changes.
        cursor.execute(query, values)
        db_connection.commit()
        print(f"Book '{title}' by '{author}' added successfully!")

        cursor.close()

    except DbConnectionError as e:
        print(e)

    except Exception as e:
        print(f"An error occurred while adding the book: {e}")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection closed after adding a book.")

def borrow_book(book_id):
    """
    Borrow a book & update its availability status.
    """
    try:
        db_name = 'Library_'  # Using configured database name.
        db_connection = _connect_to_db(db_name)
        if db_connection is None:
            raise DbConnectionError("Could not establish a database connection.")

        cursor = db_connection.cursor()

        # Check if the book is available before borrowing.
        check_query = "SELECT Available FROM Books WHERE id = %s"
        cursor.execute(check_query, (book_id,))
        availability = cursor.fetchone()

        # Ensure availability has a valid record
        if availability is None:
            print(f"Book ID {book_id} does not exist.")
            return  # Book does not exist, exit the function

        if availability[0] == 1: #as 1 means true i.e available
            # Update the book's availability to 'Borrowed' means 0 = false
            update_query = "UPDATE Books SET Available = %s WHERE id = %s"
            cursor.execute(update_query, (0, book_id)) #as 0 means borrowed
            db_connection.commit()
            print(f"Book ID {book_id} has been borrowed successfully!")
        else:
            print(f"Book ID {book_id} is has already been lended or does not exist.")

        cursor.close()

    except DbConnectionError as e:
        print(e)

    except Exception as e:
        print(f"An error occurred while borrowing the book: {e}")

    finally:
        if db_connection:
            db_connection.close()
            print("DB connection closed after borrowing a book.")

def main():
    # update_book_details() updated booked details left in for you to review
    get_all_records() #checked to see once update if it now shows in table



if __name__ == '__main__':
    main()