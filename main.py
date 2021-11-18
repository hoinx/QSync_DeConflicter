
# Solasys QSync De-Confliter
import hashlib
import os
import re

test_mode = True

verbose = True
#verbose = Falsegit


'''

md5_hash = hashlib.md5()

a_file = open("test.txt", "rb")
content = a_file.read()
md5_hash.update(content)

digest = md5_hash.hexdigest()
print(digest)

'''

database = {}


def to_clean_path(conflicted_source_folder, target_folder, path):
    path_clean = re.sub(r"(_Konflikt_\(\d{1,2}\))", r"", path)
    relative_path = os.path.relpath(path_clean, conflicted_source_folder)
    return os.path.join(target_folder, relative_path)


def create_dir(dir):
    if verbose:
        print(dir)
    if test_mode:
        return
    os.makedirs(dir, exist_ok=True)


def store_dup_file(dup_file, target):
    md5_hash = hashlib.md5()

    a_file = open(dup_file, "rb")
    content = a_file.read()

    all_null = True
    for x in content:
        if x != 0:
            all_null = False
            break
    if all_null:
        if verbose:
            print("ALL NULL ...")
        return

    md5_hash.update(content)
    digest = md5_hash.hexdigest()

    if target in database:
        entry = database[target]
        print(f'Different Version ... MD5: {digest} Path: {dup_file}')
    else:
        database[target] = {}
        entry = database[target]

    if digest in entry:
        checksum_entry = entry[digest]
        if verbose:
            print("Duplicate ...")
        return  # optional, if not return, we collect all duplicates with same checksum
    else:
        entry[digest] = []
        checksum_entry = entry[digest]

    checksum_entry.append(dup_file)

    if verbose:
        print(f'MD5: {digest} Path: {dup_file}')

    if test_mode:
        return


def dedup(conflicted_source_folder, target_folder):
    print('-----------------------------------------------------------------')
    print('                   Solasys QSync De-Conflict')
    print('-----------------------------------------------------------------')
    print(f'Source:, {conflicted_source_folder}')
    print(f'Target: {target_folder}')
    print()
    print('-----------------------------------------------------------------')

    for subdir, dirs, files in os.walk(conflicted_source_folder):
        for dir in dirs:

            dir_path = os.path.join(subdir, dir)
            clean_path = to_clean_path(conflicted_source_folder, target_folder, dir_path)
            create_dir(clean_path)

        for file in files:
            file_path = os.path.join(subdir, file)
            clean_path = to_clean_path(conflicted_source_folder, target_folder, file_path)
            store_dup_file(file_path, clean_path)

    # print(database)

'''

In [2]: re.sub(r"\.(00|11)\.", r"X\1X", ".00..0..11.")
Out[2]: 'X00X.0.X11X'


path = "/home / User / Desktop / file.txt"
start = "/home / User"  
relative_path = os.path.relpath(path, start)




'''


if __name__ == '__main__':

    conflicted = '...'  # source path absolute
    cleanedup = '...'  # target path absolute

    dedup(conflicted, cleanedup)
