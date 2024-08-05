from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER

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

causes = {
    'TOTAL_COLIFORM': "Sewage discharge, agricultural runoff, and animal waste.",
    'DO': "Organic waste discharge, nutrient loading from fertilizers, and algal blooms.",
    'pH': "Industrial discharges, acid rain, and agricultural runoff.",
    'TEMP': "Industrial thermal pollution, deforestation, and climate change.",
    'CONDUCTIVITY': "Industrial discharges, road salt usage, and agricultural runoff.",
    'BOD': "Organic matter from sewage, industrial effluents, and agricultural runoff.",
    'NITRATE_N_NITRITE_N': "Fertilizer runoff, sewage discharge, and industrial effluents.",
    'FECAL_COLIFORM': "Sewage contamination, agricultural runoff, and animal waste."
}

consequences = {
    'TOTAL_COLIFORM': "Waterborne diseases, negative impacts on aquatic life, and degradation of water quality.",
    'DO': "Fish kills, reduced biodiversity, and poor water quality.",
    'pH': "Corrosive water, harmful effects on aquatic life, and reduced water quality.",
    'TEMP': "Thermal shock to aquatic life, reduced oxygen levels, and altered aquatic ecosystems.",
    'CONDUCTIVITY': "Harmful to aquatic life, altered water chemistry, and reduced water quality.",
    'BOD': "Depletion of dissolved oxygen, fish kills, and poor water quality.",
    'NITRATE_N_NITRITE_N': "Eutrophication, harmful algal blooms, and negative impacts on aquatic ecosystems.",
    'FECAL_COLIFORM': "Spread of waterborne diseases, health risks to humans, and degradation of water quality."
}

api_key = "AIzaSyAo6Vv609JovSv_B6W2VOVEyaaBWKwAEC4"  # Ensure you replace this with your actual API key

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

        detailed_analysis = {
            "reason": reason,
            "solution": solutions.get(parameter, "No solution available for the selected parameter."),
            "causes": causes.get(parameter, "No causes available for the selected parameter."),
            "consequences": consequences.get(parameter, "No consequences available for the selected parameter.")
        }

    else:
        return jsonify({'error': 'Invalid input'}), 400

    return jsonify({
        'location1_data': data1.to_dict(orient='records'),
        'location2_data': data2.to_dict(orient='records'),
        'more_polluted': more_polluted,
        'detailed_analysis': detailed_analysis
    })

@app.route('/api/ai_query', methods=['POST'])
def ai_query():
    query = request.json.get('query')
    print(f"Received query: {query}")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
    
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": query}
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    print(f"Response status code: {response.status_code}")
    if response.status_code == 200:
        ai_response = response.json()
        print(f"AI Response: {ai_response}")
        return jsonify(ai_response)
    else:
        print(f"Error from AI API: {response.text}")
        return jsonify({'error': 'Failed to get AI response'}), response.status_code

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    request_data = request.json.get('data')
    if not request_data:
        return jsonify({'error': 'No data provided'}), 400

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    styles = getSampleStyleSheet()
    style_heading = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=24,
        alignment=TA_CENTER
    )
    
    style_subheading = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=18
    )
    
    style_normal = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=12
    )
    
    elements = []

    elements.append(Paragraph("AI Generated Water Quality Report", style_heading))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Comparison of Water Quality Indices across various locations.", style_subheading))
    elements.append(Spacer(1, 12))

    for item in request_data:
        elements.append(Paragraph(f"Location: {item['LOCATIONS']}", style_subheading))
        elements.append(Paragraph(f"State: {item['STATE']}", style_normal))
        elements.append(Spacer(1, 12))

        query = f"""
        Provide a detailed analysis of the water quality in {item['LOCATIONS']} at {item['STATE']} based on the following data:
        BOD: {item.get('BOD')}, CONDUCTIVITY: {item.get('CONDUCTIVITY')}, DO: {item.get('DO')}, 
                FECAL_COLIFORM: {item.get('FECAL_COLIFORM')}, NITRATE_N_NITRITE_N: {item.get('NIT        RATE_N_NITRITE_N')}, 
        STATION_CODE: {item.get('STATION_CODE')}, TEMP: {item.get('TEMP')}, TOTAL_COLIFORM: {item.get('TOTAL_COLIFORM')}, 
        pH: {item.get('pH')}
        Analyze these parameters in context with typical environmental factors and provide insights based on current environmental science.
        Include the following sections:
        1. Reason for Pollution
        2. Causes
        3. Consequences
        4. Suggested Solutions
        """
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}",
            headers={'Content-Type': 'application/json'},
            json={"contents": [{"parts": [{"text": query}]}]}
        )

        if response.status_code == 200:
            ai_response = response.json()
            ai_text = ai_response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            # Split the AI response into paragraphs
            for line in ai_text.split("\n"):
                if line.startswith("###"):
                    elements.append(Paragraph(line.replace("###", "").strip(), style_subheading))
                elif line.startswith("##"):
                    elements.append(Paragraph(line.replace("##", "").strip(), style_heading))
                else:
                    elements.append(Paragraph(line.strip().replace('**', ''), style_normal))
                elements.append(Spacer(1, 12))
        else:
            elements.append(Paragraph("Failed to get AI response", style_normal))
            elements.append(Spacer(1, 12))

        elements.append(PageBreak())

    doc.build(elements)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="water_quality_report.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)

