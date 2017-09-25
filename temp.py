import json

disease_json_file = open("test.json","r")
disease_data = json.load(disease_json_file)
print(disease_data)
all_symptoms = []; disease_symptoms = []
for disease in disease_data[:3]:
    print(disease)
    all_symptoms.extend(disease["Symptoms"])
    disease_symptoms = disease["Symptoms"]
    print(disease_symptoms)
#print(all_symptoms)
