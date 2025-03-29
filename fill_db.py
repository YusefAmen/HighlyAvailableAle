import mysql.connector
import time

# Connect to MySQL (matches flask app config)
conn = mysql.connector.connect(
    host="localhost",  # We'll port-forward later
    user="root",
    password="password",
    database="mydb"
)
cursor = conn.cursor()

# Create table if not exists (matches app.py)
cursor.execute("CREATE TABLE IF NOT EXISTS visits (id INT AUTO_INCREMENT PRIMARY KEY, count INT)")

# Insert rows rapidly
start_time = time.time()
for i in range(1000000):  # Adjust to hit ~1GB
    cursor.execute("INSERT INTO visits (count) VALUES (%s)", (i,))
    if i % 10000 == 0:
        conn.commit()
        print(f"Inserted {i} rows, elapsed: {time.time() - start_time:.2f}s")
conn.commit()
conn.close()
print("Done!")
