for i in range(10000):
    with open("../四位字典.txt", "a") as f:
        f.write(f'{i:04}' + '\n')