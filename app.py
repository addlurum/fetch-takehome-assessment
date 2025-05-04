from flask import Flask, request, jsonify
from uuid import uuid4
from datetime import datetime
import math
import re

app = Flask(__name__)
receipts_data = {}

# === Input Validation Functions ===
def is_valid_receipt(receipt):
    try:
        # Required fields
        required_fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]
        if not all(field in receipt for field in required_fields):
            return False

        # Pattern checks
        if not re.match(r"^[\w\s\-\&]+$", receipt["retailer"]):
            return False
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", receipt["purchaseDate"]):
            return False
        if not re.match(r"^\d{2}:\d{2}$", receipt["purchaseTime"]):
            return False
        if not re.match(r"^\d+\.\d{2}$", receipt["total"]):
            return False
        if not isinstance(receipt["items"], list) or len(receipt["items"]) == 0:
            return False

        for item in receipt["items"]:
            if not all(k in item for k in ["shortDescription", "price"]):
                return False
            if not re.match(r"^[\w\s\-]+$", item["shortDescription"].strip()):
                return False
            if not re.match(r"^\d+\.\d{2}$", item["price"]):
                return False

    except Exception:
        return False

    return True

# === Business Logic ===
def calculate_points(receipt):
    points = 0

    # 1 point per alphanumeric character in retailer name
    points += sum(c.isalnum() for c in receipt.get("retailer", ""))

    total = float(receipt.get("total", "0"))

    # 50 points if total is a round dollar amount
    if total.is_integer():
        points += 50

    # 25 points if total is multiple of 0.25
    if (total * 100) % 25 == 0:
        points += 25

    items = receipt.get("items", [])
    points += (len(items) // 2) * 5

    for item in items:
        desc = item.get("shortDescription", "").strip()
        price = float(item.get("price", "0"))
        if len(desc) % 3 == 0:
            points += math.ceil(price * 0.2)

    # 6 points if day is odd
    try:
        day = int(receipt["purchaseDate"].split("-")[2])
        if day % 2 == 1:
            points += 6
    except:
        pass

    # 10 points if time is between 14:00 and 16:00
    try:
        time = datetime.strptime(receipt["purchaseTime"], "%H:%M").time()
        if time >= datetime.strptime("14:00", "%H:%M").time() and time < datetime.strptime("16:00", "%H:%M").time():
            points += 10
    except:
        pass

    return points

# === Endpoints ===

@app.route("/receipts/process", methods=["POST"])
def process_receipt():
    receipt = request.get_json()

    if not receipt or not is_valid_receipt(receipt):
        return jsonify({"message": "The receipt is invalid"}), 400

    receipt_id = str(uuid4())
    receipts_data[receipt_id] = calculate_points(receipt)

    return jsonify({"id": receipt_id}), 200

@app.route("/receipts/<receipt_id>/points", methods=["GET"])
def get_points(receipt_id):
    if receipt_id not in receipts_data:
        return jsonify({"message": "No receipt found for that ID."}), 404

    return jsonify({"points": receipts_data[receipt_id]}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
