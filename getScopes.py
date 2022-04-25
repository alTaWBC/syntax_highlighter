import re

filename = r"C:\Users\William\Downloads\temp-20220419T142258Z-001\temp\temp\textmate\m.tmLanguage"
regex = ">((?:\w+\.(?:\w+\.)\w+)+)<"


with open(filename, "r") as matlab_scopes:
    content = matlab_scopes.read()
    scopes = re.findall(regex, content)

with open("scopes.txt", "w") as matlab_scopes:
    print("\n".join(scopes), file=matlab_scopes)