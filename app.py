import os
from flask import Flask, request, render_template, jsonify
import pandas as pd
import openai

app = Flask(__name__, template_folder=".")

# Configure OpenAI API key
openai.api_key = 'your_api_key_here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'csv_file' not in request.files:
        return "No CSV file provided."

    file = request.files['csv_file']

    if file.filename == '':
        return "No selected file."

    if file:
        try:
            # Save the uploaded CSV file
            filename = file.filename
            file.save(os.path.join('uploads', filename))

            # Parse the CSV using pandas
            data = pd.read_csv(os.path.join('uploads', filename), encoding='utf-8', errors='replace')

            # Analyze the data (Replace this with your own analysis)
            analysis_report = f"CSV file '{filename}' has {len(data)} rows and {len(data.columns)} columns."

            # Generate a report using ChatGPT
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"Analyzing CSV file: {analysis_report}",
                max_tokens=100,
            )

            report = response.choices[0].text

            return report

        except Exception as e:
            return str(e)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
