import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()  

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

def connect(dbname = db_name, user = db_user, password = db_password, host='localhost', port='5432'):
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print("Connection to the database established.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def disconnect(connection):
    if connection:
        connection.close()
        print("Database connection closed.")

# Insert a new user into the users table
def insert_user(connection, username, email, password_hash):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (username, email, password_hash)
            )
            user_id = cursor.fetchone()[0]
            connection.commit()
            print(f"Inserted user with id: {user_id}")
            return user_id
    except Exception as e:
        print(f"Error inserting user: {e}")
        connection.rollback()
        return None

# Delete a user by id
def delete_user(connection, user_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM users WHERE id = %s;",
                (user_id,)
            )
            connection.commit()
            print(f"Deleted user with id: {user_id}")
    except Exception as e:
        print(f"Error deleting user: {e}")
        connection.rollback()

# Update a user's email by id
def update_user_email(connection, user_id, new_email):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET email = %s WHERE id = %s;",
                (new_email, user_id)
            )
            connection.commit()
            print(f"Updated user {user_id} email to {new_email}")
    except Exception as e:
        print(f"Error updating user email: {e}")
        connection.rollback()

def insert_article(connection, user_id, name, image_url, is_default, category):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO articles (user_id, name, image_url, is_default, category)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (user_id, name, image_url, is_default, category)
            )
            article_id = cursor.fetchone()[0]
            connection.commit()
            print(f"Inserted article with id: {article_id}")
            return article_id
    except Exception as e:
        print(f"Error inserting article: {e}")
        connection.rollback()
        return None

# Update an article's name and category by id
def update_article(connection, article_id, new_name=None, new_category=None):
    try:
        with connection.cursor() as cursor:
            updates = []
            params = []
            if new_name is not None:
                updates.append("name = %s")
                params.append(new_name)
            if new_category is not None:
                updates.append("category = %s")
                params.append(new_category)
            if not updates:
                print("No updates provided.")
                return
            params.append(article_id)
            query = f"UPDATE articles SET {', '.join(updates)} WHERE id = %s;"
            cursor.execute(query, tuple(params))
            connection.commit()
            print(f"Updated article {article_id}")
    except Exception as e:
        print(f"Error updating article: {e}")
        connection.rollback()

# Delete an article by id
def delete_article(connection, article_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM articles WHERE id = %s;",
                (article_id,)
            )
            connection.commit()
            print(f"Deleted article with id: {article_id}")
    except Exception as e:
        print(f"Error deleting article: {e}")
        connection.rollback()