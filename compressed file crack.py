import zipfile
import rarfile
import py7zr
import random
import string
import timeit
from concurrent.futures import ThreadPoolExecutor

def generate_random_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def extract_zip_with_password(zip_path, password):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            zip_file.extractall(pwd=password.encode())
        return True
    except Exception as e:
        return False

def extract_rar_with_password(rar_path, password):
    try:
        with rarfile.RarFile(rar_path, 'r') as rar_file:
            rar_file.extractall(pwd=password)
        return True
    except Exception as e:
        return False

def extract_7z_with_password(sevenzip_path, password):
    try:
        with py7zr.SevenZipFile(sevenzip_path, 'r', password=password) as sevenzip_file:
            sevenzip_file.extractall()
        return True
    except Exception as e:
        return False

def extract_with_password(file_path, password, file_type):
    if file_type == 'zip':
        return extract_zip_with_password(file_path, password)
    elif file_type == 'rar':
        return extract_rar_with_password(file_path, password)
    elif file_type == '7z':
        return extract_7z_with_password(file_path, password)
    else:
        return False

def extract_with_dictionary(file_path, dictionary_path, file_type):
    with open(dictionary_path, 'r', encoding='utf-8') as dictionary_file:
        passwords = dictionary_file.read().splitlines()

    start_time = timeit.default_timer()
    with ThreadPoolExecutor() as executor:
        futures = []
        for password in passwords:
            future = executor.submit(extract_with_password, file_path, password, file_type)
            futures.append(future)

        for idx, future in enumerate(futures):
            if future.result():
                elapsed_time = timeit.default_timer() - start_time
                print(f"Password found: {passwords[idx]}")
                print(f"Elapsed time: {elapsed_time:.2f} seconds")
                break
            else:
                print(f"Current password: {passwords[idx]}")

        else:
            print("Password not found in the dictionary.")

def extract_with_random_password(file_path, password_length, file_type):
    start_time = timeit.default_timer()
    with ThreadPoolExecutor() as executor:
        while True:
            password = generate_random_password(password_length)
            future = executor.submit(extract_with_password, file_path, password, file_type)
            if future.result():
                elapsed_time = timeit.default_timer() - start_time
                print(f"Password found: {password}")
                print(f"Elapsed time: {elapsed_time:.2f} seconds")
                break
            else:
                print(f"Current password: {password}")

# 사용자로부터 압축 파일 정보 및 옵션 입력 받기
file_path = input("압축 파일 경로를 입력하세요: ")
file_type = input("압축 파일의 종류를 입력하세요 (zip, rar, 7z): ")

# 사용자로부터 옵션 입력 받기
option = input("암호를 풀 옵션을 선택하세요 (1: 사전 대입, 2: 완전히 무작위): ")

# 사용자가 옵션 1을 선택한 경우
if option == '1':
    dictionary_path = "password_list.txt"
    extract_with_dictionary(file_path, dictionary_path, file_type)

# 사용자가 옵션 2를 선택한 경우
elif option == '2':
    password_length = int(input("생성할 비밀번호의 길이를 입력하세요: "))
    extract_with_random_password(file_path, password_length, file_type)

# 유효하지 않은 옵션 입력한 경우
else:
    print("유효하지 않은 옵션입니다.")
