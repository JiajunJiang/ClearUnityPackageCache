import os
import shutil
from os import path
import natsort
import sys
import getopt

cache_dir = path.expandvars(r'%LOCALAPPDATA%\Unity\cache')
npm_dir = path.expandvars(r'%LOCALAPPDATA%\Unity\cache\npm')
packages_dir = path.expandvars(r'%LOCALAPPDATA%\Unity\cache\packages')

keep_value = 3
skip_calculate_size = False


def clear_npm(path):
    for folder in os.listdir(path):
        clear_npm_scoped(path + "\\" + folder)


def clear_npm_scoped(path):
    path_folder = os.path.basename(path)
    for folder in os.listdir(path):
        if path_folder != folder:
            clear_npm_packages(path + "\\" + folder)


def clear_npm_packages(path):
    path_list = os.listdir(path)
    path_list = natsort.natsorted(path_list)
    length = max(len(path_list) - keep_value, 0)
    for i in range(0, length):
        remove_folder(path + "\\" + path_list[i])


def clear_packages(path):
    for folder in os.listdir(path):
        clear_packages_scoped(path + "\\" + folder)


def clear_packages_scoped(path):
    path_list = os.listdir(path)
    path_list = natsort.natsorted(path_list)
    package_name = ''
    list = []

    for folder in path_list:
        temp = folder.split('@')
        if len(temp) == 2:
            if package_name != temp[0]:
                length = max(len(list) - keep_value, 0)
                for i in range(0, length):
                    remove_folder(path + "\\" + package_name + "@" + list[i])

                package_name = temp[0]
                list.clear()
                list.append(temp[1])
            else:
                list.append(temp[1])


def remove_folder(path):
    shutil.rmtree(path)


def get_folder_size(path):
    size = 0
    for root, dirs, files in os.walk(path):
        size += sum(
            [os.path.getsize(os.path.join(root, name)) for name in files]
        )
    return size


def main(argv):
    try:
        options, args = getopt.getopt(argv, "k:s:", ["skip=", "keep="])
    except getopt.GetoptError:
        print("options error")
        sys.exit()

    for option, value in options:
        if option in ("-k", "--keep"):
            if value.isdigit():
                global keep_value
                keep_value = int(value)
            else:
                print("{0} is not digit".format(value))
                sys.exit()

        if option in ("-s", "--skip"):
            global skip_calculate_size
            skip_calculate_size = True

    if not skip_calculate_size:
        print("Start calculate the UnityCache size, may take some minutes")
        print("Total Unity Cache Size = %.2f GB" % (get_folder_size(cache_dir) / 1024 / 1024 / 1024))

    print("Start Clear Unity Cache")

    clear_npm(npm_dir)

    clear_packages(packages_dir)
    print("End Clear Unity Cache")

    if not skip_calculate_size:
        print("Remain Unity Cache Size = %.2f GB" % (get_folder_size(cache_dir) / 1024 / 1024 / 1024))


if __name__ == '__main__':
    main(sys.argv[1:])
