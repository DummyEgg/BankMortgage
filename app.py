from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from flask import render_template
app = Flask(__name__)

banks = [
    {
        'id' : 0,
        'name' : 'Test Bank',
        'interest_rate' : 10.00,
        'maximum_loan' : 100000,
        'minimum_down_payment' : 20.00,
        'loan_term' : 12,
    }
]

@app.route('/api/get_banks', methods=['GET'])
def get_tasks():
    return jsonify({'banks' : banks})

@app.route('/api/get_bank/<int:bank_id>', methods=['GET'])
def get_task(bank_id):
    bank = filter(lambda temp: temp['id'] == bank_id, banks)
    if len(bank) == 0:
        abort(404)
    return jsonify({'bank': bank[0]})

@app.route('/api/add_bank', methods=['POST'])
def add_bank():
    print(request.json)
    if not request.json:
        abort(400)
    bank = {
        'id': banks[-1]['id'] + 1,
        'name': request.json['name'],
        'interest_rate' : request.json['interest_rate'],
        'maximum_loan' : request.json['maximum_loan'],
        'minimum_down_payment' : request.json['minimum_down_payment'],
        'loan_term' : request.json['loan_term']
    }
    banks.append(bank)
    return jsonify({'bank': bank}), 201

@app.route('/api/edit_bank/<int:bank_id>', methods=['PUT'])
def edit_bank(bank_id):
    if not bank_id:
        abort(404)
    if not request.json:
        abort(400)
    bank = filter(lambda temp: temp['id'] == bank_id, banks)
    if 'name' in request.json and type(request.json['name']) != str:
        abort(400)
    if 'interest_rate' in request.json and type(request.json['interest_rate']) is not float:
        abort(400)
    if 'maximum_loan' in request.json and type(request.json['maximum_loan']) is not int:
        abort(400)
    if 'minimum_down_payment' in request.json and type(request.json['minimum_down_payment']) is not float:
        abort(400)
    if 'loan_term' in request.json and type(request.json['loan_term']) is not int:
        abort(400)
    bank[0]['name'] = request.json.get('name', bank[0]['name'])
    bank[0]['interest_rate'] = request.json.get('interest_rate', bank[0]['interest_rate'])
    bank[0]['maximum_loan'] = request.json.get('maximum_loan', bank[0]['maximum_loan'])
    bank[0]['minimum_down_payment'] = request.json.get('minimum_down_payment', bank[0]['minimum_down_payment'])
    bank[0]['loan_term'] = request.json.get('loan_term', bank[0]['loan_term'])
    return jsonify({'bank' : bank[0]})

@app.route('/api/delete_bank/<int:bank_id>', methods=['DELETE'])
def delete_bank(bank_id):
    bank = filter(lambda temp: temp['id'] == bank_id, banks)
    if len(bank) == 0:
        abort(404)
    banks.remove(bank[0])
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

if __name__ == '__main__':
    app.run(debug=True)