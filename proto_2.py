from flask import Flask
from flask import request
import json
import time
import random
app = Flask(__name__)


current_users = []
disease_json_file = open("final.json","r")
disease_data = json.load(disease_json_file)
disease_json_file.close()
all_symptoms = []; all_disease_list = []
for disease in disease_data:
    all_symptoms.extend(disease["Symptoms"])
    all_disease_list.append(disease["Disease"])
all_symptoms = list(set(all_symptoms)) #remove duplicates
assert len(all_disease_list)==133
test_symp = ""
@app.route('/', methods=['GET', 'POST'])
def hello():
    convo_starters = ["Hey there! How are you feeling today?", "Today is a great day outside! But are you feeling great today?", \
    "I had a great nap...but enough about me, tell me about you.", "Good morning! Or is it actually a good morning?", "Hi hi! What's up with you?"]
    convo_enders = ["Cool! Remember to drink water and stay hydrated today. :D", "Great! Remember to eat your vegetables today! ;)", \
    "Have fun out there! But use sunscreen if you must."]
    user_list = []; convo_started = False
    global current_users
    global disease_data
    if len(request.form["message"]) < 2:
        return json.dumps("Hmm... I didn't quite catch that...")
    for user_dict in current_users:
        for e in list(user_dict.keys()):
            user_list.append(e)
    if request.form["user_id"] not in user_list:
        msg = random.choice(convo_starters); convo_started = True
        user_list.append(request.form["user_id"])
        current_users.append({request.form["user_id"]:{"symptoms":[],"diseases":all_disease_list}})
        return json.dumps({"message":msg, "flag":0})
    elif request.form["user_id"] in user_list:
        print("OLD")
        user_ind = 0
        for i in range(len(current_users)):
            if request.form["user_id"] == list(current_users[i].keys())[0]:
                user_ind = i; break
        if request.form["message"].lower() == "yes":
            global test_symp
            current_users[user_ind][request.form["user_id"]]["symptoms"].append(test_symp)
        #print("CONV")
        convo_started = False
        if "i" in request.form["message"].lower():
            if "fine" in request.form["message"].lower() or "good" in request.form["message"].lower() or "well" in request.form["message"].lower():
                msg = random.choice(convo_enders)
                return json.dumps({"message":msg, "flag":0})
        #print("NO CONV")
        words = request.form["message"].split(" ")
        for word in words:
            if word in all_symptoms:
                current_users[user_ind][request.form["user_id"]]["symptoms"].append(word)
                #next line is to remove duplicates
                current_users[user_ind][request.form["user_id"]]["symptoms"] = list(set(current_users[user_ind][request.form["user_id"]]["symptoms"]))
        print("SYM", current_users[user_ind][request.form["user_id"]]["symptoms"])
        delete_diseases = []
        for disease in disease_data:
            disease_symptoms = disease["Symptoms"]
            for symptom in current_users[user_ind][request.form["user_id"]]["symptoms"]:
                if symptom not in disease_symptoms:
                    delete_diseases.append(disease["Disease"])
        delete_diseases = list(set(delete_diseases))
        for disease in delete_diseases:
            try:
                current_users[user_ind][request.form["user_id"]]["diseases"].remove(disease)
            except ValueError:
                # when value is not present
                pass
        test_symp = ""
        for dis in current_users[user_ind][request.form["user_id"]]["diseases"]:
            for disease in disease_data:
                if dis == disease["Disease"]:
                    test_symp = random.choice(disease["Symptoms"])
                    break
        print("D ", len(current_users[user_ind][request.form["user_id"]]["diseases"]))
        if len(current_users[user_ind][request.form["user_id"]]["diseases"]) == 1:
            msg = "You may have " + ", ".join(current_users[user_ind][request.form["user_id"]]["diseases"])
            return json.dumps({"message":msg, "flag":2}) # 2 means stop chat
        if len(current_users[user_ind][request.form["user_id"]]["diseases"]) == 0:
            msg = "Your disease could not be diagnosed :( Contact the doctor for help..."
            return json.dumps({"message":msg, "flag":2})
        if len(current_users[user_ind][request.form["user_id"]]["diseases"]) < 4 and len(current_users[user_ind][request.form["user_id"]]["symptoms"]) > 3:
            msg = "You may have " + ", ".join(current_users[user_ind][request.form["user_id"]]["diseases"])
            return json.dumps({"message":msg, "flag":2}) # 2 means stop chat
        print(current_users[user_ind][request.form["user_id"]]["diseases"])
        print("D ", len(current_users[user_ind][request.form["user_id"]]["diseases"]))
        print("END")
        if test_symp == "":
            return json.dumps({"message":"How do you feel?", "flag":0})
        return json.dumps({"message":"Do you feel any: {}?".format(test_symp), "flag":1}) # 1 - yes/no question #but don't enforce inline keyboard


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
