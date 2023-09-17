import os
from flask import Flask, request, render_template, jsonify
import pandas as pd
import openai

app = Flask(__name__, template_folder=".")

# Configure OpenAI API key
openai.api_key = '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'

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
            data = pd.read_csv(os.path.join('uploads', filename), encoding='iso-8859-1')

            # Analyze the data (Replace this with your own analysis)
            analysis_report = f"CSV file '{filename}' has {len(data)} rows and {len(data.columns)} columns."

            # Generate a report using ChatGPT
            messages = [
                {"role": "system", "content": "You are a helpful data analytical assistant, that can read trends and come to conclusions"},
                {"role": "user", "content": "Please give me a good summary of what data you are analying from the CSV file that was sent, go through the rows and columns and logically come up with your own conclusion on what the data is trying to tell you, and relay it, showing signfiicant figures from the data"},
                {"role": "assistant", "content": analysis_report}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            
            report = response.choices[0].message['content']

            return report

        except Exception as e:
            return str(e)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
