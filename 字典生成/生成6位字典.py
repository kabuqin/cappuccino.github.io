for i in range(1000000):
    with open("../四位字典.txt", "a") as f:
        f.write(f'{i:06}' + '\n')