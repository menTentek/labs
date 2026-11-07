
# Хэмминг коды
HAMMING_TASKS = {
    1: {
        "info": "0100",
        "error_position": 3,
        "parity_count": 3
    },
    11: {
        "info": "11001010",
        "error_position": 3,
        "parity_count": 4
    }
}

#Префикстік код
PREFIX_TASKS = {
    1: {
        "alphabet_size": 23,
        "message": "0110110111"
    },
    11: {
        "alphabet_size": 135,
        "message": "1011100110"
    }
}

PREFIX_CODE = {
    "A": "0",
    "B": "10",
    "C": "110",
    "D": "111"
}


def hamming_encode(info, parity_count):
    """Ақпараттық комбинацияны Хэмминг кодына түрлендіреді."""
    n = len(info) + parity_count
    code = [0] * (n + 1)

    parity_positions = [2 ** i for i in range(parity_count)]

    data_index = 0
    for position in range(1, n + 1):
        if position not in parity_positions:
            code[position] = int(info[data_index])
            data_index += 1

    print("\n1-ЕСЕП. ХЭММИНГ КОДЫН ҚҰРУ")
    print("Ақпараттық комбинация:", info)
    print("Ақпараттық бит саны:", len(info))
    print("Бақылау биттерінің саны:", parity_count)
    print("Жалпы бит саны:", n)
    print("Бақылау позициялары:", parity_positions)

    for p in parity_positions:
        checked_positions = [
            position for position in range(1, n + 1)
            if position & p and position != p
        ]

        parity = 0
        for position in checked_positions:
            parity ^= code[position]

        code[p] = parity

        expression = " XOR ".join(
            f"a{position}" for position in checked_positions
        )
        print(f"a{p} = {expression} = {parity}")

    result = "".join(str(code[position]) for position in range(1, n + 1))
    print("Қорытынды кодтық комбинация C:", result)
    return result


def detect_and_correct_error(correct_code, error_position, parity_count):
    """Қабылданған кодтағы бір бит қатесін тауып, түзетеді."""
    received = list(correct_code)

    index = error_position - 1
    received[index] = "1" if received[index] == "0" else "0"
    received_code = "".join(received)

    print("\n2-ЕСЕП. ҚАТЕНІ АНЫҚТАУ ЖӘНЕ ТҮЗЕТУ")
    print("Дұрыс код C:        ", correct_code)
    print("Бұрмаланған позиция:", error_position)
    print("Қабылданған код C*:", received_code)

    bits = [0] + [int(bit) for bit in received_code]
    n = len(received_code)
    syndrome = 0
    syndrome_values = []

    for i in range(parity_count):
        p = 2 ** i
        checked_positions = [
            position for position in range(1, n + 1)
            if position & p
        ]

        check_value = 0
        for position in checked_positions:
            check_value ^= bits[position]

        syndrome_values.append(check_value)
        syndrome += check_value * p

        print(
            f"E{i + 1} = {check_value}; "
            f"тексерілетін позициялар: {checked_positions}"
        )

    syndrome_binary = "".join(str(value) for value in reversed(syndrome_values))
    print("Синдром (екілік):", syndrome_binary)
    print("Синдром (ондық):", syndrome)

    if 1 <= syndrome <= n:
        corrected = list(received_code)
        corrected[syndrome - 1] = (
            "1" if corrected[syndrome - 1] == "0" else "0"
        )
        print(f"{syndrome}-позициядағы бит инверсияланды.")
        print("Түзетілген код:", "".join(corrected))
    elif syndrome == 0:
        print("Қате анықталған жоқ.")
    else:
        print("Синдром код ұзындығынан үлкен. Бір разрядты түзету мүмкін емес.")


def run_hamming(variant):
    task = HAMMING_TASKS[variant]

    print("\n" + "=" * 50)
    print(f"ӘН8. ХЭММИНГ КОДЫ. {variant}-НҰСҚА")
    print("=" * 50)

    correct_code = hamming_encode(
        task["info"],
        task["parity_count"]
    )

    detect_and_correct_error(
        correct_code,
        task["error_position"],
        task["parity_count"]
    )

def check_fano_condition(code):
    """Кодтық сөздердің префикс шартына сәйкестігін тексереді."""
    words = list(code.values())

    for i in range(len(words)):
        for j in range(len(words)):
            if i != j and words[j].startswith(words[i]):
                return False

    return True

def decode_message(message, code):
    """Хабарды солдан оңға қарай префикстік кодпен декодтайды."""
    reverse_code = {
        code_word: symbol for symbol, code_word in code.items()
    }

    decoded = []
    current_code = ""
    separated_codes = []

    for bit in message:
        current_code += bit

        if current_code in reverse_code:
            decoded.append(reverse_code[current_code])
            separated_codes.append(current_code)
            current_code = ""

    print("Бөлінген кодтық сөздер:", " | ".join(separated_codes))

    if current_code:
        print("Декодталмаған қалдық биттер:", current_code)

    return "".join(decoded)


def run_prefix(variant):
    task = PREFIX_TASKS[variant]
    alphabet_size = task["alphabet_size"]
    message = task["message"]

    print("\n" + "=" * 50)
    print(f"9. ПРЕФИКСТІК КОД. {variant}-НҰСҚА")
    print("=" * 50)

    print("\n1-ЕСЕП. БІРКЕЛКІ ЕКІЛІК КОД")
    print("Алфавиттегі символдар саны N =", alphabet_size)

    k = 0
    while 2 ** k < alphabet_size:
        k += 1

    print(f"2^{k} = {2 ** k} >= {alphabet_size}")
    print("Бір символға қажетті ең аз бит саны:", k)

    print("\n2-ЕСЕП. ПРЕФИКСТІК КОДТЫ ДЕКОДТАУ")
    print("Код кестесі:")
    for symbol, code_word in PREFIX_CODE.items():
        print(f"{symbol} = {code_word}")

    print("Фано шарты орындала ма?", "Иә" if check_fano_condition(PREFIX_CODE) else "Жоқ")
    print("Берілген хабар:", message)

    decoded = decode_message(message, PREFIX_CODE)
    print("Декодталған хабар:", decoded)


def main():
    print("=" * 50)
    print("Хэмминг коды")
    print("Префикстік кодтар. Фано шарты")
    print("=" * 50)

    while True:
        variant = input("\nНұсқаны таңдаңыз (1 немесе 11): ").strip()
        if variant in ("1", "11"):
            variant = int(variant)
            break
        print("Тек 1 немесе 11 нұсқасын енгізіңіз.")

    print("\nТапсырманы таңдаңыз:")
    print("1 - ӘН8 (Хэмминг коды)")
    print("2 - ӘН9 (Префикстік код)")
    print("3 - Екеуін де орындау")

    while True:
        choice = input("Таңдауыңыз (1/2/3): ").strip()
        if choice in ("1", "2", "3"):
            break
        print("1, 2 немесе 3 енгізіңіз.")

    if choice in ("1", "3"):
        run_hamming(variant)

    if choice in ("2", "3"):
        run_prefix(variant)

    print("\nБағдарлама аяқталды.")


if __name__ == "__main__":
    main()
