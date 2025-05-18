# TODO clean up and update

# Clueless
This project sets up a PostgreSQL database and provides the necessary files to establish a connection and define the database schema.

## Setup Instructions

1. **Install PostgreSQL**: Ensure that PostgreSQL is installed on your machine. You can download it from the official PostgreSQL website.

2. **Clone the Repository**: Clone this repository to your local machine.

   ```
   git clone <repository-url>
   cd clueless
   ```

3. **Install Dependencies**: Install the required Python packages using pip. Make sure you have Python and pip installed.

   ```
   pip install -r requirements.txt
   ```

4. **Configure Database Connection**: Update the `connection.py` file with your PostgreSQL database credentials.

5. **Create Database Schema**: Run the following to set up the database.
createdb clueless
psql -U your_username -d clueless -f schema.sql


6. **Run the Application**: Execute the main application file to start interacting with the database.

   ```
   python src/main.py
   ```

## Usage

- The `connection.py` file contains functions to connect and disconnect from the PostgreSQL database.
- The `schema.sql` file defines the structure of the database.
- The `main.py` file serves as the entry point for executing queries and commands.

## venv

- Also set up your venv
With powershell, do something like: 
   .venv\Scripts\Activate.ps1
