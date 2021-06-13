data = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def conversion(number, past_notation, notation):
    global data
    number = main(number, past_notation, notation)
    result = ''
    while number:
        number, count_index = divmod(int(number), len(notation))
        result += data[count_index]
    return result[::-1]


def main(number, past_notation, notation):
    try:
        number = int(number, int(past_notation))
        if len(notation) > 36:
            raise ValueError
        elif notation not in data:
            raise TypeError
        return number
    except (TypeError, ValueError):
        print('usage')


print(conversion(input('Введите число:'), input('Введите систему счисления данного числа(просто цифрой):'),
                 input('Введите систему счисления в которую перевести (в формате:"01", "012" и т.п.):')))