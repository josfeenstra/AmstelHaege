import json
import os

jsonPATH = "C:\\Users\\Jos\\GitHub\\UrbanPlanning\\Rhino\\json"
print(os.getcwd())
os.chdir(jsonPATH)
print(os.getcwd())

data = {}
data['people'] = []
data['people'].append({
    'name': 'kaas',
    'website': 'schijt.com',
    'from': 'henk'
})
data['people'].append({
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan'
})
data['people'].append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})

with open("kaas.txt", "w") as jsonFile:

    jsonFile.seek(0)  # rewind
    json.dump(data, jsonFile)
    jsonFile.truncate()

try:
    outFile = open('P4Output.txt','w')
    outFile.write(json.dumps(data))
    outFile.close()
except IOError as strerror:
    print("I/O error({0}): {1}".format(errno, strerror))
