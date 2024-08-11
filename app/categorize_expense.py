import requests
import json
from .config import Config

def categorize_expense(expense_text):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {Config.GPT_API_KEY}'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {"role": "system", "content": "You are a financial assistant."},
            {"role": "user", "content": (
                f'Categorize o seguinte gasto, extraia o valor dele em reais e determine o tipo de compartilhamento: '
                f'"{expense_text}". O resultado deve atender à seguinte estrutura de exemplo do json: '
                f'{{"category": "vestuário", "item": "blusa", "value": 30, "sharing_type": "Meio a Meio"}}. '
                f'Os tipos de compartilhamento podem ser: "Bruna", "Bruno", "Meio a Meio", "Proporcional". '
                f'Use "Bruna" se o texto não indicar claramente outra pessoa.' 
            )}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        choices = result.get('choices', [])
        if choices:
            message_content = choices[0]['message']['content'].strip()
            try:
                expense_info = json.loads(message_content)
            except json.JSONDecodeError:
                lines = message_content.split("\n")
                expense_info = {
                    "item": "desconhecido",
                    "value": 0,
                    "category": "desconhecido",
                    "sharing_type": "Bruna"
                }
                for line in lines:
                    parts = line.split(":")
                    if len(parts) == 2:
                        key, value = parts
                        key = key.strip().lower()
                        value = value.strip()
                        if "item" in key:
                            expense_info["item"] = value
                        elif "value" in key:
                            try:
                                expense_info["value"] = float(value)
                            except ValueError:
                                expense_info["value"] = 0
                        elif "category" in key:
                            expense_info["category"] = value
                        elif "sharing_type" in key:
                            expense_info["sharing_type"] = value
            return expense_info
        else:
            return {'error': 'No choices returned by API'}
    else:
        return {'error': 'API request failed'}
