import random

def insert_parity_bits(data_bits):
    codeword = [0] * 12
    data_positions = [2, 4, 5, 6, 8, 9, 10, 11]
    for bit, pos in zip(data_bits, data_positions):
        codeword[pos] = int(bit)
    return codeword

def calculate_parity_bits(codeword):
    for i in range(4):
        p = 2 ** i
        parity = 0
        for j in range(1, 13):
            if j & p:
                parity ^= codeword[j - 1]
        codeword[p - 1] = parity
    return codeword

def encode_byte(byte_str):
    data_bits = list(byte_str)
    codeword = insert_parity_bits(data_bits)
    codeword = calculate_parity_bits(codeword)
    return codeword

def simulate_error(codeword, error_position=None):
    if error_position is None:
        error_position = random.randint(1, 12)
    codeword[error_position - 1] ^= 1
    return codeword, error_position

def calculate_syndrome(codeword):
    syndrome = 0
    for i in range(4):
        p = 2 ** i
        parity = 0
        for j in range(1, 13):
            if j & p:
                parity ^= codeword[j - 1]
        if parity != 0:
            syndrome += p
    return syndrome

def correct_error(codeword, syndrome):
    if 1 <= syndrome <= 12:
        codeword[syndrome - 1] ^= 1
    return codeword

def extract_data_bits(codeword):
    data_positions = [2, 4, 5, 6, 8, 9, 10, 11]
    return [str(codeword[i]) for i in data_positions]

def byte_to_bin_str(byte):
    return format(byte, '08b')

def write(report, line=""):
    print(line)
    report.write(line + "\n")

def main():
    input_text = "Прекрасно!"
    with open("report.txt", "w", encoding="utf-8") as report:

        write(report, f"Вхідне повідомлення: {input_text}\n")
        all_encoded = []

        write(report, "Кодування символів у код Хеммінга (12 бітів):\n")
        for ch in input_text:
            byte = ord(ch)
            bin_str = byte_to_bin_str(byte)
            codeword = encode_byte(bin_str)
            all_encoded.append(codeword[:])
            write(report, f"'{ch}' -> {bin_str} -> {''.join(map(str, codeword))}")

        write(report, "\nІмітація помилки:\n")
        error_index = random.randint(0, len(all_encoded) - 1)
        code_with_error = all_encoded[error_index][:]
        code_with_error, error_pos = simulate_error(code_with_error)
        write(report, f"Помилка в символі №{error_index + 1}, біт позиція {error_pos}")
        write(report, f"Зіпсований код: {''.join(map(str, code_with_error))}")

        write(report, "\nДекодування та виявлення помилки:\n")
        syndrome = calculate_syndrome(code_with_error)
        write(report, f"Синдром: {format(syndrome, '04b')} (десяткове: {syndrome})")
        if syndrome == 0:
            write(report, "Помилок не виявлено.")
        else:
            write(report, f"Виявлено помилку в позиції {syndrome}, виконується виправлення...")
            corrected = correct_error(code_with_error, syndrome)
            write(report, f"Після виправлення: {''.join(map(str, corrected))}")
            decoded_bits = extract_data_bits(corrected)
            decoded_char = chr(int(''.join(decoded_bits), 2))
            write(report, f"Розкодовано символ: '{decoded_char}'")

        write(report, "\nРозкодування всього повідомлення:")
        decoded_message = ""
        for i, codeword in enumerate(all_encoded):
            s = calculate_syndrome(codeword)
            corrected = correct_error(codeword[:], s)
            data_bits = extract_data_bits(corrected)
            decoded_char = chr(int(''.join(data_bits), 2))
            decoded_message += decoded_char
            write(report, f"Символ №{i + 1}: {''.join(map(str, codeword))} -> '{decoded_char}'")

        write(report, f"\nРезультат після декодування: {decoded_message}")
        write(report, "\n--- Кінець звіту ---")

if __name__ == "__main__":
    main()
