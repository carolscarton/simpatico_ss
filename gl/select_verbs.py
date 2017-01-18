f = open("dicc.src", "r")

for s in f.readlines():
    tokens = s.split(" ")
    tag = tokens[2]
    if tag[0] == "V":
        print s.strip()
