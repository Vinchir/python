water_max = 0
errors = 0
attempt_top_up = 0
attempt_scoop = 0
quantity_scoop_water = 0
quantity_top_up_water = 0
failed_top_up = 0
failed_scoop = 0
count = 0
test = True


def time(time_a, time_b, data):
    global state
    state = time_a + '00' < data[:data.find('Z') - 2].replace('.', ':').replace('Т', 'T') < time_b + '00'
    return time_a + '00' < data[:data.find('Z') - 2].replace('.', ':').replace('Т', 'T') < time_b + '00'


def water_changes(all_water, data):
    global errors, attempt_scoop, attempt_top_up, quantity_scoop_water, \
        quantity_top_up_water, failed_top_up, failed_scoop
    if 'scoop' in data and all_water - int(data[data.find('p') + 2:data.find('l')]) >= 0:
        if state is True:
            attempt_scoop += 1
            quantity_scoop_water += int(data[data.find('p') + 2:data.find('l')])
        return all_water - int(data[data.find('p') + 2:data.find('l')])
    elif 'top up' in data and all_water + int(data[data.find('up') + 3:data.find('l')]) <= water_max:
        if state is True:
            attempt_top_up += 1
            quantity_top_up_water += int(data[data.find('up') + 3:data.find('l')])
        return all_water + int(data[data.find('up') + 3:data.find('l')])
    else:
        if state is True:
            if 'top up' in data:
                failed_top_up += int(data[data.find('up') + 3:data.find('l')])
                errors += 1
            elif 'scoop' in data:
                failed_scoop += int(data[data.find('p') + 2:data.find('l')])
                errors += 1
            return all_water


enter = input('Введите ссылку на файл и диапазон времени:').split(' ')
url = enter[0]
time1 = enter[1]
time2 = enter[2]
with open(url, 'r', encoding='UTF-8') as log:
    for line in log:
        if '(объем бочки)' in line:
            water_max = int(line[:line.find(' ')])
            continue
        if '(текущий объем воды в бочке)' in line:
            water_in_barrel = int(line[:line.find(' ')])
            continue
        if line != 'META DATA:\n' and line[:line.find('Z') - 2].replace('.', ':').replace('Т', 'T') > time2 + '00':
            break
        if time(time1, time2, line):
            water_in_barrel = water_changes(water_in_barrel, line)
        elif time(time1, time2, line):
            if test:
                water_in_barrel = water_changes(water_in_barrel, line)
                test = False
                count += 1
                continue
            water_in_barrel = water_changes(water_in_barrel, line)
        count += 1
errors = (errors / count) * 100
result = [str(attempt_top_up), str(errors), str(quantity_top_up_water), str(failed_top_up),
          str(attempt_scoop), str(quantity_scoop_water), str(failed_scoop)]
with open('result.csv', 'w') as file:
    file.write('количество попыток налить воду, процент ошибок, объем воды был налит,'
               'объем воды был не налит, количество попыток вычерпать воду, количество вычерпанной воды,'
               'количество воды неудалось вычерпать\n')
    file.write(', '.join(result))
