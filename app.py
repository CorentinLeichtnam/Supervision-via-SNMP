from flask import Flask, render_template, request, jsonify
import json
import os
from snmp_monitor import SNMPMonitor  # Importer le module SNMPMonitor

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

@app.route("/monitor/<int:id>", methods=["GET"])
def monitor_equipment(id):
    """
    Surveille un équipement via SNMP.
    """
    equipments = load_equipments()
    equipment = next((e for e in equipments if e["id"] == id), None)

    if not equipment:
        return jsonify({"error": "Equipment not found"}), 404

    # Initialisez une session SNMPMonitor
    ip = equipment["ip"]
    community = "public"  # Personnalisez si besoin
    monitor = SNMPMonitor(ip, community)

    # Récupérez des données SNMP
    sys_name_oid = "1.3.6.1.2.1.1.5.0"  # Nom de l'équipement (sysName)
    sys_uptime_oid = "1.3.6.1.2.1.1.3.0"  # Temps de fonctionnement (sysUpTime)

    sys_name = monitor.get_snmp_data(sys_name_oid)
    sys_uptime = monitor.get_snmp_data(sys_uptime_oid)

    return jsonify({
        "name": sys_name if sys_name else "Unknown",
        "uptime": sys_uptime if sys_uptime else "Unknown"
    })

if __name__ == "__main__":
    app.run(debug=True)
