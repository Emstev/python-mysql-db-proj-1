from flask import Flask, jsonify, render_template, request
import pymysql

app = Flask(__name__)

def get_db_connection():
    connection = pymysql.connect(
        host='mydb.c5su8yseyvqt.eu-central-1.rds.amazonaws.com',
        user='dbuser',
        password='dbpassword',
        db='devprojdb',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/create_table')
def create_table():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS example_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                status VARCHAR(50)
            )
        """
        cursor.execute(create_table_query)
        connection.commit()
        return "Table created successfully", 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/insert_record', methods=['POST'])
def insert_record():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        status = data.get('status')

        if not name:
            return jsonify({'error': 'Missing "name" in request body'}), 400

        connection = get_db_connection()
        cursor = connection.cursor()
        insert_query = "INSERT INTO example_table (name, email, status) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (name, email, status))
        connection.commit()
        return jsonify({'message': 'Record inserted successfully', 'id': cursor.lastrowid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/data')
def data():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM example_table')
        result = cursor.fetchall()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/update_record/<int:id>', methods=['PUT'])
def update_record(id):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        status = data.get('status')

        if not name and not email and not status:
            return jsonify({'error': 'No fields to update'}), 400

        updates = []
        values = []

        if name:
            updates.append("name = %s")
            values.append(name)
        if email:
            updates.append("email = %s")
            values.append(email)
        if status:
            updates.append("status = %s")
            values.append(status)

        values.append(id)
        update_query = f"UPDATE example_table SET {', '.join(updates)} WHERE id = %s"

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(update_query, tuple(values))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': f'Record with id {id} not found'}), 404

        return jsonify({'message': f'Record {id} updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/delete_record/<int:id>', methods=['DELETE'])
def delete_record(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        delete_query = "DELETE FROM example_table WHERE id = %s"
        cursor.execute(delete_query, (id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': f'Record with id {id} not found'}), 404

        return jsonify({'message': f'Record {id} deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
