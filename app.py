from flask import Flask, jsonify, render_template, request
import pymysql

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host='mydb.c5su8yseyvqt.eu-central-1.rds.amazonaws.com',  # Replace with your RDS endpoint
        user='dbuser',
        password='dbpassword',
        db='devprojdb',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Create table function (called at startup)
def create_table_if_not_exists():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS example_table (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255),
                    status VARCHAR(100)
                )
            """)
        connection.commit()
    finally:
        connection.close()

# Health check route
@app.route('/health')
def health():
    return "Up & Running", 200

# UI route
@app.route('/')
def index():
    return render_template('index.html')

# Insert a new record
@app.route('/insert_record', methods=['POST'])
def insert_record():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    status = data.get('status')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO example_table (name, email, status) VALUES (%s, %s, %s)",
                (name, email, status)
            )
        connection.commit()
        return jsonify({"message": "Record inserted successfully"}), 201
    finally:
        connection.close()

# Get all records
@app.route('/data')
def get_data():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM example_table")
            result = cursor.fetchall()
        return jsonify(result), 200
    finally:
        connection.close()

# Update a record
@app.route('/update_record/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    status = data.get('status')

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE example_table SET name=%s, email=%s, status=%s WHERE id=%s",
                (name, email, status, record_id)
            )
        connection.commit()
        return jsonify({"message": "Record updated successfully"}), 200
    finally:
        connection.close()

# Delete a record
@app.route('/delete_record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM example_table WHERE id=%s", (record_id,))
        connection.commit()
        return jsonify({"message": "Record deleted successfully"}), 200
    finally:
        connection.close()

# Run the Flask app and ensure the table exists on startup
if __name__ == '__main__':
    create_table_if_not_exists()
    app.run(debug=True, host='0.0.0.0', port=5000)
