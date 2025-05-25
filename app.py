from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/api": {"origins": "*"}})  # Enable CORS for /api endpoint

# Load student data
try:
    with open('students.json', 'r') as f:
        data = json.load(f)
    # Create a dictionary for faster lookup
    students_dict = {item['name'].lower(): item['marks'] for item in data}
except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
    data = None
    students_dict = {}

@app.route('/api', methods=['GET'])
def get_marks():
    if data is None:
        return jsonify({"error": "Student data not found or invalid JSON"}), 500

    # Get list of names from query parameters
    names = request.args.getlist('name')
    
    if not names:
        return jsonify({"error": "At least one name is required"}), 400

    marks = []
    for name in names:
        # Search for the student's marks (case-insensitive)
        mark = students_dict.get(name.lower())
        if mark is None:
            return jsonify({"error": f"Student '{name}' not found"}), 404
        marks.append(int(mark))

    return jsonify({"marks": marks})

if __name__ == "__main__":
    app.run(debug=True)