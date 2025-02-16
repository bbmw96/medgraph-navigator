import json
import random
from datetime import datetime, timedelta

def generate_demo_data():
    """
    Generate sample medical data for demonstration purposes
    """
    patients = []
    conditions = []
    medications = []
    encounters = []
    
    # Common medical conditions and medications
    condition_list = [
        "Type 2 Diabetes",
        "Hypertension",
        "Coronary Artery Disease",
        "Asthma",
        "COPD",
        "Depression",
        "Anxiety",
        "Osteoarthritis"
    ]
    
    medication_list = [
        "Metformin",
        "Lisinopril",
        "Atorvastatin",
        "Albuterol",
        "Sertraline",
        "Ibuprofen",
        "Omeprazole",
        "Amoxicillin"
    ]
    
    # Generate 100 sample patients
    for i in range(100):
        patient_id = f"P{i+1}"
        patient = {
            "_key": patient_id,
            "age": random.randint(25, 85),
            "gender": random.choice(["M", "F"]),
            "location": "Slough, UK",
            "registration_date": (datetime.now() - timedelta(days=random.randint(365, 1825))).strftime("%Y-%m-%d")
        }
        patients.append(patient)
        
        # Generate conditions and medications for each patient
        num_conditions = random.randint(2, 5)
        for _ in range(num_conditions):
            condition = random.choice(condition_list)
            medication = random.choice(medication_list)
            
            # Create encounter
            encounter_id = f"E{len(encounters)+1}"
            encounters.append({
                "_key": encounter_id,
                "patient_id": patient_id,
                "date": (datetime.now() - timedelta(days=random.randint(1, 365))).strftime("%Y-%m-%d"),
                "type": "Diagnosis"
            })
            
            # Add condition
            conditions.append({
                "_key": f"C{len(conditions)+1}",
                "patient_id": patient_id,
                "encounter_id": encounter_id,
                "description": condition,
                "status": random.choice(["Active", "Managed", "Resolved"])
            })
            
            # Add medication
            medications.append({
                "_key": f"M{len(medications)+1}",
                "patient_id": patient_id,
                "encounter_id": encounter_id,
                "description": medication,
                "status": random.choice(["Active", "Discontinued"])
            })
    
    return {
        "patients": patients,
        "conditions": conditions,
        "medications": medications,
        "encounters": encounters
    }

if __name__ == "__main__":
    demo_data = generate_demo_data()
    # Save to file
    with open("demo_data.json", "w") as f:
        json.dump(demo_data, f, indent=2)
    print(f"Generated {len(demo_data['patients'])} patients with conditions and medications")
