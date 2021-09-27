from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from flask import render_template
from flask.json import JSONEncoder
from database import create_connection, db_query, db_read_query

connection = create_connection("app.sqlite")
app = Flask(__name__)

initialQuery = """
CREATE TABLE IF NOT EXISTS banks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    interest_rate INTEGER NOT NULL,
    maximum_loan INTEGER NOT NULL,
    minimum_down_payment INTEGER NOT NULL,
    loan_term INTEGER NOT NULL
);
"""
db_query(connection, initialQuery)


@app.route('/api/get_banks', methods=['GET'])
def get_banks():
    query = "SELECT * from banks"
    db_banks = db_read_query(connection, query)
    banks = []
    keys = ['id', 'name', 'interest_rate', 'maximum_loan', 'minimum_down_payment', 'loan_term']
    for val in db_banks:
        bank = {}
        for i in range(len(val)):
            bank[keys[i]] = val[i]
        banks.append(bank)
    return jsonify({'banks' : banks})

@app.route('/api/get_bank/<int:bank_id>', methods=['GET'])
def get_bank(bank_id):
    query = f"""
    SELECT * from users WHERE id = {bank_id} 
    """
    db_bank = db_read_query(connection, query)
    bank = {}
    keys = ['id', 'name', 'interest_rate', 'maximum_loan', 'minimum_down_payment', 'loan_term']
    for i in range(len(db_bank)):
        bank[keys[i]] = db_bank[i]
    return jsonify({'bank': bank})

@app.route('/api/add_bank', methods=['POST'])
def add_bank():
    print(request.json)
    for key in request.json:
        if request.json[key] is None:
            abort(400)
    if not request.json:
        abort(400)
    query = f"""
    INSERT INTO 
        banks (name, interest_rate, maximum_loan, minimum_down_payment, loan_term)
    VALUES
    ('{request.json['name']}', {request.json['interest_rate']}, {request.json['maximum_loan']}, {request.json['minimum_down_payment']}, {request.json['loan_term']})
    """
    db_query(connection, query)
    return "bank added",201

@app.route('/api/edit_bank/<int:bank_id>', methods=['PUT'])
def edit_bank(bank_id):
    query = f"""
    UPDATE
        banks
    SET
        name = "{request.json['name']}",
        interest_rate = {request.json['interest_rate']},
        minimum_down_payment = {request.json['minimum_down_payment']},
        loan_term = {request.json['loan_term']}
    WHERE
        id = {bank_id}
    """
    db_query(connection, query)
    return "edit successful", 200

@app.route('/api/delete_bank/<int:bank_id>', methods=['DELETE'])
def delete_bank(bank_id):
    query = f"DELETE from banks WHERE id = {bank_id}"
    db_query(connection, query)
    return jsonify({'result':True})
    
    


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/banks')
def banks_template():
    return render_template('banks.html')

@app.route('/addbank')
def addbank_template():
    return render_template('addbank.html')

@app.route('/bankadded')
def bankadded_template():
    return render_template('addedbank.html')

@app.route('/edit_bank')
def editbank_template():
    return render_template('editbank.html')

@app.route('/delete_bank')
def delete_bank_template():
    return render_template('delete_bank.html')

@app.route('/mortgage')
def mortgage_template():
    return render_template('mortgage.html')

if __name__ == '__main__':
    app.run(debug=True)