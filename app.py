from flask import Flask, jsonify, request
import requests
import os
from members import create_new_member, select_members, find_member_by_id, delete_member_by_id, reset_db, replace_member, update_member

app = Flask(__name__)

# ROUTES
@app.route('/', methods=['GET'])
def read_all():
    result = select_members()
    return jsonify(result[1]), result[0]

# RESET
@app.route('/reset', methods=['GET'])
def reset():
    reset_db()
    result = select_members()
    return jsonify(result[1]), result[0]

# --- MEMEBERS
# GET ALL MEMBERS
@app.route('/members', methods=['GET'])
def members():
    result = select_members()
    return jsonify(result[1]), result[0]

# POST NEW MEMBER
@app.route('/members', methods=['POST'])
def create_member():
    data = request.get_json()
    result = []

    if isinstance(data, dict):
        # If data is a single dictionary, call create_new_member once
        result = create_new_member(data)

    elif isinstance(data, list):
        # If data is a list of dictionaries, iterate and call create_new_member for each
        for member in data:
            result = create_new_member(member)
    else:
        return jsonify({"error": "Invalid input format"}), 400
    
    return jsonify(result[1]), result[0]


# PUT MEMBER (REPLACE/UPDATE DATA)
@app.route('/members/<int:member_id>', methods=['PUT'])
def put_member(member_id):
    data = request.get_json()
    result = []

    if isinstance(data, dict):
        # If data is a single dictionary, call create_new_member
        result = replace_member(member_id, data)
    else:
        return jsonify({"error": "Invalid input format. Must be a dict"}), 400
    
    return jsonify(result[1]), result[0]


# PATCH MEMBER (UPDATE PART OF THE DATA)
@app.route('/members/<int:member_id>', methods=['PATCH'])
def patch_member(member_id):
    data = request.get_json()
    result = [{"message": "Something went wrong"}, 500]

    if isinstance(data, dict):
        # If data is a single dictionary, call create_new_member
        result = update_member(member_id, data)
    else:
        return jsonify({"error": "Invalid input format. Must be a dict"}), 400
    
    return jsonify(result[1]), result[0]


# DELETE MEMBER BY ID
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = find_member_by_id(member_id)
    if member[0] == 200:
        result = delete_member_by_id(member_id)
        return jsonify(result[1]), result[0]
    else:
        return jsonify({"error": "Member not found"}), 404


# GET MEMBER BY ID
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    result = find_member_by_id(member_id)
    return jsonify(result[1]), result[0]


# --- GITHUB API
@app.route('/api/members/<int:member_id>', methods=['GET'])
def show_member_api(member_id):
    member = find_member_by_id(member_id)
    if member[0] == 200 and member[1]["github_username"]:

        if member["github_username"].lower() == "detgrey": # My own username
            
            github_access_token = os.getenv('GITHUB_ACCESS_TOKEN')
            url = f'https://api.github.com/user/repos'
            headers = {'Authorization': f'token {github_access_token}'}
            req = requests.get(url, headers=headers)
            return req.json(), req.status_code
        
        else:

            url = f'https://api.github.com/users/{member["github_username"]}/repos'
            print(url)
            req = requests.get(url)
            return req.json(), req.status_code
        
    else:
        return jsonify({"error": "Member not found or does not have a github username"}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050)