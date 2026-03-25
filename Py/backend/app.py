# backend/app.py
from flask import Flask, render_template, request
from flask_cors import CORS
from pymongo import MongoClient

from config import Config
from routes.hospitals import hospital_bp
from routes.incidents import incident_bp
from routes.patients import patient_bp

app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)
CORS(app)

# Mongo client attached to app config
mongo_client = MongoClient(Config.MONGO_URI)
app.config["MONGO_CLIENT"] = mongo_client

# Global variable to store latest location from ESP32
latest_location = {"lat": None, "lng": None}

# APIs
app.register_blueprint(hospital_bp, url_prefix="/api/hospitals")
app.register_blueprint(incident_bp, url_prefix="/api/incidents")
app.register_blueprint(patient_bp, url_prefix="/api/patients")

# Pages
@app.route("/")
def dashboard():
    try:
        db_h = mongo_client["hospital_db"]
        db_p = mongo_client["patient_vitals"]
        hospital_count = db_h["bangalore_hospitals"].count_documents({})
        incident_count = db_h["incidents"].count_documents({})
        patient_count = db_p["records"].count_documents({})
        ambulance_count = db_h["ambulances"].count_documents({}) if "ambulances" in db_h.list_collection_names() else 0
    except Exception as e:
        hospital_count = 0
        incident_count = 0
        patient_count = 0
        ambulance_count = 0
    return render_template("dashboard.html",
                           hospital_count=hospital_count,
                           incident_count=incident_count,
                           patient_count=patient_count,
                           ambulance_count=ambulance_count)

@app.route("/report")
def report():
    return render_template("report_emergency.html")

@app.route("/hospitals")
def hospitals_page():
    try:
        db = mongo_client["hospital_db"]
        hospitals = list(db["bangalore_hospitals"].find({}, {"_id": 0}))
    except Exception as e:
        hospitals = []
    return render_template("hospitals.html", hospitals=hospitals)

@app.route("/patients")
def patients_page():
    try:
        db = mongo_client["patient_vitals"]
        patients = list(db["records"].find({}, {"_id": 0}))
    except Exception as e:
        patients = []
    return render_template("patients.html", patients=patients)

@app.route("/incidents")
def incidents_page():
    try:
        db = mongo_client["hospital_db"]
        incidents = list(db["incidents"].find({}, {"_id": 0}))
    except Exception as e:
        incidents = []
    return render_template("incidents.html", incidents=incidents)

@app.route("/update", methods=["POST"])
def update_location():
    global latest_location
    lat = request.form.get("lat")
    lng = request.form.get("lng")
    if lat and lng:
        latest_location["lat"] = float(lat)
        latest_location["lng"] = float(lng)
        return {"status": "success", "lat": lat, "lng": lng}, 200
    return {"status": "error", "message": "Invalid data"}, 400

@app.route("/location")
def get_location():
    return {"lat": latest_location["lat"], "lng": latest_location["lng"]}

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
