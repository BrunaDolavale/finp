from flask import Flask, request, jsonify
import pyrebase
import requests
import json
from config import GPT_API_KEY, FIREBASE_CONFIG

app = Flask(__name__)

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
db = firebase.database()

@app.route('/categorize', methods=['POST'])
def categorize():
    data = request.json
    expense_text = data['expense']

    # Chamada à API do GPT
    gpt_response = categorize_expense(expense_text)
    
    if 'error' in gpt_response:
        return jsonify({'error': 'Erro ao categorizar o gasto'}), 500

    # Salvar no Firebase
    db.child("expenses").push(gpt_response)

    return jsonify(gpt_response), 200

def categorize_expense(expense_text):
    url = 'https://api.openai.com/v1/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {GPT_API_KEY}'
    }
    data = {
        'model': 'text-davinci-003',
        'prompt': f'Categorize the following expense: "{expense_text}"',
        'max_tokens': 50
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        result = response.json()
        # Aqui você pode precisar ajustar a extração dependendo da resposta da API
        return {
            "item": result.get('choices')[0].get('text').strip(),
            "value": 30,  # Supondo que a extração do valor foi feita corretamente
            "category": "Clothes"  # Supondo que a categoria foi extraída corretamente
        }
    else:
        return {'error': 'API request failed'}

if __name__ == '__main__':
    app.run(debug=True)
