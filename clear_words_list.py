import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(BASE_DIR)

def get_words() -> list:
    """Получаем все слова из файла words.txt"""

    with open("words.txt", encoding='utf-8') as file:
        return file.read().splitlines()

def main() -> None:
    if not os.path.exists("words.txt"): # Проверка на наличие словаря
        print("[ERROR] No file words.txt found!")
        os._exit(0)

    words = get_words() # Получаем все слова из словаря
    if not words:
        print("[ERROR] No words in file words.txt!")
        os._exit(0)
    else:
        print(f"[INFO] Найдено [{len(words)}] слов!")

    print("[INFO] Обработка слов...") # Проверяем слова на длину в 5 символов
    new_words = []
    for item in words:
        if len(item) != 5:
            continue

        if "-" in item:
            continue

        new_words.append(item)

    words = new_words.copy()
    new_words = []

    with open("words.txt", "w", encoding='utf-8') as file:
        for val, word in enumerate(words):
            if val == 0:
                file.write(word)
            else:
                file.write("\n" + word)

if __name__ == "__main__":
    main()