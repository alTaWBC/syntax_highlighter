import json
filename = r"C:\Users\William\Downloads\temp-20220419T142258Z-001\temp\temp\textmate\scopes.txt"


with open(filename, "r") as scopes:
    lines = scopes.readlines()
    dictionary = {scope.strip():index for index, scope in enumerate(lines)}
    with open("dict.txt", "w") as dicti:
        json.dump(dictionary, dicti)