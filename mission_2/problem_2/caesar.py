import string

def caesar_cipher_decode(target_text):
    alphabet = string.ascii_lowercase
    print(f"[*] 입력 텍스트: {target_text}")

    for shift in range(26):
        decoded_text = ''
        for char in target_text:
            if char in alphabet:
                idx = (alphabet.index(char) - shift) % 26
                decoded_text += alphabet[idx]
            else:
                decoded_text += char
        print(f"Shift {shift}: {decoded_text}")

    selected_shift = int(input("해독된 결과 중 올바른 shift 번호를 입력하세요: "))
    final_text = ''
    for char in target_text:
        if char in alphabet:
            idx = (alphabet.index(char) - selected_shift) % 26
            final_text += alphabet[idx]
        else:
            final_text += char

    with open('result.txt', 'w') as f:
        f.write(final_text)
    print(f"[*] 최종 해독 결과 저장 완료: result.txt")


if __name__ == '__main__':
    with open('password.txt', 'r') as f:
        encrypted_text = f.read().strip()
    caesar_cipher_decode(encrypted_text)
