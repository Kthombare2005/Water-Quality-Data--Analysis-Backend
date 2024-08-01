# import pandas as pd

# # Load the dataset with latin1 encoding
# file_path = 'F:/Project\'s/Water-Quality-Data- Analysis/backend/data/waterquality.csv'
# data = pd.read_csv(file_path, encoding='latin1')

# # Remove rows with any empty field
# cleaned_data = data.dropna()

# # Save the cleaned data to a new CSV file
# cleaned_file_path = 'F:/Project\'s/Water-Quality-Data- Analysis/backend/data/cleaned_waterquality.csv'
# cleaned_data.to_csv(cleaned_file_path, index=False)

# print("Cleaned data saved to", cleaned_file_path)


import pandas as pd

# Load your dataset
file_path = 'data/cleaned_waterquality.csv'
data = pd.read_csv(file_path, encoding='latin1')

# Define pollution reasons and solutions for each state
pollution_reasons = {
    'MAHARASHTRA': [
        'Industrial discharge', 'Agricultural runoff', 'Urban waste', 'Improper sewage treatment'
    ],
    'ANDHRA PRADESH': [
        'Industrial waste', 'Agricultural chemicals', 'Sewage discharge', 'Sand mining'
    ],
    'UTTAR PRADESH': [
        'Industrial effluents', 'Domestic sewage', 'Agricultural runoff', 'Religious rituals and festivals'
    ],
    'BIHAR': [
        'Sewage discharge', 'Industrial pollution', 'Agricultural runoff', 'Inadequate waste management'
    ],
    'WEST BENGAL': [
        'Industrial waste', 'Agricultural chemicals', 'Urban runoff', 'Deforestation'
    ],
    'ASSAM': [
        'Oil spills', 'Tea industry effluents', 'Deforestation', 'Urban waste'
    ],
    'KARNATAKA': [
        'Industrial waste', 'Urban runoff', 'Agricultural chemicals', 'Sewage discharge'
    ],
    'HIMACHAL PRADESH': [
        'Hydropower projects', 'Deforestation', 'Urban runoff', 'Industrial waste'
    ],
    'KERALA': [
        'Agricultural runoff', 'Industrial waste', 'Sewage discharge', 'Urban runoff'
    ],
    'TAMILNADU': [
        'Industrial effluents', 'Agricultural chemicals', 'Urban waste', 'Sewage discharge'
    ],
    'MADHYA PRADESH': [
        'Agricultural runoff', 'Industrial waste', 'Urban waste', 'Sewage discharge'
    ],
    'RAJASTHAN': [
        'Industrial effluents', 'Agricultural runoff', 'Urban waste', 'Desertification'
    ],
    'PUNJAB': [
        'Agricultural chemicals', 'Industrial waste', 'Sewage discharge', 'Urban runoff'
    ],
    'GOA': [
        'Mining waste', 'Tourism-related waste', 'Industrial discharge', 'Urban runoff'
    ],
    'GUJARAT': [
        'Industrial effluents', 'Agricultural chemicals', 'Urban runoff', 'Sewage discharge'
    ],
    # Add more states...
}

pollution_solutions = {
    'TEMP': [
        'Planting trees along water bodies to provide shade and reduce water temperature',
        'Creating artificial lakes and wetlands to absorb heat',
        'Regulating industrial discharge temperatures',
        'Implementing cooling systems in industrial plants'
    ],
    'DO': [
        'Installing aeration devices in water bodies to increase oxygen levels',
        'Reducing organic waste input by improving waste management practices',
        'Controlling algae growth through chemical or biological means',
        'Restoring river flow regimes to improve oxygenation'
    ],
    'pH': [
        'Neutralizing acidic or basic water with appropriate chemicals',
        'Regulating industrial discharges to maintain pH balance',
        'Planting vegetation to reduce soil erosion and buffer pH changes',
        'Using limestone to neutralize acidic waters'
    ],
    'CONDUCTIVITY': [
        'Reducing the use of salts and chemicals in agriculture',
        'Implementing better wastewater treatment processes',
        'Controlling industrial discharges of salts and chemicals',
        'Monitoring and managing urban runoff'
    ],
    'BOD': [
        'Improving wastewater treatment facilities to reduce organic load',
        'Reducing industrial effluents through better treatment processes',
        'Promoting organic farming practices to reduce chemical runoff',
        'Encouraging community waste management initiatives'
    ],
    'NITRATE_N_NITRITE_N': [
        'Implementing buffer strips along water bodies to absorb nitrates',
        'Reducing the use of nitrogen-based fertilizers in agriculture',
        'Improving sewage treatment to reduce nitrate discharges',
        'Promoting organic farming practices'
    ],
    'FECAL_COLIFORM': [
        'Improving sanitation and sewage treatment facilities',
        'Promoting the use of toilets and proper waste disposal methods',
        'Implementing disinfection processes in water treatment',
        'Conducting public awareness campaigns on hygiene practices'
    ],
    'TOTAL_COLIFORM': [
        'Upgrading sewage treatment plants to reduce coliform levels',
        'Implementing chlorination and other disinfection methods in water supply',
        'Ensuring proper waste disposal and reducing open defecation',
        'Monitoring and managing agricultural runoff'
    ],
    # Add more parameters...
}

# Function to get pollution reasons for a state
def get_pollution_reasons(state):
    return '; '.join(pollution_reasons.get(state, ['Unknown']))

# Function to get solutions for a parameter
def get_pollution_solutions(parameter):
    return '; '.join(pollution_solutions.get(parameter, ['Unknown']))

# Assuming the correct column names are 'STATE' and 'PARAMETER'
data['Pollution_Reasons'] = data['STATE'].apply(get_pollution_reasons)

# Apply solutions for each specific pollution parameter
data['TEMP_Solutions'] = get_pollution_solutions('TEMP')
data['DO_Solutions'] = get_pollution_solutions('DO')
data['pH_Solutions'] = get_pollution_solutions('pH')
data['CONDUCTIVITY_Solutions'] = get_pollution_solutions('CONDUCTIVITY')
data['BOD_Solutions'] = get_pollution_solutions('BOD')
data['NITRATE_N_NITRITE_N_Solutions'] = get_pollution_solutions('NITRATE_N_NITRITE_N')
data['FECAL_COLIFORM_Solutions'] = get_pollution_solutions('FECAL_COLIFORM')
data['TOTAL_COLIFORM_Solutions'] = get_pollution_solutions('TOTAL_COLIFORM')

# Save the updated dataframe to a new CSV file
updated_file_path = 'data/updated_waterquality.csv'
data.to_csv(updated_file_path, index=False)

print(f'Updated CSV saved to {updated_file_path}')

