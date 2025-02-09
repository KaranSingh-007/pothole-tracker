from flask import Flask, jsonify
import cx_Oracle
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection details
db_username = "PRITAM_SAPKAL"  # Update this
db_password = "pass@123"       # Update this
db_host = "192.168.75.36"          # Update this
db_service = "XE"              # Update this

def get_pothole_data():
    """Fetch pothole data from the database."""
    connection = cx_Oracle.connect(db_username, db_password, f"{db_host}/{db_service}")
    cursor = connection.cursor()
    query = "SELECT LATITUDE, LONGITUDE FROM POTHOLES_DATABASE"
    cursor.execute(query)
    data = [{"latitude": lat, "longitude": lon} for lat, lon in cursor]
    connection.close()
    return data

@app.route('/api/potholes', methods=['GET'])
def potholes():
    """API endpoint to fetch pothole data."""
    try:
        data = get_pothole_data()
        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
