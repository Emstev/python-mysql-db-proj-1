from flask import Flask, jsonify, render_template, request
import pymysql

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host='mydb.c5su8yseyvqt.eu-central-1.rds.amazonaws.com',  # Your RDS endpoint
        user='dbuser',                                             # Your DB username
        password='dbpassword',                                     # Your DB password
        db='devprojdb',                                            # Your DB name
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Health check
@app.route('/health')
def health():
    return "Up & Running"

# UI Route
@app.route('/')
def index():
    return render_template('index.html')

# Create table (optional setup route)
@app.route('/create_table')
def create_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS example_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            status VARCHAR(100)
        )
    """)
    connection.commit()
    connection.close()
    return "Table created successfully"

# Insert new record
@app.route('/insert_record', methods=['POST'])
def insert_record():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    status = data.get('status')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO example_table (name, email, status) VALUES (%s, %s, %s)", (name, email, status))
    connection.commit()
    connection.close()
    return jsonify({"message": "Record inserted successfully"})

# Get all records
@app.route('/data')
def get_data():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM example_table")
    result = cursor.fetchall()
    connection.close()
    return jsonify(result)

# Update record
@app.route('/update_record/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    status = data.get('status')

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE example_table SET name=%s, email=%s, status=%s WHERE id=%s", (name, email, status, record_id))
    connection.commit()
    connection.close()
    return jsonify({"message": "Record updated successfully"})

# Delete record
@app.route('/delete_record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM example_table WHERE id=%s", (record_id,))
    connection.commit()
    connection.close()
    return jsonify({"message": "Record deleted successfully"})

# Run app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
