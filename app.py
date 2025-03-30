from flask import Flask, request
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

@app.route('/')
def hello():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS visits (id INT AUTO_INCREMENT PRIMARY KEY, count INT)")
    cursor.execute("INSERT INTO visits (count) VALUES (1)")

    conn.commit()

    cursor.execute("SELECT SUM(count) FROM visits")

    total = cursor.fetchone()[0]

    conn.close()

    return f"Hello from Kubernetes! Total visits: {total}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
