#bmi088_parser.py

old_data_str = ''
data_cap_complete = True
incomplete_count = 0

def parse_data(data):
    global old_data_str, data_cap_complete, incomplete_count
    new_data = old_data_str + data

    if data_cap_complete:
        if '#' in new_data:
            data = new_data.split('#')[1]
            if '\n' in data:
                full_data = data.split('\n')[0]
                old_data_str = data.split('\n')[1]
                data_cap_complete = True
                incomplete_count = 0
                if len(old_data_str) > 35:
                    print('old_data_str has a lot of data')
                    print(old_data_str)
                    sys.exit()
                return data_cap_complete, full_data
            else:
                data_cap_complete = False
                return data_cap_complete, data
        else:
            incomplete_count += 1
            if incomplete_count > 2:
                old_data_str = ''
                data_cap_complete = True
            return False, new_data
    else:
        if '\n' in new_data:
            full_data = new_data.split('\n')[0]
            old_data_str = data.split('\n')[1]
            data_cap_complete = True
            incomplete_count = 0
            if len(old_data_str) > 35:
                print('old_data_str has a lot of data')
                print(old_data_str)
                sys.exit()
            return data_cap_complete, full_data

        else:
            incomplete_count += 1
            if incomplete_count > 2:
                old_data_str = ''
                data_cap_complete = True
            return False, new_data

def break_data(data):
    output = dict()
    split_data = data.split(',')
    output['time'] = split_data[0]
    output['ax'] = split_data[1]
    output['ay'] = split_data[2]
    output['az'] = split_data[3]
    output['gx'] = split_data[4]
    output['gy'] = split_data[5]
    output['gz'] = split_data[6]

    return output
