import json
filename = "cred.json"

with open(filename, 'r') as open_file:
    database = json.load(open_file)

username = input("Username : ")
password = input("Password : ")

if username and password :
    database[username] = password


with open(filename, 'w') as open_file:
    json.dump(database, open_file, indent=2, sort_keys=True)