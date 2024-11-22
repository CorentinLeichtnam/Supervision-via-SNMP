from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Fichier JSON pour sauvegarder les équipements
EQUIPMENT_FILE = "equipment.json"

# Charger les équipements à partir du fichier JSON
def load_equipments():
    if not os.path.exists(EQUIPMENT_FILE):
        return []
    with open(EQUIPMENT_FILE, "r") as file:
        return json.load(file)

# Sauvegarder les équipements dans le fichier JSON
def save_equipments(equipments):
    with open(EQUIPMENT_FILE, "w") as file:
        json.dump(equipments, file, indent=4)

@app.route("/")
def index():
    equipments = load_equipments()
    return render_template("index.html", equipments=equipments)

@app.route("/add", methods=["POST"])
def add_equipment():
    name = request.form.get("name")
    ip = request.form.get("ip")
    description = request.form.get("description")

    if not name or not ip:
        return jsonify({"error": "Name and IP address are required"}), 400

    equipment = {
        "name": name,
        "ip": ip,
        "description": description
    }

    equipments = load_equipments()
    equipments.append(equipment)
    save_equipments(equipments)

    return jsonify({"message": "Equipment added successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
