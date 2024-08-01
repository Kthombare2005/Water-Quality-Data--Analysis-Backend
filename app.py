from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)

# Load and preprocess data
file_path = 'data/cleaned_waterquality.csv'
data = pd.read_csv(file_path, encoding='latin1')

# Replace NaN values with None
data = data.replace({np.nan: None})

solutions = {
    'TOTAL_COLIFORM': "Improve sanitation facilities, ensure proper waste treatment, and prevent sewage discharge into water bodies.",
    'DO': "Increase aeration, control nutrient loading to reduce algal blooms, and manage organic waste discharge.",
    'pH': "Monitor industrial discharges, control acid rain, and manage agricultural runoff.",
    'TEMP': "Implement riparian buffers, control thermal pollution from industrial sources, and increase shading along waterways.",
    'CONDUCTIVITY': "Manage agricultural runoff, reduce road salt usage, and monitor industrial discharges.",
    'BOD': "Improve waste treatment processes, reduce organic matter discharge, and control agricultural runoff.",
    'NITRATE_N_NITRITE_N': "Manage agricultural practices, reduce fertilizer usage, and improve waste treatment.",
    'FECAL_COLIFORM': "Enhance sanitation infrastructure, prevent sewage discharge, and promote good hygiene practices."
}

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/unique_states', methods=['GET'])
def get_unique_states():
    unique_states = data['STATE'].dropna().unique().tolist()
    return jsonify(unique_states)

@app.route('/api/locations_in_state', methods=['POST'])
def get_locations_in_state():
    state = request.json.get('state')
    locations = data[data['STATE'] == state]['LOCATIONS'].dropna().unique().tolist()
    return jsonify(locations)

@app.route('/api/compare', methods=['POST'])
def compare_data():
    request_data = request.json
    location1 = request_data.get('location1')
    location2 = request_data.get('location2')
    parameter = request_data.get('parameter')
    secondary_parameter = request_data.get('secondary_parameter')

    if location1 and location2 and parameter:
        data1 = data[data['LOCATIONS'] == location1][['LOCATIONS', parameter, secondary_parameter]].dropna()
        data2 = data[data['LOCATIONS'] == location2][['LOCATIONS', parameter, secondary_parameter]].dropna()

        avg1 = data1[parameter].mean()
        avg2 = data2[parameter].mean()

        if avg1 > avg2:
            more_polluted = location1
            reason = f"{location1} has higher {parameter} levels ({avg1}) compared to {location2} ({avg2})."
        elif avg2 > avg1:
            more_polluted = location2
            reason = f"{location2} has higher {parameter} levels ({avg2}) compared to {location1} ({avg1})."
        else:
            secondary_avg1 = data1[secondary_parameter].mean()
            secondary_avg2 = data2[secondary_parameter].mean()
            if secondary_avg1 > secondary_avg2:
                more_polluted = location1
                reason = f"{location1} and {location2} have the same {parameter} levels ({avg1}). However, {location1} has higher {secondary_parameter} levels ({secondary_avg1}) compared to {location2} ({secondary_avg2})."
            else:
                more_polluted = location2
                reason = f"{location1} and {location2} have the same {parameter} levels ({avg1}). However, {location2} has higher {secondary_parameter} levels ({secondary_avg2}) compared to {location1} ({secondary_avg1})."

        solution = solutions.get(parameter, "No solution available for the selected parameter.")

    else:
        return jsonify({'error': 'Invalid input'}), 400

    return jsonify({
        'location1_data': data1.to_dict(orient='records'),
        'location2_data': data2.to_dict(orient='records'),
        'more_polluted': more_polluted,
        'reason': reason,
        'solution': solution
    })

if __name__ == '__main__':
    app.run(debug=True)
