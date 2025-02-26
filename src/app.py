"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, render_template_string
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route("/", methods=["GET"])
def welcome():
    return render_template_string("""
        <html>
            <body style="text-align: center;">
                <h1>Welcome to the Jackson Family API!</h1>
                <p>Click the button below to see the family members:</p>
                <a href="{{ url_for('get_members') }}">
                    <button style="padding: 10px 20px; font-size: 16px;">See Members</button>
                </a>
            </body>
        </html>
    """)

@app.route("/members", methods=["GET"])
def get_members():
    return jsonify(jackson_family.get_all_members()), 200

@app.route("/member/<int:member_id>", methods=["GET"])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

@app.route("/member", methods=["POST"])
def add_member():
    member = request.get_json()
    if not member or "first_name" not in member or "age" not in member or "lucky_numbers" not in member:
        return jsonify({"error": "Invalid request body"}), 400
    new_member = jackson_family.add_member(member)
    return jsonify(new_member), 200

@app.route("/member/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    member = jackson_family.get_member(member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
    jackson_family.delete_member(member_id)
    return jsonify({"done": True}), 200

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
