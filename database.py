import sqlite3

conn = sqlite3.connect("users.db",check_same_thread=False)

cursor = conn.cursor()

# Create user table....

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT UNIQUE,
    username TEXT UNIQUE,
    password TEXT
    )
    """
)
conn.commit()

#****************User ragistration******************
def register_user(full_name,
                  email,
                  username,
                  password):
    try:
        cursor.execute(
            """
            INSERT INTO users(
            full_name,
            email,
            username,
            password)
            VALUES(?,?,?,?)""",
            (full_name,
             email,
             username,
             password)
        )
        conn.commit()
        return True
    except:
        return False
    
#***************************************user login*******************
def user_login(username,password):
    cursor.execute(
        """
        SELECT * FROM users
        WHERE username=? AND password=?""",
        (username,password)
    )
    user = cursor.fetchone()
    return user
