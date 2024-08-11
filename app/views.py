from flask import render_template, request, jsonify
from app import app, db
from .categorize_expense import categorize_expense

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categorize', methods=['POST'])
def categorize():
    data = request.json
    expense_text = data['expense']
    
    gpt_response = categorize_expense(expense_text)
    
    if 'error' in gpt_response:
        return jsonify({'error': 'Erro ao categorizar o gasto'}), 500
    
    try:
        result = db.child("expenses").push(gpt_response)
    except Exception as e:
        return jsonify({'error': 'Erro ao salvar no Firebase'}), 500

    return jsonify(gpt_response), 200

@app.route('/expenses')
def expenses():
    try:
        expenses = db.child("expenses").get().val()
        if not expenses:
            expenses = {}
        return render_template('expenses.html', expenses=expenses)
    except Exception as e:
        return jsonify({'error': 'Erro ao recuperar dados do Firebase'}), 500
