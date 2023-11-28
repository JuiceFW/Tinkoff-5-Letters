import progressbar
import os

a = "russian_nouns.txt" # Первый файл, который будем скрещивать
b = "words.txt" # Второй файл, который будем скрещивать
c = "words.txt" # Результат

def get_data_from_file(name: str) -> list:
    """Чтение строчек файла"""
    if os.path.exists(name):
        with open(name, encoding='utf-8') as file:
            return file.read().splitlines()
    else:
        print("[ERROR] Файл отсутствует!")
        return []

def main() -> None:
    data = get_data_from_file(a)
    data2 = get_data_from_file(b)

    max_length = len(data) + len(data2)

    # Создаем progressbar. Его число будет зависить от числа amount.
    bar = progressbar.ProgressBar(
        max_value=max_length)
    amount = 0

    copies_found = 0
    uniq_words = 0

    all_words = []

    for item in data: # Проходимся по списку из файла a
        amount += 1
        bar.update(amount) # Обновляем progressbar "привязывая" amount.

        if item not in all_words:
            all_words.append(item)
            uniq_words += 1
        else:
            copies_found += 1

    for item in data2: # Проходимся по списку из файла b
        amount += 1
        bar.update(amount)

        if item not in all_words:
            all_words.append(item)
            uniq_words += 1
        else:
            copies_found += 1

    print("Записываю....")
    with open(c, "w", encoding='utf-8') as file: # Записываем результат в файл c
        for val, item in enumerate(all_words):
            if val == 0: # Проверка на то, нужно ли писать с новой строчки или нет.
                file.write(item)
            else:
                file.write("\n" + item)

    # Выводим результаты.
    print(f"Всего слов: [{max_length}]")
    print(f"Уникальных слов: [{uniq_words}]")
    print(f"Найдено копий: [{copies_found}]")

if __name__ == "__main__":
    main()