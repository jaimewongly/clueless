# tests/test_database.py

# to run these tests 
# set the pythonpath to src:
#
# cd app
# set PYTHONPATH=src
# 
# then use the command:
# python -m pytest

from src.database.connection import connect, disconnect, insert_user, delete_user, update_user_email, insert_article, update_article, delete_article

def test_can_connect_to_database():
    connection = connect()

    assert connection is not None, "Connection failed: returned None"
    assert connection.closed == 0, "Connection is unexpectedly closed"

    cur = connection.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    assert result[0] == 1, "Unexpected result from test query"

    cur.close()
    disconnect(connection)

def test_can_write_to_database():
    connection = connect()

    assert connection is not None, "Connection failed: returned None"
    assert connection.closed == 0, "Connection is unexpectedly closed"

    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name VARCHAR(50));")
    cur.execute("INSERT INTO test_table (name) VALUES ('test_name');")
    connection.commit()

    cur.execute("SELECT name FROM test_table WHERE name = 'test_name';")
    result = cur.fetchone()
    assert result[0] == 'test_name', "Unexpected result from test write operation"

    cur.execute("DROP TABLE test_table;")
    connection.commit()

    cur.close()
    disconnect(connection)

def test_can_delete_from_database():
    connection = connect()
    assert connection is not None, "Connection failed: returned None"
    assert connection.closed == 0, "Connection is unexpectedly closed"

    cur = connection.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name VARCHAR(50));")
    cur.execute("INSERT INTO test_table (name) VALUES ('delete_me') RETURNING id;")
    row_id = cur.fetchone()[0]
    connection.commit()

    cur.execute("DELETE FROM test_table WHERE id = %s;", (row_id,))
    connection.commit()

    cur.execute("SELECT * FROM test_table WHERE id = %s;", (row_id,))
    result = cur.fetchone()
    assert result is None, "Row was not deleted from the database"

    cur.execute("DROP TABLE test_table;")
    connection.commit()
    cur.close()
    disconnect(connection)

    
def test_insert_user():
    connection = connect()
    assert connection is not None, "Connection failed: returned None"
    assert connection.closed == 0, "Connection is unexpectedly closed"

    cur = connection.cursor()
    cur.execute("DELETE FROM users WHERE username = 'testuser';")
    connection.commit()

    user_id = insert_user(connection, "testuser", "testuser@example.com", "hashedpassword123")
    assert user_id is not None, "User was not inserted"

    cur.execute("SELECT username, email FROM users WHERE id = %s;", (user_id,))
    result = cur.fetchone()
    assert result is not None, "Inserted user not found"
    assert result[0] == "testuser"
    assert result[1] == "testuser@example.com"

    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    connection.commit()
    cur.close()
    disconnect(connection)

def test_update_user_email():
    connection = connect()
    assert connection is not None, "Connection failed: returned None"
    assert connection.closed == 0, "Connection is unexpectedly closed"

    user_id = insert_user(connection, "updateuser", "updateuser@example.com", "hashedpassword456")
    assert user_id is not None, "User was not inserted for update"

    new_email = "updated_email@example.com"
    update_user_email(connection, user_id, new_email)

    cur = connection.cursor()
    cur.execute("SELECT email FROM users WHERE id = %s;", (user_id,))
    result = cur.fetchone()
    assert result is not None, "Updated user not found"
    assert result[0] == new_email

    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    connection.commit()
    cur.close()
    disconnect(connection)

def test_delete_user():
    connection = connect()
    assert connection is not None, "Connection failed: returned None"
    assert connection.closed == 0, "Connection is unexpectedly closed"

    user_id = insert_user(connection, "deleteuser", "deleteuser@example.com", "hashedpassword789")
    assert user_id is not None, "User was not inserted for deletion"

    delete_user(connection, user_id)

    cur = connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
    result = cur.fetchone()
    assert result is None, "User was not deleted"

    cur.close()
    disconnect(connection)
    
def test_insert_article():
    connection = connect()
    assert connection is not None, "Connection failed: returned None"
    assert connection.closed == 0, "Connection is unexpectedly closed"

    # Ensure a user exists to satisfy the foreign key constraint
    cur = connection.cursor()
    cur.execute("INSERT INTO users (username, email, password_hash) VALUES ('articleuser', 'articleuser@example.com', 'hash') RETURNING id;")
    user_id = cur.fetchone()[0]
    connection.commit()

    article_id = insert_article(connection, user_id, "Test Article", "http://example.com/image.png", True, "TestCategory")
    assert article_id is not None, "Article was not inserted"

    cur.execute("SELECT name, image_url, is_default, category FROM articles WHERE id = %s;", (article_id,))
    result = cur.fetchone()
    assert result is not None, "Inserted article not found"
    assert result[0] == "Test Article"
    assert result[1] == "http://example.com/image.png"
    assert result[2] is True or result[2] == True
    assert result[3] == "TestCategory"

def test_update_article():
    connection = connect()
    assert connection is not None, "Connection failed: returned None"
    assert connection.closed == 0, "Connection is unexpectedly closed"

    cur = connection.cursor()
    cur.execute("INSERT INTO users (username, email, password_hash) VALUES ('updatearticleuser', 'updatearticleuser@example.com', 'hash') RETURNING id;")
    user_id = cur.fetchone()[0]
    connection.commit()

    article_id = insert_article(connection, user_id, "Old Name", "http://example.com/old.png", False, "OldCategory")
    assert article_id is not None, "Article was not inserted for update"

    update_article(connection, article_id, new_name="New Name", new_category="NewCategory")

    cur.execute("SELECT name, category FROM articles WHERE id = %s;", (article_id,))
    result = cur.fetchone()
    assert result is not None, "Updated article not found"
    assert result[0] == "New Name"
    assert result[1] == "NewCategory"

def test_delete_article():
    connection = connect()
    assert connection is not None, "Connection failed: returned None"
    assert connection.closed == 0, "Connection is unexpectedly closed"

    cur = connection.cursor()
    cur.execute("INSERT INTO users (username, email, password_hash) VALUES ('deletearticleuser', 'deletearticleuser@example.com', 'hash') RETURNING id;")
    user_id = cur.fetchone()[0]
    connection.commit()

    article_id = insert_article(connection, user_id, "Delete Me", "http://example.com/delete.png", False, "DeleteCategory")
    assert article_id is not None, "Article was not inserted for deletion"

    delete_article(connection, article_id)

    cur.execute("SELECT * FROM articles WHERE id = %s;", (article_id,))
    result = cur.fetchone()
    assert result is None, "Article was not deleted"

    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    connection.commit()
    cur.close()
    disconnect(connection)
    
