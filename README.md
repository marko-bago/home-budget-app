# Home Budget App


Home Budget App API is a backend application designed to help users manage their personal finances.
Users can register, log in, perform CRUD operations on transactions and transaction categories.
Transactions can be of type income and expense.
Default categories are created when a user is created (defined in config.py)
The API also features a filtering system to search for transactions by dates and categories and a summary endpoint to get summarizations of transaction data by amount.


Took guidelines and inspiration for structuring this project from: [fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices)


<img alt="Static Badge" src="https://img.shields.io/badge/Version-1.0.0-seagreen?style=for-the-badge">

<br>

## Installation

1. Clone this repository on your local machine:

   ```bash
   git clone https://github.com/marko-bago/home-budget-app.git
   ```

2. Go to the project directory:

   ```bash
   cd home-budget-app
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv          # Create a virtual environment
   .venv\Scripts\activate        # Activate the environment in Windows
   source .venv/bin/activate  # Activate the environment in Linux/MacOS
   ```

4. Install the necessary dependencies for the project using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

5. There is a file called  `template.env` in the root directory of the project with the neccessary project config parameters. To start the project create an `.env` file using the template:

    For the `SECRET_KEY`, you can generate a secure key by running the following command in your terminal:

    ```bash
    openssl rand -hex 32
    ```

    `SQLALCHEMY_DATABASE_URI` is a SQLite connection string by default. This can be changed to any database supported by SQLAlchemy.

    `TEST_DATABASE_URL` is used for testing. It is set to `:memory:` to avoid writing to db while testing.

   


6. Start the API development server with the following command:

    ```bash
    uvicorn main:app --reload
    ```

<br>

Adjust other parameters in `.env` file as needed.

<br>

## Testing

This project uses pytest to perform automated tests to ensure the reliability and functionality of key features.

To run all tests, use the following command:
```bash
pytest
```

To run tests with logger output use:
```bash
pytest tests -o log_cli=true -o log_cli_level=INFO
```


<br>

## Documentation

Once the application is up and running, you can access Swagger's interactive API documentation at 
`http://localhost:8000/docs`, or ReDoc's at `http://localhost:8000/redoc`, where you can visualize and test the available API endpoints.


<br>


