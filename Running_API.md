
Hello Akram;
This is a **Markdown** file created using Python. To give you an overview of my API for Assignment 4.

### Overview:
- **db_utils.py** - Contains database utility functions: can update directly to the original DB, this holds the SQL data.
- **main.py** - Contains the Flask app and API routes: to start doing something. The idea is to have a set of functions in `main.py` that interact with the user, while `db_utils.py` handles all database operations.
- **config.py** - Contains database configuration details: login info added to `.gitignore` so that my personal data is not available to you. Please create your own credentials to run the code.
- **Running_API.md** - What you are reading now, documenting how to run and test the API.

### Downloads required:
- `mysql.connector`and from it also imported Errors
- `Flask`, `request`, `jsonify` - for API and formatting API outcomes.

### Detail:
- In MySQL, I created one table for my DB - **Library**: table named **Books**:
id (INT, Primary Key, Auto Increment)
title (VARCHAR) NOT NULL
author (VARCHAR) NOT NULL
available (BOOLEAN) = BIT

- I had made an error so you will see in my db-utils file I corrected this directly to reflect in my SQL

### In my config.py:
- This contains the sensitive information to the DB in this format:

HOST="HOSTNAME"
USER="USERNAME"
PASSWORD="PASSWORD"
#DATABASE="DB_NAME" - the latter is not required as I used Ben's method to integrate the DB into my code but left this in to show you, you can add here and include in the import

- **Reminder**: To run my API please create your own credentials

### In my db_utils.py:
- Import `mysql.connector` so the DB can be used in PyCharm & the API.
- From `mysql.connector` import `Error`.
- `config` import `USER`, `PASSWORD`, `HOST` #DATABASE - left DB in to show you it can be added this way.

### My queries are as follows:
- **Insert Query**: Insert a new book into the books table.
- **Select Query**: Retrieve book details based on the ID.
- **Update Query**: Update the available status of the book when it's borrowed.

### In my main.py:
Imports:
- `from flask import Flask, request, jsonify` - Flask is the API to be used.
- `from db_utils import _connect_to_db, DbConnectionError, get_all_records, add_book, borrow_book` - these are imported from `db_utils` so the API can interact with the DB.

### API endpoints:
- **POST /add-book** � Adds a new book to the library.
- **GET /get-book/<id>** � Retrieves book details by its ID.
- **POST /borrow-book/<id>** � Allows borrowing a book, updating its available status.

### Added a def:run function -

- Made user friendly questions and visibility for the end user

### User interaction:
- The API prompts the user with a set of options:
        *print("1. Add a new book")*
        *print("2. Borrow a book")*
        *print("3. View all books")*
        *print("4. Exit
")*
- Once you have run the API, stop running the program to exit the loop.
Thank you for reading! I hope you enjoyed my Library API!
