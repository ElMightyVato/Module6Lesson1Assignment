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
@app.route('/members', methods = ['POST'])
def add_member():
    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()

    query = "Insert into members (first_name, last_name, email) values (%s, %s, %s)"
    cursor.execute(query, (first_name, last_name, email))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Member added successfully"}), 201

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()

    query = "Select * from Members where id = %s"
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

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id)
    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()

    query = "Update members set first_name = %s, last_name = %s, email = %s where id = %s"
    cursor.execute(query, (first_name, last_name, email, id))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Member updated successfully"}), 200

@app.route('/members/int:id>', methods=['Delete'])
def delete_member(id):
    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()

    query = "Delete from Members where id = %s"
    cursor.execute(query, (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Member deleted successfully"}), 200

"""Task 3"""
@app.route('/wourkouts', methods = ['POST'])
def add_workout_session():
    data = request.get_json()

    member_id = data.get('member_id'),
    date = data.get('date'),
    duration = data.get('duration'),
    workout_type = data.get('type')

    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()

    query = "Insert into WorkoutSessions (member_id, date, duration, type) Values (%s, %s, %s, %s)"
    cursor.execute(query, (member_id, date,duration, workout_type))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"Message": "Workout session added successfully"}), 201

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500
    
    cursor = conn.cursor()

    query = "Select * from WorkoutSessions where id = %s"
    cursor.execute(query, (id,))
    workout_session = cursor.fetchone()

    cursor.close()
    conn.close()

    if workout_session:
        workout_data = {
            "id": workout_session[0],
            "member_id": workout_session[1],
            "date": workout_session[2],
            "Duration": workout_session[3],
            "type": workout_session[4],
        }
        return jsonify(workout_data), 200
    else:
        abort(404, description = "workout session not found")

@app.route('/members/<int:member_id>/workouts', methods = ['GET'])
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
        # Manually format each workout session
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


@app.route('/workouts/<int:id>', methods=['PUT'])
def update_workout_session(id):
    data = request.get_json()

    date = data.get('date')
    duration = data.get('duration')
    workout_type = data.get('type')

    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    cursor = conn.cursor()

    query = "UPDATE WorkoutSessions SET date = %s, duration = %s, type = %s WHERE id = %s"
    cursor.execute(query, (date, duration, workout_type, id))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Workout session updated successfully"}), 200


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout_session(id):
    conn = get_db_connection()

    if conn is None:
        return jsonify({"message": "Failed to connect to the database"}), 500

    cursor = conn.cursor()

    query = "DELETE FROM WorkoutSessions WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Workout session deleted successfully"}), 200


# Error handling
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({"message": str(error)}), 404


if __name__ == '__main__':
    app.run(debug=True)