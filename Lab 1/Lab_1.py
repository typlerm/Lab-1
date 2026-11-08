"""
Лабораторна робота: вбудовані структури даних Python.
Завдання 1–5. Детерміновані дані, без сторонніх бібліотек.
"""
import time
import timeit


# =====================================================================
# ЗАВДАННЯ 1. Списки: індексація, зрізи, мутації in-place
# =====================================================================
def task1_lists():
    print("=" * 70)
    print("ЗАВДАННЯ 1. Списки: індексація, зрізи та мутації")
    print("=" * 70)

    # Детерміновані початкові дані (тип: int)
    nums = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    print(f"Початковий список: {nums}  (len={len(nums)})")

    # --- Індексація ---
    print(f"\n[Індексація]")
    print(f"  nums[0]   = {nums[0]}")
    print(f"  nums[2]   = {nums[2]}")
    print(f"  nums[-1]  = {nums[-1]}")
    print(f"  nums[-3]  = {nums[-3]}")

    # --- Три різні зрізи (створюють НОВІ списки) ---
    print(f"\n[Зрізи — створюють нові спискові об'єкти]")
    s1 = nums[2:6]          # start:stop без кроку
    s2 = nums[:4]           # від початку
    s3 = nums[::2]          # з кроком 2
    s4 = nums[::-1]         # реверс (крок -1)
    print(f"  nums[2:6]   = {s1}")
    print(f"  nums[:4]    = {s2}")
    print(f"  nums[::2]   = {s3}")
    print(f"  nums[::-1]  = {s4}")
    print(f"  (зрізи — це копії: s1 is nums -> {s1 is nums})")

    # --- Мутація in-place (змінює той самий об'єкт) ---
    print(f"\n[Мутації in-place]")

    nums.append(100)
    print(f"  append(100)       -> {nums}  (len={len(nums)})")

    nums.insert(2, 25)
    print(f"  insert(2, 25)     -> {nums}  (len={len(nums)})")

    nums.remove(40)     # видалення за значенням
    print(f"  remove(40)        -> {nums}  (len={len(nums)})")

    del nums[0]         # видалення за індексом
    print(f"  del nums[0]       -> {nums}  (len={len(nums)})")

    nums[1:3] = [21, 31, 41]   # заміна діапазону
    print(f"  nums[1:3]=[...]   -> {nums}  (len={len(nums)})")

    print("\nПояснення: append/insert/remove/del/зрізова заміна змінюють "
          "існуючий список (той самий id), тоді як зрізи nums[a:b] та "
          "конкатенація nums + [..] створюють новий об'єкт — це важливо "
          "для пам'яті та очікуваної семантики посилань.")


# =====================================================================
# ЗАВДАННЯ 2. Кортежі, розпакування, агрегат, іммутабельність
# =====================================================================
def task2_tuples():
    print("\n" + "=" * 70)
    print("ЗАВДАННЯ 2. Кортежі: розпакування, агрегат, іммутабельність")
    print("=" * 70)

    # Записи: (id, назва, кількість, ціна_за_од.)
    goods = [
        ("A01", "Зошит",   20, 15.50),
        ("A02", "Ручка",   50,  8.00),
        ("A03", "Олівець", 30,  6.25),
    ]

    print("Записи (id, назва, кількість, ціна):")
    for g in goods:
        print("  ", g)

    # Функція 1: розпакування одного кортежу
    def unpack_record(rec):
        gid, name, qty, price = rec
        return gid, name, qty, price, qty * price

    # Функція 2: агрегат — загальна вартість
    def total_value(records):
        total = 0.0
        for rec in records:
            _, _, qty, price = rec
            total += qty * price
        return total

    print("\nРозпакування першого запису:")
    gid, name, qty, price, subtotal = unpack_record(goods[0])
    print(f"  id={gid}, назва={name}, кількість={qty}, "
          f"ціна={price:.2f} грн, вартість={subtotal:.2f} грн")

    total = total_value(goods)
    print(f"\nЗагальна вартість усіх позицій: {total:.2f} грн")

    # Демонстрація іммутабельності кортежу
    print("\n[Іммутабельність кортежу]")
    try:
        goods[0][1] = "Зошит-2"   # спроба змінити елемент кортежу
    except TypeError as e:
        print(f"  Спроба goods[0][1] = ... -> TypeError: {e}")

    # Вкладений мутабельний об'єкт: список оцінок усередині кортежу
    student = ("Іваненко", "КН-21", [90, 85, 78])
    print(f"\n[Вкладений мутабельний об'єкт]")
    print(f"  student = {student}")
    student[2].append(95)         # змінюємо ВМІСТ списку
    print(f"  після student[2].append(95) -> {student}")
    print("  Пояснення: незмінним залишається лише контейнер кортежу "
          "(посилання на список), а сам список — мутабельний, тому "
          "його вміст може змінюватися.")


# =====================================================================
# ЗАВДАННЯ 3. Словник частот
# =====================================================================
def task3_word_freq():
    print("\n" + "=" * 70)
    print("ЗАВДАННЯ 3. Словник частот слів")
    print("=" * 70)

    text = (
        "Python — це мова програмування. Python простий. "
        "Мова Python популярна, і Python швидко вчиться!"
    )
    print(f"Вхідний текст:\n  {text!r}\n")

    # Токенізація: літери/апостроф, нижній регістр; розділові знаки — межі
    def tokenize(s):
        word = []
        tokens = []
        for ch in s.lower():
            if ch.isalpha() or ch == "'":
                word.append(ch)
            else:
                if word:
                    tokens.append("".join(word))
                    word = []
        if word:
            tokens.append("".join(word))
        return tokens

    tokens = tokenize(text)
    print(f"Токени: {tokens}")

    # Підрахунок (без collections.Counter)
    freq = {}
    for w in tokens:
        # безпечний доступ до відсутнього ключа
        freq[w] = freq.get(w, 0) + 1

    # Сортування за ключем
    print("\nЗа ключем (алфавіт):")
    for k in sorted(freq):
        print(f"  {k!r:12} -> {freq[k]}")

    # Сортування за спаданням частоти, потім за ключем
    print("\nЗа спаданням частоти:")
    for k in sorted(freq, key=lambda x: (-freq[x], x)):
        print(f"  {k!r:12} -> {freq[k]}")

    # dict comprehension: лише частота >= 2
    THRESHOLD = 2
    popular = {k: v for k, v in freq.items() if v >= THRESHOLD}
    print(f"\nЛише часті слова (freq >= {THRESHOLD}): {popular}")


# =====================================================================
# ЗАВДАННЯ 4. Множини
# =====================================================================
def task4_sets():
    print("\n" + "=" * 70)
    print("ЗАВДІННЯ 4. Множини: унікальність та операції")
    print("=" * 70)

    A_raw = ["u1", "u2", "u2", "u3", "u4", "u5"]
    B_raw = ["u4", "u5", "u6", "u6", "u7"]
    C_raw = ["u4", "u5"]

    A = set(A_raw)
    B = set(B_raw)
    C = set(C_raw)

    print(f"A (raw) = {A_raw}  ->  set(A) = {sorted(A)}")
    print(f"B (raw) = {B_raw}  ->  set(B) = {sorted(B)}")
    print(f"C (raw) = {C_raw}  ->  set(C) = {sorted(C)}")

    print(f"\nA ∩ B = {sorted(A & B)}")
    print(f"A ∪ B = {sorted(A | B)}")
    print(f"A Δ B = {sorted(A ^ B)}")

    print(f"\nC <= A ? {C <= A}   (True/False)")
    print(f"C <= B ? {C <= B}   (True/False)")
    print(f"A <= C ? {A <= C}   (True/False)")

    # frozenset як елемент іншої множини
    fs1 = frozenset({"x", "y"})
    fs2 = frozenset({"y", "z"})
    container = {fs1, fs2}
    print(f"\nfrozenset у множині: {container}")
    print("Сценарій: множина як незмінний ключ/елемент — коли потрібно "
          "групувати набори тегів без ризику випадкової мутації.")


# =====================================================================
# ЗАВДАННЯ 5. Вимірювання складності
# =====================================================================
def task5_perf():
    print("\n" + "=" * 70)
    print("ЗАВДІННЯ 5. Алгоритмічна складність: вимірювання")
    print("=" * 70)

    sizes = [1_000, 10_000, 100_000]
    repeats = 3

    def bench(func, number=1):
        """Повертає середній час у мс за `number` повторів."""
        t = timeit.timeit(func, number=number) / number * 1000
        return t

    print(f"{'n':>10} | {'list_in (ms)':>14} | {'set_in (ms)':>13} | "
          f"{'dict_key (ms)':>15} | {'uniq list (ms)':>16} | "
          f"{'uniq set (ms)':>14}")
    print("-" * 95)

    for n in sizes:
        data = list(range(n))
        target = n - 1                       # є в колекції
        ls = data
        ss = set(data)
        dd = {i: None for i in range(n)}

        t_list = bench(lambda: target in ls, number=repeats)
        t_set  = bench(lambda: target in ss, number=repeats)
        t_dict = bench(lambda: target in dd, number=repeats)

        # унікальність одним проходом
        src = data + data[: n // 10]         # з дублікатами

        def uniq_list():
            out = []
            for x in src:
                if x not in out:             # O(n) усередині
                    out.append(x)
            return out

        def uniq_set():
            out = set()
            for x in src:
                out.add(x)                   # O(1) у середньому
            return out

        # для великих n uniq_list робимо менше повторів (він O(n²))
        reps_ul = 1 if n >= 10_000 else repeats
        t_ul = bench(uniq_list, number=reps_ul)
        t_us = bench(uniq_set,  number=repeats)

        print(f"{n:>10} | {t_list:>14.4f} | {t_set:>13.4f} | "
              f"{t_dict:>15.4f} | {t_ul:>16.4f} | {t_us:>14.4f}")

    print("\nАсимптотика (теоретичне обґрунтування):")
    print("  list membership  : O(n)   — лінійний пошук")
    print("  set membership   : O(1)   — у середньому, за коректного хешу")
    print("  dict key lookup  : O(1)   — у середньому")
    print("  uniqueness list  : O(n²)  — 'if x not in out' всередині циклу")
    print("  uniqueness set   : O(n)   — add() у середньому O(1)")
    print("\nВисновки:")
    print("  * Для частих звернень за ключем — dict.")
    print("  * Для збереження порядку вставки з дедуплікацією — dict "
          "(зберігає порядок у сучасному Python) або list з супровідним set.")
    print("  * Для 'чи вже зустрічали' під час одного проходу — set "
          "дає O(1) у середньому проти O(n) у списку.")


# =====================================================================
if __name__ == "__main__":
    task1_lists()
    task2_tuples()
    task3_word_freq()
    task4_sets()
    task5_perf()