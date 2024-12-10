with open(filename, 'r') as infile:
    lines = infile.readlines()

with open(filename, 'w') as outfile:
    for line in lines:
        if not line.strip():
            continue
        outfile.write(line)