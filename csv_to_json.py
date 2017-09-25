#python file to convert csv disease file to json

import json
csvfile = open("convertcsv.csv", 'r')
json_list = list()
disease_dict = dict()
disease = ""; count_occurence = 0; symptoms =  []
#disease_done = False
for line in csvfile:
    if line.startswith(",,"):
        #disease_done = False
        symptoms.append(line[2:])
    else:
        #disease_done = True
        disease_dict["Symptoms"] = symptoms
        print("APPEND", disease_dict)
        print()
        json_list.append(disease_dict)
        disease_dict = dict(); symptoms = []
        #print(line.split(","))
        disease = line.split(",")[0]; count_occurence = line.split(",")[1]; symptoms.append(line.split(",")[2])
        disease_dict["Disease"] = disease
        disease_dict["Count"] = count_occurence
        disease_dict["Symptoms"] = symptoms
csvfile.close()
json_list = json_list[1:]
print(json_list)
json.dumps(json_list)
with open("final.json", 'w') as outfile:
    json.dump(json_list, outfile)
