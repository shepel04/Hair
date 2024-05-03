from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

service_records_json_file_path = 'service_records.json'
inventory_json_file_path = 'inventory.json'
employees_json_file_path = 'employees.json'

if not os.path.exists(service_records_json_file_path):
    with open(service_records_json_file_path, 'w') as f:
        json.dump([], f)

if not os.path.exists(inventory_json_file_path):
    with open(inventory_json_file_path, 'w') as f:
        json.dump({}, f)

service_records = []
employees = []
inventory = {}


# Business Logic Layer for Service Records
def check_service_availability(service_id, time):
    return True


def load_service_records():
    global service_records
    with open(service_records_json_file_path, 'r') as f:
        service_records = json.load(f)


def save_employees():
    with open(employees_json_file_path, 'w') as f:
        json.dump(employees, f, indent=4)


def save_service_records():
    with open(service_records_json_file_path, 'w') as f:
        json.dump(service_records, f, indent=4)


# Business Logic Layer for Inventory
def load_inventory():
    global inventory
    with open(inventory_json_file_path, 'r') as f:
        inventory = json.load(f)


def save_inventory():
    with open(inventory_json_file_path, 'w') as f:
        json.dump(inventory, f, indent=4)


# Presentation Layer for Service Records
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    client_name = data.get('client_name')
    service_id = data.get('service_id')
    time = data.get('time')

    # Business logic: Check service availability and time
    if not check_service_availability(service_id, time):
        return jsonify({'error': 'Service not available at the specified time'}), 400

    service_records.append({
        'client_name': client_name,
        'service_id': service_id,
        'time': time
    })

    save_service_records()

    return jsonify({'message': 'Registration successful'}), 200


@app.route('/appointments/<client_name>', methods=['GET'])
def get_appointments(client_name):
    load_service_records()

    appointments = [record for record in service_records if record['client_name'] == client_name]
    if not appointments:
        return jsonify({'message': 'No appointments found for the client'}), 404
    return jsonify(appointments), 200


# Presentation Layer for Inventory
@app.route('/inventory', methods=['GET'])
def get_inventory():
    load_inventory()
    return jsonify(inventory), 200


@app.route('/inventory', methods=['POST'])
def add_inventory_item():
    data = request.json

    item_id = data.get('item_id')
    item_name = data.get('item_name')
    quantity = data.get('quantity')

    load_inventory()
    if item_id in inventory:
        return jsonify({'error': 'Item with the same ID already exists'}), 400
    inventory[item_id] = {'item_name': item_name, 'quantity': quantity}
    save_inventory()

    return jsonify({'message': 'Item added to inventory'}), 200


@app.route('/inventory/<item_id>', methods=['PUT'])
def update_inventory_item(item_id):
    data = request.json

    item_name = data.get('item_name')
    quantity = data.get('quantity')

    load_inventory()
    if item_id not in inventory:
        return jsonify({'error': 'Item not found in inventory'}), 404
    inventory[item_id]['item_name'] = item_name
    inventory[item_id]['quantity'] = quantity
    save_inventory()

    return jsonify({'message': 'Item updated successfully'}), 200


@app.route('/inventory/<item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    load_inventory()
    if item_id not in inventory:
        return jsonify({'error': 'Item not found in inventory'}), 404
    del inventory[item_id]
    save_inventory()

    return jsonify({'message': 'Item deleted successfully'}), 200


# @app.route('/employees', methods=['POST'])
# def employee():
#     data = request.json
#
#     name = data.get('name')
#     position = data.get('position')
#     phone_number = data.get('phone_number')
#
#     employees.append({
#         'name': name,
#         'position': position,
#         'phone_number': phone_number
#     })
#
#     save_employees()
#
#     return jsonify({'message': 'Registration successful'}), 200


if __name__ == '__main__':
    app.run(debug=True)
