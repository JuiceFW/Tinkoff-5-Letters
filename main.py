import os
import progressbar

# Меняем директорию на директорию со скриптом.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(BASE_DIR)

def get_words() -> list:
    """Получаем все слова из файла words.txt"""
    with open("words.txt", encoding='utf-8') as file:
        return file.read().splitlines()

def get_same_count(word: str, letter: str, ignore: str = None) -> int:
    """Получаем количество повторений letter в word."""
    count = 0
    for item in word:
        if ignore:
            if item == ignore:
                continue

        if item == letter:
            count += 1
    
    return count

def input_for_length(text: str, max_length: int = 5, min_length: int = 0, check_int: bool = False, check_empty: bool = False):
    while True:
        answer = input(text)

        if check_empty == True:
            if not answer or answer == "\n" or answer == " ":
                print("[ERROR] Вы ничего не ввели!")
                continue

        if check_int == True:
            try:
                answer = int(answer)
            except:
                print("[ERROR] Похоже это не число!")
                continue

        if len(answer) > max_length:
            print("[ERROR] Похоже ваш ответ превышает длину в 5 символов!")
            continue

        if len(answer) < min_length:
            print("[ERROR] Похоже ваш ответ не состоит из 5 символов!")
            continue

        return answer

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

        new_words.append(item)

    words = new_words.copy()
    new_words = None

    if not words:
        print("[ERROR] Не найдены слова в 5 символов!")
        os._exit(0)
    else:
        print(f"[INFO] Найдено [{len(words)}] слов с длинной из пяти символов!")
    
    not_exists_list = []
    exists_list = []
    words_used_list = []
    known_positions = {}
    bad_positions_D = {}

    print('[INFO] Запускаю поиск...')
    count = 0
    while True:
        count += 1
        if count == 6: # Максимальное кол-во строчек для слов в самом приложении.
            print("[INFO] У вас закончились попытки!")
            break

        # word_used = input(f"[{count}] Введите введенное слово: ")
        word_used = input_for_length(text=f"[{count}] Введите введенное слово: ", max_length=5, min_length=5, check_int=False, check_empty=True)
        word_used = word_used.lower()
        if word_used not in words_used_list:
            words_used_list.append(word_used)
        print(f"[INFO] Список введенных слов: {words_used_list}")

        # exists = input("Введите буквы, которые точно есть в слове (пр. ___о_): ")
        exists = input_for_length(text="Введите буквы, которые точно есть в слове (пр. ___о_): ", max_length=5, check_int=False, check_empty=False)
        if not exists or exists == "\n" or exists == " ":
            exists = ''

        exists = exists.lower()

        word_example = ""
        for item in exists:
            word_example = word_example + item

            if item == "_":
                continue

            copies = get_same_count(exists, item, "_")
            if item in exists_list:
                if copies > 1:
                    exists_list.remove(item)
                    exists_list.append({"letter": item, "amount": copies})
                else:
                    pass
            elif {"letter": item, "amount": copies} in exists_list:
                pass
            else:
                break_else = False
                for i in range(10):
                    if {"letter": item, "amount": i} in exists_list:
                        break_else = True
                        break

                if break_else == False:
                    if item in not_exists_list:
                        not_exists_list.remove(item)
                        exists_list.append({"letter": item, "amount": copies})
                    else:
                        exists_list.append(item)

        print(f"[INFO] Список существующих букв: {exists_list}")

        # not_exists = input("Введите буквы, которых точно нет в слове (пр. хут_р): ")
        # not_exists = input_for_length(text="Введите буквы, которых точно нет в слове (пр. хут_р): ", max_length=5, check_int=False, check_empty=False)
        # if not not_exists or not_exists == "\n" or not_exists == " ":
        #     not_exists = ''

        # not_exists = not_exists.lower()

        for val, item in enumerate(word_used):
            if exists[val] == "_":
                if item not in not_exists_list:
                    if item in exists_list:
                        exists_list.remove(item)
                        exists_list.append({"letter": item, "amount": 1})
                    elif {"letter": item, "amount": 1} in exists_list:
                        pass
                    else:
                        not_exists_list.append(item)
                    # not_exists_list.append(item)

        print(f"[INFO] Список не существующих букв: {not_exists_list}")

        # positions = input("Введите расположение букв в слове (пример: ор__з): ")
        positions = input_for_length(text="Введите расположение букв в слове (пример: ор__з): ", max_length=5, check_int=False, check_empty=False)
        if not positions or positions == "\n" or positions == " ":
            positions = ''

        positions = positions.lower()

        bad_pos_word_ex = word_example

        for val, item in enumerate(positions):
            if item == "_":
                continue

            known_positions[val] = item
            bad_pos_word_ex = bad_pos_word_ex[:val] + "_" + bad_pos_word_ex[val+1:]

        print(f"[INFO] Список позиций букв: {known_positions}")

        # bad_positions = input_for_length(text="Введите не верное расположение букв в слове (буквы есть в слове, но не на позиции) (пример: __бу_): ", max_length=5, check_int=False, check_empty=False)
        # if not bad_positions or bad_positions == "\n" or bad_positions == " ":
        #     bad_positions = ''

        # bad_positions = bad_positions.lower()

        # for val, item in enumerate(bad_positions):
        for val, item in enumerate(bad_pos_word_ex):
            if item == "_":
                continue

            if not bad_positions_D.get(val):
                bad_positions_D[val] = [item]
            else:
                bad_positions_D[val].append(item)

        print(f"[INFO] Список неправильных позиций букв: {bad_positions_D}")

        bar = progressbar.ProgressBar(
            max_value=len(words))
        amount = 0

        matched_words = []

        print('[INFO] Ищу слова...')

        for word in words:
            word = str(word).lower()
            
            words_repeat_count = {}
            for item in word:
                if words_repeat_count.get(item):
                    words_repeat_count[item] = words_repeat_count.get(item) + 1
                else:
                    words_repeat_count[item] = 1

            amount += 1
            try:
                bar.update(amount)
            except:
                pass

            # Проверка на расположение букв
            skip_word = False
            for val, letter in enumerate(word):
                if known_positions.get(val):
                    if letter != known_positions.get(val):
                        skip_word = True
                        break
            if skip_word:
                # if word == "оазис":
                #     print("4")
                continue

            skip_word = False
            for val, letter in enumerate(word):
                if bad_positions_D.get(val):
                    if letter in bad_positions_D.get(val):
                        skip_word = True
                        break

            if skip_word:
                continue

            # Проверка на уже введенные слова
            skip_word = False
            for item in words_used_list:
                if str(item).lower() == word:
                    skip_word = True
                    break
                
            if skip_word:
                # if word == "оазис":
                #     print('1')
                continue

            # Проверка на не существующие буквы в слове
            skip_word = False
            for item in not_exists_list:
                if item in word:
                    skip_word = True
                    break
                
            if skip_word:
                # if word == "оазис":
                #     print('2')
                continue

            # Проверка на существующие буквы в слове
            skip_word = False
            for item in exists_list:
                if isinstance(item , str):
                    if item not in word:
                        skip_word = True
                        break
                elif isinstance(item , dict):
                    if not item.get("letter") in word:
                        skip_word = True
                        break
                    else:
                        if words_repeat_count.get(item.get("letter")) > item.get("amount"):
                            skip_word = True
                            break
                else:
                    break

            if skip_word:
                # if word == "оазис": # Это было добавлено для проверок на совпадение слов и поиска причины отклонения слова.
                #     print('3')
                continue
            
            matched_words.append(word)

        bar.finish()

        if matched_words:
            for item in matched_words: # Выводим каждом совпадающее слово.
                print(item)
        else:
            print('[INFO] Слова не найдены!')

        words = matched_words.copy()

        print("\n")

if __name__ == "__main__":
    main()