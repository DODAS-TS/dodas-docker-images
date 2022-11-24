with open("./token.dat") as file:
    lines = [line.rstrip() for line in file]
    
print(lines[1])