# Code by Ivy Ardanaz - 2024

def keep_modulo_26(password):
    converted_password = password
    for i in range(5):
        letter_in_ord = ord(converted_password[i])
        if letter_in_ord >= 0x5B:
            converted_password[i] = chr(letter_in_ord - 0x1A)
        elif letter_in_ord <= 0x40:
            converted_password[i] = chr(letter_in_ord + 0x1A)
        
    return converted_password


def generate_password(original_password) -> str:
    # validation
    if len(original_password) != 5:
        return "INVALID PASSWORD"
    
    if not original_password.isalpha() or not original_password.isupper():
        return "INVALID PASSWORD"
    
    # scrambling
    converted_password = [""] * 5
    converted_password[0] = original_password[3]
    converted_password[1] = original_password[0]
    converted_password[2] = original_password[4]
    converted_password[3] = original_password[1]
    converted_password[4] = original_password[2]

    # transforming each letter
    converted_password[0] = ord(converted_password[0]) ^ 0x13
    converted_password[0] = chr(converted_password[0] + 0x03)

    converted_password[1] = ord(converted_password[1]) ^ 0x04
    converted_password[1] = chr(converted_password[1] + 0x12)

    converted_password[2]  = ord(converted_password[2]) ^ 0x06
    converted_password[2] = chr(converted_password[2] + 0x04)

    converted_password[3]  = ord(converted_password[3]) ^ 0x11
    converted_password[3] = chr(converted_password[3] + 0x07)

    converted_password[4]  = ord(converted_password[4]) ^ 0x01
    converted_password[4] = chr(converted_password[4] + 0x10)

    # keep it modulo 26
    converted_password = keep_modulo_26(converted_password)

    # do some magic with the first and last letter of the original passowrd
    magic_first_letter = ord(original_password[4]) & 0x17
    magic_last_letter = ord(original_password[0]) & 0x17

    for i in range(5):
        converted_password[i] = ord(converted_password[i]) ^ magic_first_letter
        converted_password[i] = chr(converted_password[i] ^ magic_last_letter)

    # keep it modulo 26
    converted_password = keep_modulo_26(converted_password)

    return "".join(converted_password)
    
print(generate_password(input()))
