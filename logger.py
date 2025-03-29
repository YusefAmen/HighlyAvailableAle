from flask import Flask
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql-service"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "password"),
        database=os.getenv("MYSQL_DB", "mydb")
    )

@app.route('/log')
def log_visit():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO visits (count) VALUES (1)")
    conn.commit()
    conn.close()
    return "Visit logged!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
