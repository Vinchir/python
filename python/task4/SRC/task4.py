import re


def compare_string(str1, str2):
    pattern = re.compile('\*+')
    str2 = pattern.sub('.*', str2)
    if re.findall(str2, str1)[0] == str1:
        print('ОК')
    else:
        print('КО')


compare_string(input('Введите первую строку:'), input('Введите вторую строку:'))
