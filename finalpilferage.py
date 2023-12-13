from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/pilferage', methods=['POST'])
def check_pilferage():
    try:
        # Get the CSV file from the request
        csv_file = request.files['file']
        
        # Read CSV into a DataFrame
        data = pd.read_csv(csv_file)
        
        # Initialize lists to store sensor numbers for different categories
        warning = []
        high_risk = []
        pilferage = []
        
        # Check flow rates and categorize sensor numbers
        for index, row in data.iterrows():
            if 58.047065380418914 <= row['flow_rate'] < 59.547065380418914:
                warning.append(row['sensor_no'])
            elif 59.547065380418915 <= row['flow_rate'] < 60.000000380418914:
                high_risk.append(row['sensor_no'])
            elif row['flow_rate'] >= 60.000000380418915:
                pilferage.append(row['sensor_no'])

        # Prepare response
        response = {
            'warning': warning,
            'high_risk': high_risk,
            'pilferage': pilferage
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
