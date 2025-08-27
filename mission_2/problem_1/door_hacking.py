import zipfile
import itertools
import string
import time


def unlock_zip():
    zip_file = 'emergency_storage_key.zip'
    chars = string.ascii_lowercase + string.digits  # a-z + 0-9
    password_length = 6
    attempt_count = 0

    print(f"[*] 암호 해독 시작: {time.ctime()}")
    start_time = time.time()

    with zipfile.ZipFile(zip_file) as zf:
        for pwd_tuple in itertools.product(chars, repeat=password_length):
            attempt_count += 1
            password = ''.join(pwd_tuple)
            try:
                zf.extractall(pwd=bytes(password, 'utf-8'))
                end_time = time.time()
                print(f"[*] 성공! 암호: {password}")
                print(f"[*] 시도 횟수: {attempt_count}, 진행 시간: {end_time - start_time:.2f} 초")
                with open('password.txt', 'w') as f:
                    f.write(password)
                return password
            except:
                if attempt_count % 100000 == 0:
                    elapsed = time.time() - start_time
                    print(f"[*] 시도 횟수: {attempt_count}, 진행 시간: {elapsed:.2f} 초")

if __name__ == '__main__':
    unlock_zip()
