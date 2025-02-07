"""Task 1"""
from flask import Flask, request, jsonify, abort
from flask_marshmallow import Marshmallow
import mysql.connector

app = Flask(__name__)

ma = Marshmallow(app)


def get_db_connection():
    """ Connect to the MySQL database and return the connection object"""
    # Database Connection Parameteres
    db_name = 'fitness_center'
    user = 'root'
    password = "NeroZero1377@"
    host = 'localhost'

    try:
        #attempting to establish connection
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password, 
            host = host
        )

        # Check if the connection is successful
        print("Connected to MySQL database successfully")
        return conn

    except Error as e:
        # Handling any connection errors
        print(f"Error: {e}")
        return None
    
"""Task 2"""
# Route to get all members
@app.route('/members', methods=['GET'])
def get_all_members():
    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    cursor = conn.cursor()

    query = "SELECT * FROM Members"
    cursor.execute(query)
    members = cursor.fetchall()

    cursor.close()
    conn.close()

    if members:
        members_data = []
        for member in members:
            members_data.append({
                "id": member[0],
                "first_name": member[1],
                "last_name": member[2],
                "email": member[3]
            })
        return jsonify(members_data), 200
    else:
        return jsonify({"message": "No members found"}), 404

# Route to add a new member
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    cursor = conn.cursor()

    query = "INSERT INTO Members (first_name, last_name, email) VALUES (%s, %s, %s)"
    cursor.execute(query, (first_name, last_name, email))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Member added successfully"}), 201

# Route to get a single member by ID
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    cursor = conn.cursor()

    query = "SELECT * FROM Members WHERE id = %s"
    cursor.execute(query, (id,))
    member = cursor.fetchone()

    cursor.close()
    conn.close()

    if member:
        member_data = {
            "id": member[0],
            "first_name": member[1],
            "last_name": member[2],
            "email": member[3]
        }
        return jsonify(member_data), 200
    else:
        abort(404, description="Member not found")

# Route to update a member by ID
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    cursor = conn.cursor()

    query = "UPDATE Members SET first_name = %s, last_name = %s, email = %s WHERE id = %s"
    cursor.execute(query, (first_name, last_name, email, id))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Member updated successfully"}), 200

# Route to delete a member by ID
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    cursor = conn.cursor()

    query = "DELETE FROM Members WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Member deleted successfully"}), 200

# Route to add a new workout session
@app.route('/workouts', methods=['POST'])
def add_workout_session():
    data = request.get_json()

    member_id = data.get('member_id')
    date = data.get('date')
    duration = data.get('duration')
    workout_type = data.get('type')

    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    cursor = conn.cursor()

    query = "INSERT INTO WorkoutSessions (member_id, date, duration, type) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (member_id, date, duration, workout_type))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"Message": "Workout session added successfully"}), 201

# Route to get a workout session by ID
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    cursor = conn.cursor()

    query = "SELECT * FROM WorkoutSessions WHERE id = %s"
    cursor.execute(query, (id,))
    workout_session = cursor.fetchone()

    cursor.close()
    conn.close()

    if workout_session:
        workout_data = {
            "id": workout_session[0],
            "member_id": workout_session[1],
            "date": workout_session[2],
            "duration": workout_session[3],
            "type": workout_session[4],
        }
        return jsonify(workout_data), 200
    else:
        abort(404, description="Workout session not found")

# Route to get all workout sessions for a specific member
@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_member_workouts(member_id):
    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    cursor = conn.cursor()

    query = "SELECT * FROM WorkoutSessions WHERE member_id = %s"
    cursor.execute(query, (member_id,))
    workouts = cursor.fetchall()

    cursor.close()
    conn.close()

    if workouts:
        workout_sessions_data = []
        for workout in workouts:
            workout_sessions_data.append({
                "id": workout[0],
                "member_id": workout[1],
                "date": workout[2],
                "duration": workout[3],
                "type": workout[4]
            })
        return jsonify(workout_sessions_data), 200
    else:
        abort(404, description="No workout sessions found for this member")

# Error handling for 404
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({"message": str(error)}), 404

if __name__ == '__main__':
    app.run(debug=True)


    