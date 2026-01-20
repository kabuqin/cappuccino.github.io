def calculate_check_digit(id17):
    # 系数
    coefficients = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 校验码对应值
    check_code_dict = {
        0: '1', 1: '0', 2: 'X', 3: '9', 4: '8',
        5: '7', 6: '6', 7: '5', 8: '4', 9: '3', 10: '2'
    }
    # 计算校验码
    sum_of_products = sum(int(id17[i]) * coefficients[i] for i in range(17))
    remainder = sum_of_products % 11
    return check_code_dict[remainder]

def generate_id_dict():
    id_dict = {}
    for i in range(10**17):  # 17位数字共有10^17种组合
        id17 = str(i).zfill(17)  # 格式化为17位数字，不足的前面补0
        check_digit = calculate_check_digit(id17)  # 计算校验码
        id_dict[id17] = id17 + check_digit  # 将完整的18位身份证号码作为值
    return id_dict

# 生成字典
id_dict = generate_id_dict()

# 将字典保存到文本文件中
with open('身份证后6位字典.txt', 'w', encoding='utf-8') as file:
    for id17, full_id in id_dict.items():
        # 仅保存后6位（包括校验码）
        file.write(full_id[-6:] + '\n')

print("身份证后6位字典已保存到身份证后6位字典.txt文件中。")