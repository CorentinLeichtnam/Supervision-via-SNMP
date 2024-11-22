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
        equipments = json.load(file)

    # Ajouter un ID unique si un équipement n'en a pas
    for index, equipment in enumerate(equipments):
        if "id" not in equipment:
            equipment["id"] = index + 1  # Assigner un ID unique basé sur l'index

    save_equipments(equipments)  # Sauvegarder les modifications si nécessaire
    return equipments

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

    equipments = load_equipments()

    # Trouver le plus grand ID existant et générer un nouvel ID
    new_id = max([equipment.get("id", 0) for equipment in equipments], default=0) + 1

    equipment = {
        "id": new_id,
        "name": name,
        "ip": ip,
        "description": description
    }

    equipments.append(equipment)
    save_equipments(equipments)

    return jsonify({"message": "Equipment added successfully"}), 200

@app.route("/update/<int:id>", methods=["POST"])
def update_equipment(id):
    equipments = load_equipments()
    for equipment in equipments:
        if equipment["id"] == id:
            equipment["name"] = request.form.get("name", equipment["name"])
            equipment["ip"] = request.form.get("ip", equipment["ip"])
            equipment["description"] = request.form.get("description", equipment["description"])
            save_equipments(equipments)
            return jsonify({"message": "Equipment updated successfully"}), 200
    return jsonify({"error": "Equipment not found"}), 404

@app.route("/delete/<int:id>", methods=["POST"])
def delete_equipment(id):
    equipments = load_equipments()
    
    # Vérifiez si l'équipement avec l'ID donné existe
    if not any(equipment["id"] == id for equipment in equipments):
        return jsonify({"error": "Equipment not found"}), 404

    # Supprimez l'équipement correspondant
    equipments = [equipment for equipment in equipments if equipment["id"] != id]
    save_equipments(equipments)
    
    return jsonify({"message": "Equipment deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
