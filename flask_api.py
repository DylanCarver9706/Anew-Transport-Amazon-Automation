from flask import Flask, request, jsonify

import json
from webcrawler import update_order_child_statuses

# Open the JSON file
with open('auth.json', 'r') as file:
    # Load the JSON data
    auth_data = json.load(file)

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def api():
    # Assuming the request contains JSON data
    request_data = request.get_json()

    # Validate the data


    response_data = update_order_child_statuses(request_data["order_numbers_list"], auth_data["pro_username"], auth_data["pro_password"])
    print(response_data)
    # Return a JSON response
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)