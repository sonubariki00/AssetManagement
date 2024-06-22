import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load data from JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

@app.route("/api/assets", methods=["GET"])
def get_assets():
    return jsonify(data["assets"])

@app.route("/api/assets/<string:asset_id>", methods=["GET"])
def get_asset(asset_id):
    asset = next((asset for asset in data["assets"] if asset["asset_id"] == asset_id), None)
    if asset:
        return jsonify(asset)
    return jsonify({"error": "Asset not found"}), 404

@app.route("/api/employees", methods=["GET"])
def get_employees():
    return jsonify(data["employees"])

@app.route("/api/employees/<string:employee_id>", methods=["GET"])
def get_employee(employee_id):
    employee = next((employee for employee in data["employees"] if employee["employee_id"] == employee_id), None)
    if employee:
        return jsonify(employee)
    return jsonify({"error": "Employee not found"}), 404

@app.route("/api/requests", methods=["POST"])
def make_request():
    new_request = request.get_json()
    new_request["status"] = "pending"
    data["asset_requests"].append(new_request)
    with open('data.json', 'w') as f:
        json.dump(data, f ,)
    return jsonify({
        "id": len(data["asset_requests"]) - 1,
        "asset_id": new_request["asset_id"],
        "employee_id": new_request["employee_id"],
        "status": new_request["status"]
    }), 201

@app.route("/api/requests/log", methods=["GET"])
def get_request_log():
    log_data = []
    for i, req in enumerate(data["asset_requests"]):
        try:
            asset_name = next((asset["name"] for asset in data["assets"] if asset["asset_id"] == req["asset_id"]), None)
            employee_name = next((employee["first_name"] for employee in data["employees"] if employee["employee_id"] == req["employee_id"]), None)
            log_data.append({
                "id": i,
                "asset_name": asset_name,
                "employee_name": employee_name,
                "status": req["status"],
                "timestamp": "",
                "result": "Pass" if req["status"] == "approved" else "Fail"
            })
        except KeyError as e:
            print(f"KeyError: {e} in request {req}")
            log_data.append({
                "id": i,
                "asset_name": "Unknown",
                "employee_name": "Unknown",
                "status": req.get("status", "Unknown"),
                "timestamp": "",
                "result": "Fail"
            })

    return jsonify(log_data)


@app.route("/api/assets/search", methods=["GET"])
def search_assets():
    search_query = request.args.get("q")
    assets = data["assets"]
    filtered_assets = [asset for asset in assets if search_query.lower() in asset["name"].lower() or search_query.lower() in asset.get("model", "").lower()]
    return jsonify(filtered_assets)

if __name__ == "__main__":
    app.run(debug=True)

