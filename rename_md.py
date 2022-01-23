import os

def get_file_date_list(file_name_list):
    date_list = []
    for file_name in file_name_list:
        f = open(file_path+file_name, 'r')
        date_line = f.readlines()[3]
        
        date_list.append(date_line.split(': ')[1].strip())
        
    return date_list

def format_date(date_str):
    str_list = date_str.split('-')
    for i in range(len(str_list)):
        if len(str_list[i]) == 1:
            str_list[i] = '0' + str_list[i]

    return '-'.join(str_list)

if __name__ == '__main__':

    # get file list
    file_path = '/mnt/c/Users/spwii/Dropbox/Blog/_posts/'
    os.chdir(file_path)
    file_name_list = os.popen('ls').read().strip().split('\n')
    print(f'name_list: {file_name_list}')

    # get date list
    date_list = get_file_date_list(file_name_list)
    print(f'date_list: {date_list}')

    # rename file
    for i in range(len(date_list)):
        if file_name_list[i].startswith('2'):
            continue

        cmd = 'mv ' + file_name_list[i] + ' ' + format_date(date_list[i]) + '-' + file_name_list[i]
        print(f'cmd: {cmd}')
        os.system(cmd)















