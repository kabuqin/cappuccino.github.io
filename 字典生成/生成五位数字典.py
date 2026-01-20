def generate_5_digit_numbers():
    # 创建一个空列表来存储5位数的值
    five_digit_numbers = []

    # 循环生成从00000到99999的所有数字
    for i in range(100000):
        # 将数字格式化为5位数的字符串，不足的前面补0
        five_digit_number = str(i).zfill(5)
        # 将5位数添加到列表中
        five_digit_numbers.append(five_digit_number)

    return five_digit_numbers


# 调用函数生成5位数的值列表
five_digit_numbers = generate_5_digit_numbers()

# 将5位数的值保存到文本文件中
with open('5位数字典.txt', 'w', encoding='utf-8') as file:
    for number in five_digit_numbers:
        # 将每个5位数写入文件，每个数字占一行
        file.write(number + '\n')

print("5位数的值已保存到5位数字典.txt文件中。")